# Patient-Health-Monitoring-System

************ Database Creation ************

initially to connect database and program
localhost="root" password="********"

CREATE DATABASE...................................................
mysql> create database patient;

mysql> use patient;
Database changed

CREATE USER TABLE.................................................

mysql> create table USER (id INT AUTO_INCREMENT,name VARCHAR(20),user VARCHAR(20),pass VARCHAR(20),PRIMARY KEY(id));

CREATE PATIENT DATA STORING........................................

mysql> create table data (date DATETIME,id INT AUTO_INCREMENT,username VARCHAR(20),
glucose INT,bp INT,weight INT,height INT,age INT,pregnancy INT,predict VARCHAR(15),PRIMARY KEY(id));

SHOW TABLE COMMANT............
mysql> show tables;

TO SEE THE DATA FROM THE TABLE....
mysql> select * from data;
+------------+----+----------+---------+------+--------+--------+------+------+-------------+
| data       | id | username | glucose | bp   | weight | height | age  | preg | pred        |
+------------+----+----------+---------+------+--------+--------+------+------+-------------+
| 2023-08-22 |  1 | rasi     |     104 |   62 |     49 |    170 |   21 |    0 | No Diabetes |
| 2023-08-22 |  2 | rasi     |     100 |   50 |     49 |    170 |   50 |    1 | No Diabetes |
+------------+----+----------+---------+------+--------+--------+------+------+-------------+
2 rows in set (0.00 sec)

TABLE STRUCTURE........
mysql> describe data;

----------------------------------------------------------------------------------------------------------------------------

*************************** PROGRAM RUN ***************************





