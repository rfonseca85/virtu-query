from openai import AsyncOpenAI
import chainlit as cl
from chainlit.prompt import Prompt, PromptMessage
from chainlit.playground.providers.openai import ChatOpenAI
from decouple import config
import mysql.connector
from tabulate import tabulate

# Set up BigQuery client
# client = bigquery.Client(location="EU")

openai_client = AsyncOpenAI()
settings = {"model": "gpt-3.5-turbo", "temperature": 0, "stop": ["```"]}

sql_query_prompt = """You are tasked with generating MySQL queries for a furniture order reservation system database. Here is the database structure:

-- Database Name: furniture_reservation_system

-- Tables:
1. customers (customer_id, first_name, last_name, email, phone_number)
2. furniture (product_id, product_name, description, price)
3. orders (order_id, customer_id, order_date, total_amount)
4. order_items (item_id, order_id, product_id, quantity)

Please provide just the query
{input}
```"""

explain_query_result_prompt = """Today is {date}
You received a query from a customer support operator regarding the orders table.
They executed a SQL query and provided the results in Markdown table format.
Analyze the table and explain the problem to the operator.

Markdown Table:

```
{table}
```

Short and concise analysis:
"""


async def build_query(message: cl.Message):
    # Create the prompt object
    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="user",
                template=sql_query_prompt,
                formatted=sql_query_prompt.format(input=message.content),
            )
        ],
        settings=settings,
        inputs={"input": message.content},
    )

    # Prepare the message for streaming
    msg = cl.Message(content="", author="query", language="sql", parent_id=message.id)
    await msg.send()

    # Call OpenAI and stream the message
    stream_resp = await openai_client.chat.completions.create(
        messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
    )
    async for part in stream_resp:
        token = part.choices[0].delta.content or ""
        if token:
            await msg.stream_token(token)

    # Update the prompt object with the completion
    prompt.completion = msg.content
    msg.prompt = prompt

    # Send and close the message stream
    await msg.update()

    return msg.content


def execute_query_and_add_to_markdown_table(query):
    host = config('DATABASE_HOST')
    user = config('DATABASE_USER')
    password = config('DATABASE_PASSWORD')
    database = config('DATABASE_NAME')

    # Connect to the MySQL database
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        result = cursor.fetchall()

        # Create a Markdown table from the query result
        if result:
            table = tabulate(result, headers=cursor.column_names, tablefmt="pipe")
            return table
        else:
            return "No results found."

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


execute_query_and_add_to_markdown_table("SELECT * FROM orders")

# async def run_and_analyze(parent_id: str, query: str):
#     table = execute_query(query=query)
#
#     await cl.Message(content=table, parent_id=parent_id, author="result").send()
#
#     # Create the prompt object
#     today = str(date.today())
#     prompt = Prompt(
#         provider=ChatOpenAI.id,
#         messages=[
#             PromptMessage(
#                 role="user",
#                 template=explain_query_result_prompt,
#                 formatted=explain_query_result_prompt.format(date=today, table=table),
#             )
#         ],
#         settings=settings,
#         inputs={"date": today, "table": table},
#     )
#
#     # Prepare the message for streaming
#     msg = cl.Message(
#         content="",
#     )
#     await msg.send()
#
#     # Call OpenAI and stream the message
#     stream = await openai_client.chat.completions.create(
#         messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
#     )
#     async for part in stream:
#         token = part.choices[0].delta.content or ""
#         if token:
#             await msg.stream_token(token)
#
#     # Update the prompt object with the completion
#     prompt.completion = msg.content
#     msg.prompt = prompt
#
#     msg.actions = [cl.Action(name="take_action", value="action", label="Take action")]
#
#     # Send and close the message stream
#     await msg.update()


@cl.action_callback(name="take_action")
async def take_action(action: cl.Action):
    await cl.Message(content="Contacting shipping carrier...").send()


@cl.on_message
async def main(message: cl.Message):
    query = await build_query(message)
    # await run_and_analyze(message.id, query)

# @cl.oauth_callback
# def auth_callback(provider_id: str, token: str, raw_user_data, default_app_user):
#     if provider_id == "google":
#         if "@chainlit.io" in raw_user_data["email"]:
#             return default_app_user
#     return None


# chainlit run app.py -w --port 8081
