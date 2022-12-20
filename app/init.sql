CREATE DATABASE IF NOT EXISTS payhere default character set utf8;
use payhere;

create table user
(
    id                  int auto_increment primary key,
    email               varchar(100)                            not null,
    created_at          datetime                                not null,
    updated_at          datetime                                not null,
    password            varchar(100)                            not null
);

create table receipt
(
    id                  int auto_increment primary key,
    user_id             int                                     not null,
    created_at          datetime                                not null,
    updated_at          datetime                                not null,
    payment             int default 0                           null,
    store               varchar(255)                            null,
    memo                varchar(255)                            null,
    foreign key (user_id) references user (id) on update restrict on delete cascade
);

create table detail
(
    id                  int auto_increment  primary key,
    created_at          datetime                                not null,
    updated_at          datetime                                not null,
    receipt_id          int                                     not null,
    payment_method      varchar(20)                             null,
    store_address       varchar(255)                             null,
    store_phone         varchar(20)                             null,
    store_info          varchar(100)                            null,
    url                 varchar(100)                            null,
    foreign key (receipt_id) references receipt (id) on update restrict on delete cascade
);