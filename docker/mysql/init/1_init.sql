CREATE DATABASE tabelogger DEFAULT CHARACTER SET utf8mb4;
# 本番ではパスワードを変更すること
CREATE USER 'admin'@'%'  IDENTIFIED BY 'admin';
GRANT ALL ON tabelogger.* TO admin@localhost;
commit;
