CREATE DATABASE IF NOT EXISTS Recruiter;

USE Recruiter;

CREATE TABLE IF NOT EXISTS applicants(
	a_id varchar(30) PRIMARY KEY ,
    username VARCHAR(25)  NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARBINARY(250) NOT NULL,
	name VARCHAR(100) NOT NULL,
	gender VARCHAR(5),
    image_file VARCHAR(100) DEFAULT 'default.png'
);

CREATE TABLE IF NOT EXISTS applicant_skill(
	a_id varchar(30) ,
    skill VARCHAR(25)  NOT NULL,
    FOREIGN KEY (a_id) REFERENCES applicants(a_id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS applicant_job(
	a_id varchar(30) ,
    company VARCHAR(25)  NOT NULL,
    title VARCHAR(25) NOT NULL,
    fromdate date NOT NULL,
    todate date NOT NULL,
    FOREIGN KEY (a_id) REFERENCES applicants(a_id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS company(
	c_id varchar(30) PRIMARY KEY ,
	name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARBINARY(250) NOT NULL,
    location VARCHAR(200) ,
    c_type VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS job(
	j_id varchar(30)  PRIMARY KEY,
    title VARCHAR(25)  NOT NULL,
    salary VARCHAR(100) NOT NULL,
	min_exp VARCHAR(10) NOT NULL,
    content VARCHAR(750) NOT NULL,
    c_id varchar(30),
    FOREIGN KEY (c_id) REFERENCES company(c_id) ON UPDATE CASCADE ON DELETE SET NULL 
);

CREATE TABLE IF NOT EXISTS job_tags(
	j_id varchar(30),
    tag varchar(50) NOT NULL,
    FOREIGN KEY (j_id) REFERENCES job(j_id) ON UPDATE CASCADE ON DELETE SET NULL 
);

CREATE TABLE IF NOT EXISTS applied_job(
	a_id varchar(30) ,
    j_id varchar(30) ,
    j_status varchar(25) NOT NULL,
    FOREIGN KEY (a_id) REFERENCES applicants(a_id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (j_id) REFERENCES job(j_id) ON UPDATE CASCADE ON DELETE SET NULL
);

ALTER TABLE company
ADD image_file VARCHAR(100) DEFAULT 'default1.png'
