import os
import pandas as pd
import mysql.connector

# Load the cleaned data from the CSV file
data = pd.read_csv('c:/Users/HOME/Downloads/PORTFOLIO_PROJECT/Video_games/cleaned_games_data.csv')

# Replace NaN values with None (to insert as NULL in MySQL)
data = data.where(pd.notnull(data), None)

# Connect to the MySQL server
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),  
    user=os.getenv("MYSQL_USER"),  
    password=os.getenv("MYSQL_PASSWORD")  
)
cursor = db.cursor()

# Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS video_games")
cursor.execute("USE video_games")  # Switch to the database

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    Pos INT,
    Game VARCHAR(255),
    Publisher VARCHAR(255),
    VGChartz_Score FLOAT,
    Critic_Score FLOAT,
    User_Score FLOAT,
    Total_Shipped FLOAT,
    Total_Sales FLOAT,
    NA_Sales FLOAT,
    PAL_Sales FLOAT,
    JP_Sales FLOAT,
    Other_Sales FLOAT,
    Release_Date DATE,
    Last_Update DATE,
    Release_Year INT,
    Release_Month INT,
    Release_Day INT,
    LastUpdate_Year INT,
    LastUpdate_Month INT,
    LastUpdate_Day INT,
    Game_Age_Years INT,
    Update_Lag_Days INT,
    PRIMARY KEY (Pos, Game, Publisher)  -- Composite key to uniquely identify records
)
""")

# Insert or update records in the database
for _, row in data.iterrows():
    sql = """
    INSERT INTO games (Pos, Game, Publisher, VGChartz_Score, Critic_Score, User_Score, Total_Shipped, Total_Sales, NA_Sales, PAL_Sales, JP_Sales, Other_Sales, Release_Date, Last_Update, Release_Year, Release_Month, Release_Day, LastUpdate_Year, LastUpdate_Month, LastUpdate_Day, Game_Age_Years, Update_Lag_Days)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        VGChartz_Score = VALUES(VGChartz_Score),
        Critic_Score = VALUES(Critic_Score),
        User_Score = VALUES(User_Score),
        Total_Shipped = VALUES(Total_Shipped),
        Total_Sales = VALUES(Total_Sales),
        NA_Sales = VALUES(NA_Sales),
        PAL_Sales = VALUES(PAL_Sales),
        JP_Sales = VALUES(JP_Sales),
        Other_Sales = VALUES(Other_Sales),
        Release_Date = VALUES(Release_Date),
        Last_Update = VALUES(Last_Update),
        Release_Year = VALUES(Release_Year),
        Release_Month = VALUES(Release_Month),
        Release_Day = VALUES(Release_Day),
        LastUpdate_Year = VALUES(LastUpdate_Year),
        LastUpdate_Month = VALUES(LastUpdate_Month),
        LastUpdate_Day = VALUES(LastUpdate_Day),
        Game_Age_Years = VALUES(Game_Age_Years),
        Update_Lag_Days = VALUES(Update_Lag_Days);
    """
    cursor.execute(sql, tuple(row))
    db.commit()

# Close the database connection
cursor.close()
db.close()

print("Database has been successfully updated.")