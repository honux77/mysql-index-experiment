# docker exec -i mydb mysql -u honux -pbandi1004 honuxdb --local-infile=1 --default-character-set=utf8mb4 < insert.sql
# set global local_infile=1; -- MySQL 서버에서 LOAD DATA LOCAL INFILE 허용

set foreign_key_checks = 0;
set unique_checks = 0;

load data local infile '/var/lib/mysql-files/guser.csv' into table guser fields terminated by ',' ignore 1 lines;

load data local infile '/var/lib/mysql-files/trade.csv' into table trade fields terminated by ',' ignore 1 lines;

set unique_checks = 1;
set foreign_key_checks = 1;