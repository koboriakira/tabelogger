FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root

WORKDIR work

ADD ./docker/mysql/my.cnf /etc/mysql/conf.d/my.cnf
ADD ./docker/mysql/init init

# mysqlの設定
# RUN service mysql start \
#   && mysql -uroot < ./init/init.ddl \
#   && mysql -uroot tabelogger < ./init/create_stores.sql

# 起動時に読み込むSQLたちは、こうやって放り込める
ADD ./docker/mysql/init/* /docker-entrypoint-initdb.d/

# CMD service mysql start
