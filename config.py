import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    ODDS_API_KEY = os.getenv("ODDS_API_KEY")
    BASE_URL = "https://api.the-odds-api.com/v4"
    DEFAULT_SPORT = "soccer_epl"
    DEFAULT_REGION = "us"
    DEFAULT_MARKETS = "h2h,spreads,totals"
    ODDS_FORMAT = "decimal"
    DATE_FORMAT = "iso"
    CSV_FILE_PATH = "odds_data.csv"
