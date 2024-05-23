CREATE DATABASE bb_public_library;

USE bb_public_library;

CREATE TABLE Users (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE Media (
	id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE Books (
	id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(255) NOT NULL,
    pub_year YEAR NOT NULL,
    media_id INT UNIQUE NOT NULL,
    FOREIGN KEY (media_id) REFERENCES Media(id)
);

CREATE TABLE Movies (
	id INT AUTO_INCREMENT PRIMARY KEY,
    director VARCHAR(255) NOT NULL,
    rel_year YEAR NOT NULL,
    media_id INT UNIQUE NOT NULL,
    FOREIGN KEY (media_id) REFERENCES Media(id)
);

CREATE TABLE Borrowed (
	id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    media_id INT UNIQUE NOT NULL,
    borrow_date DATE,
    return_date DATE,
    FOREIGN KEY (media_id) REFERENCES Media(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

INSERT INTO Users(name, email) VALUES
("Spongebob Squarepants", "imready@bikinibottom.org"),
("Gary", "meow@bikinibottom.org"),
("Squidward Tentacles", "clarinetgoesbrrr@bikinibottom.org"),
("Patrick Star", "emailaddress@bikinibottom.org");

INSERT INTO Media(title) VALUES
("Advanced Jellyfishing"),
("Annals of Sophistication");

INSERT INTO Books(media_id, author, pub_year) VALUES
(1, "Smitty Werbenjagermanjensen", "1999"),
(2, "Squilliam Fancyson", "1999");

INSERT INTO Borrowed(user_id, media_id) VALUES (3, 2);