create database `short-me-api`;
use `short-me-api`;

create table `urls` (
    `name`varchar(100) not null UNIQUE,
    `requested_name` varchar(100),
    `short_name` varchar(100) not null,
    `created_at` timestamp not null default NOW(),
    `expire_at` timestamp not null default ADDDATE(NOW(), INTERVAL 7 DAY)
)engine = InnoDB;