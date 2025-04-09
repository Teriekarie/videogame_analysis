# vgchartz-scraper

A Python project to scrape video game data from [VGChartz](https://www.vgchartz.com/gamedb/). This project aims to collect and analyze video game sales data for various platforms.

## Project Structure

```
vgchartz-scraper
├── src
│   ├── scraped_data.py       # Main script to handle data scraping
│   ├── scraper.py            # Contains the scraping logic
│   └── utils
│       └── helpers.py        # Utility functions for the scraper
├── requirements.txt          # List of dependencies
├── .gitignore                # Files and directories to ignore in version control
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vgchartz-scraper.git
   cd vgchartz-scraper
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the scraper, execute the following command:
```
python src/scraper.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

