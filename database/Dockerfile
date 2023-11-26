FROM postgres:latest

# If you have a custom PostgreSQL configuration, you can uncomment the next line and adjust the file path accordingly.
# COPY your_postgres_conf.conf /etc/postgresql/conf.d/your_postgres_conf.conf

# Copy the initial SQL script to the container.
# This script will be executed when the container starts for the first time.
COPY initial.sql /docker-entrypoint-initdb.d/

# Set environment variables for the PostgreSQL container.
ENV POSTGRES_DB=furniture_reservation_system
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=secret
