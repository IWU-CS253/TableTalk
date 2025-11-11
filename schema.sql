drop table if exists accounts;
create table accounts (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);
drop table if exists posts;
create table posts (
  id integer primary key autoincrement,
  title text not null
);