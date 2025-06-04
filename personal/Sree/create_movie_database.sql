-- Create database if it doesn't exist
IF DB_ID('streamflixDb') IS NULL
BEGIN
    CREATE DATABASE streamflixDb;
    PRINT 'Database streamflixDb created.';
END
ELSE
BEGIN
    PRINT 'Database streamflixDb already exists.';
END
GO

-- Switch to the database
USE streamflixDb;
GO

-- Create Movies Table
CREATE TABLE Movies (
    MovieID INT PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Language NVARCHAR(100),
    Country NVARCHAR(100),
    TotalViews INT
);

-- Create Genres Table
CREATE TABLE Genres (
    GenreID INT IDENTITY(1,1) PRIMARY KEY,
    GenreName NVARCHAR(100) UNIQUE NOT NULL
);

-- Create MovieGenres Table (Many-to-Many between Movies and Genres)
CREATE TABLE MovieGenres (
    MovieID INT,
    GenreID INT,
    PRIMARY KEY (MovieID, GenreID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
);

-- Create Users Table
CREATE TABLE Users (
    UserID NVARCHAR(20) PRIMARY KEY,
    Age INT,
    Gender CHAR(1),
    Country NVARCHAR(100),
    SubscriptionStatus NVARCHAR(50),
    TotalWatchTime INT,
    Device NVARCHAR(50)
);

-- Create Ratings Table
CREATE TABLE Ratings (
    RatingID INT PRIMARY KEY,
    UserID NVARCHAR(20),
    MovieID INT,
    Rating DECIMAL(2,1),
    Timestamp DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);
