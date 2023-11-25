FROM mysql:8.0

# Copy the custom my.cnf file into the MySQL container.
COPY my.cnf /etc/mysql/conf.d/my.cnf

# Copy the initial.sql file into the docker-entrypoint-initdb.d directory.
COPY initial.sql /docker-entrypoint-initdb.d/

# Set environment variables for the MySQL container.
ENV MYSQL_DATABASE=furniture_reservation_system
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin
ENV MYSQL_ROOT_PASSWORD=root