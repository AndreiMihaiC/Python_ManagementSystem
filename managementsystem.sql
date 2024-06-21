CREATE DATABASE sms2;
USE sms2;
DROP DATABASE sms2;

CREATE TABLE students (
	nr INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    contact VARCHAR(50),
    field_of_study VARCHAR(200),
    address VARCHAR(100)
);

SELECT * FROM students;