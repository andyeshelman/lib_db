CREATE DATABASE bb_public_library;

USE bb_public_library;

CREATE TABLE Users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE Media (
	media_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE Books (
	book_id INT PRIMARY KEY,
    author VARCHAR(255) NOT NULL,
    pub_year YEAR NOT NULL,
    FOREIGN KEY (book_id) REFERENCES Media(media_id)
);

CREATE TABLE Movies (
	movie_id INT PRIMARY KEY,
    director VARCHAR(255) NOT NULL,
    rel_year YEAR NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES Media(media_id)
);

CREATE TABLE Borrowed (
    user_id INT NOT NULL,
    media_id INT PRIMARY KEY,
    FOREIGN KEY (media_id) REFERENCES Media(media_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Users(name, email) VALUES
("Spongebob Squarepants", "imready@bikinibottom.org"),
("Gary", "meow@bikinibottom.org"),
("Squidward Tentacles", "clarinetgoesbrrr@bikinibottom.org"),
("Patrick Star", "emailaddress@bikinibottom.org");

INSERT INTO Media(title) VALUES
("Advanced Jellyfishing"),
("Annals of Sophistication");

INSERT INTO Books(book_id, author, pub_year) VALUES
(1, "Smitty Werbenjagermanjensen", "1999"),
(2, "Squilliam Fancyson", "1999");

INSERT INTO Borrowed(user_id, media_id) VALUES (3, 2);