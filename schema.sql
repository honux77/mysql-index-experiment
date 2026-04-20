# Player(id, nickname, rank, money, start_date, last_login)
# id: int pk auto_increment
# name: 한글 2- 5글자
# nickname: 영문 8 - 32글자, unique
# grank: B, S, G, P, D, C
# money: 0 - 9999900 (원)
# start_date as date: 최근 1년 이내의 날짜
# last_visit as datetime: start_date 보다 클 것, 최근 3개월 이내, NULL 가능

drop table if exists trade;

drop table if exists guser;

create table guser (
    id int primary key auto_increment,
    name char(5),
    nickname varchar(64) unique,
    grank char(1),
    money dec(7, 0),
    start_date date,
    last_visit datetime
) character set utf8mb4;

create table trade (
    id int primary key auto_increment,
    seller int,
    item_name varchar(255),
    price dec(7, 0),
    trade_date date,
    # foreign key (seller) references guser(id)
) character set utf8mb4;
