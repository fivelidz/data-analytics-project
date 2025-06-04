import pandas as pd
import pyodbc

# --- CONFIGURATION ---
SERVER = 'localhost'
DATABASE = 'streamflixDb'
USERNAME = 'sa'
PASSWORD = 'Lakshmi@18'

# --- CONNECT TO SQL SERVER ---
conn = pyodbc.connect(
    f'DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;DATABASE=streamflixDb;UID=sa;PWD=Lakshmi@18;TrustServerCertificate=yes;'
)
cursor = conn.cursor()

# --- LOAD EXCEL FILES ---
movies_df = pd.read_excel("Movies.xlsx")
ratings_df = pd.read_excel("Ratings_Dataset.xlsx")
users_df = pd.read_excel("Users.xlsx")
print(movies_df.head())
# --- CREATE GENRE TABLE ENTRIES ---
genre_set = set()
for genres in movies_df['Genres']:
    genre_set.update(genres.split('|'))
genre_list = sorted(genre_set)
genres_df = pd.DataFrame({'GenreName': genre_list})
genre_list = list(dict.fromkeys(genre_list))


# --- INSERT GENRES ---
genre_id_map = {}
for genre in genre_list:
    cursor.execute("INSERT INTO Genres (GenreName) OUTPUT INSERTED.GenreID VALUES (?)", genre)
    genre_id = cursor.fetchone()[0]
    genre_id_map[genre] = genre_id
conn.commit()

# --- INSERT MOVIES ---
for _, row in movies_df.iterrows():
    cursor.execute("""
        INSERT INTO Movies (MovieID, Title, [Year], Language, Country, TotalViews)
        VALUES (?, ?, ?, ?, ?, ?)
    """, row['MovieID'], row['Title'],str(row['Year']), row['Language'], row['Country'], row['Total Views'])
conn.commit()

# --- INSERT INTO MOVIEGENRES ---
for _, row in movies_df.iterrows():
    movie_id = row['MovieID']
    genres = row['Genres'].split('|')
    for genre in genres:
        genre_id = genre_id_map[genre]
        cursor.execute("INSERT INTO MovieGenres (MovieID, GenreID) VALUES (?, ?)", movie_id, genre_id)
conn.commit()

# --- INSERT USERS ---
for _, row in users_df.iterrows():
    cursor.execute("""
        INSERT INTO Users (UserID, Age, Gender, Country, SubscriptionStatus, TotalWatchTime, Device)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, row['UserID'], row['Age'], row['Gender'], row['Country'], row['SubscriptionStatus'], row['TotalWatchTime'], row['Device'])
conn.commit()

# --- INSERT RATINGS ---
for _, row in ratings_df.iterrows():
    cursor.execute("""
        INSERT INTO Ratings (RatingID, UserID, MovieID, Rating, Timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, row['RatingID'], row['UserID'], row['MovieID'], row['Rating'], row['Timestamp'])
conn.commit()

# --- CLEANUP ---
cursor.close()
conn.close()
print("✅ Data successfully loaded into SQL Server.")
