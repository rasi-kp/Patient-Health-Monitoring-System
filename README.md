# Patient-Health-Monitoring-System

LOGIN PAGE

<img width="960" alt="p1" src="https://github.com/rasi-kp/Patient-Health-Monitoring-System/assets/107319917/a1307f1b-cdcd-4bb0-ace2-6f8ecbb5293b">

HOME PAGE

<img width="959" alt="p3" src="https://github.com/rasi-kp/Patient-Health-Monitoring-System/assets/107319917/48068e0f-0690-45b0-835d-bce93286c9b2">

PREDICTION PAGE

<img width="959" alt="p7" src="https://github.com/rasi-kp/Patient-Health-Monitoring-System/assets/107319917/098fc02e-c7b8-45c2-b55c-610eaf925142">

RESULT PAGE

<img width="960" alt="p9" src="https://github.com/rasi-kp/Patient-Health-Monitoring-System/assets/107319917/5a1c3612-89e0-4122-99e1-e679b7731623">
<img width="960" alt="p10" src="https://github.com/rasi-kp/Patient-Health-Monitoring-System/assets/107319917/fa0dd5ce-ca60-4146-b547-bd85ff667138">

PAST HISTORY PAGE

<img width="960" alt="p8" src="https://github.com/rasi-kp/Patient-Health-Monitoring-System/assets/107319917/bf15e359-e53e-4e38-8c18-58a78e0f9c72">

************ Database Creation ************

initially to connect the database and program
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

SHOW TABLE COMMENT............
mysql> show tables;

TO SEE THE DATA FROM THE TABLE...
mysql> select * from data;


TABLE STRUCTURE........
mysql> describe data;

----------------------------------------------------------------------------------------------------------------------------

*************************** PROGRAM RUN ***************************

First run model.py
then run app.py




