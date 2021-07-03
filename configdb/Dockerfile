FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD 123
ENV MYSQL_DATABASE footwear_db
ENV MYSQL_USER admin
ENV MYSQL_PASSWORRD 123
ENV MYSQL_ALLOW_EMPTY_PASSWORD yes
ADD footwear_db.sql /docker-entrypoint-initdb.d
CMD [ "default-authentication-plugin=mysql_native_password" ]
EXPOSE 3306