import requests
import csv
from config import Config

def fetch_odds_data(sport=None, region=None, markets=None, odds_format=None, date_format=None):
    """
    Fetch odds data from the Odds API and save it to a CSV file.
    """
    sport = sport or Config.DEFAULT_SPORT
    region = region or Config.DEFAULT_REGION
    markets = markets or Config.DEFAULT_MARKETS
    odds_format = odds_format or Config.ODDS_FORMAT
    date_format = date_format or Config.DATE_FORMAT

    url = f"{Config.BASE_URL}/sports/{sport}/odds"
    params = {
        "apiKey": Config.ODDS_API_KEY,
        "regions": region,
        "markets": markets,
        "oddsFormat": odds_format,
        "dateFormat": date_format,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        with open(Config.CSV_FILE_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Sport", "Region", "Match", "Bookmaker", "Market", "Outcome", "Odds Format", "Odds", "Date"])

            for game in data:
                match = f"{game['home_team']} vs {game['away_team']}"
                for bookmaker in game['bookmakers']:
                    site_name = bookmaker['title']
                    for market in bookmaker['markets']:
                        market_type = market['key']
                        for outcome in market['outcomes']:
                            writer.writerow([
                                sport, region, match, site_name, market_type,
                                outcome['name'], odds_format,
                                outcome['price'], game['commence_time']
                            ])

        return Config.CSV_FILE_PATH

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
