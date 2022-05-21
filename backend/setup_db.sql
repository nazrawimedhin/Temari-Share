-- create user and set up db
CREATE user IF NOT EXISTS 'temari'@'localhost' IDENTIFIED BY 'temari_pwd';
GRANT ALL ON temari_db.* TO 'temari'@'localhost';

CREATE DATABASE IF NOT EXISTS temari_db;
