-- DROP database tennis_db;

CREATE DATABASE tennis_db;
USE tennis_db;

CREATE TABLE Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

SELECT * FROM Categories;

CREATE TABLE Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20),
    gender VARCHAR(10),
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

SELECT * FROM Competitions;

CREATE TABLE Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

SELECT * FROM Complexes;

CREATE TABLE Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100),
    country_name VARCHAR(100),
    country_code CHAR(3),
    timezone VARCHAR(100),
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);

SELECT * FROM Venues;

CREATE TABLE Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(100),
    country_code CHAR(3),
    abbreviation VARCHAR(10)
);

SELECT * FROM Competitors;

CREATE TABLE Competitor_Rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    rank1 INT,
    movement INT,
    points INT,
    competitions_played INT,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
);

SELECT * FROM Competitor_Rankings;