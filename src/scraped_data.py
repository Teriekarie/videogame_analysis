import requests
import pandas as pd
from bs4 import BeautifulSoup

# Base URL for the game database
base_url = 'https://www.vgchartz.com/games/games.php'

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Define the expected column names
expected_columns = ['Pos', 'Game', 'Publisher', 'VGChartz Score', 
                    'Critic Score', 'User Score', 'Total Shipped', 'Total Sales', 
                    'NA Sales', 'PAL Sales', 'Japan Sales', 'Other Sales', 
                    'Release Date', 'Last Update']

# Loop through pages
for page in range(1, 200):  # Adjust the range as needed
    print(f"Scraping page {page}...")
    
    url = f"{base_url}?page={page}&results=50&order=Sales&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1&showreleasedate=1&showlastupdate=1"
    
    # Fetch and parse the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select_one('#generalBody table')  # Adjust the selector if needed

    # Skip if no table is found (end of pages)
    if not table:
        print("No more data found. Stopping.")
        break

    # Extract rows from the table
    rows = table.find_all('tr')

    # Initialize a list to store cleaned rows
    cleaned_rows = []

    # Loop through each row
    for row in rows:
        cells = row.find_all('td')  # Extract all cells in the row
        if len(cells) == 0:
            continue  # Skip header or empty rows

        # Extract text content only, ignoring images and irrelevant data
        cleaned_row = []
        for i, cell in enumerate(cells):
            # Skip the "Boxart Missing" and "Series" columns
            if i == 1 or i == 3:  # Skip the image column and "Series" column
                continue
            
            # Special handling for the Game column (index 1)
            if i == 1:
                game_name = cell.find('a')  # Extract the game name from the <a> tag
                if game_name:
                    cleaned_row.append(game_name.get_text(strip=True))
                else:
                    cleaned_row.append("")  # Add an empty string if no game name is found
            else:
                cleaned_row.append(cell.get_text(strip=True))  # Extract text content

        # Append the cleaned row to the list
        cleaned_rows.append(cleaned_row)

    # Convert the cleaned rows to a DataFrame
    df = pd.DataFrame(cleaned_rows)

    # Ensure the DataFrame has the expected number of columns
    if len(df.columns) > len(expected_columns):
        df = df.iloc[:, :len(expected_columns)]  # Keep only the first N columns

    # Rename columns to match the website's structure
    df.columns = expected_columns[:len(df.columns)]

    # Append the data to the main DataFrame
    all_data = pd.concat([all_data, df], ignore_index=True)

# Display the total number of rows scraped
print(f"Total rows scraped: {len(all_data)}")

# Save the scraped data to a CSV file
all_data.to_csv('games_data_2.csv', index=False)
print("Scraped data has been saved to 'games_data_fixed.csv'.")