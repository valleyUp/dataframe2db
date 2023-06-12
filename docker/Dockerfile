FROM mysql:latest
WORKDIR /matExplorer/db
ENV LANG=C.UTF-8
ENV MYSQL_ROOT_PASSWORD=1
ENV MYSQL_DATABASE=matDatabase
ADD matDatabase.sql /docker-entrypoint-initdb.d/