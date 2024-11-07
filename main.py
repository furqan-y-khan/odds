from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for
from odds_fetcher import fetch_odds_data

app = Flask(__name__)

# Define available options (as before)
SPORTS_OPTIONS = [("soccer_epl", "English Premier League"), ("basketball_nba", "NBA Basketball"), ("americanfootball_nfl", "NFL Football")]
REGION_OPTIONS = [("us", "United States"), ("uk", "United Kingdom"), ("au", "Australia"), ("eu", "Europe")]
MARKET_OPTIONS = [("h2h", "Head to Head"), ("spreads", "Point Spreads"), ("totals", "Over/Under Totals")]
ODDS_FORMAT_OPTIONS = [("decimal", "Decimal"), ("american", "American"), ("fractional", "Fractional")]
DATE_FORMAT_OPTIONS = [("iso", "ISO 8601"), ("unix", "Unix Timestamp")]

@app.route("/")
def home():
    # Redirect to the fetch odds form
    return redirect(url_for("fetch_odds"))

@app.route("/fetch-odds", methods=["GET", "POST"])
def fetch_odds():
    if request.method == "POST":
        # Fetch selected form options and trigger data fetching
        sport = request.form.get("sport")
        region = request.form.get("region")
        markets = request.form.get("markets")
        odds_format = request.form.get("odds_format")
        date_format = request.form.get("date_format")

        # Fetch odds data and return as downloadable CSV if successful
        csv_file_path = fetch_odds_data(sport=sport, region=region, markets=markets, odds_format=odds_format, date_format=date_format)
        if csv_file_path:
            return send_file(csv_file_path, as_attachment=True)
        else:
            return jsonify({"error": "Failed to fetch odds data"}), 500

    # Render the form template
    return render_template("fetch_odds_form.html",
                           sports_options=SPORTS_OPTIONS,
                           region_options=REGION_OPTIONS,
                           market_options=MARKET_OPTIONS,
                           odds_format_options=ODDS_FORMAT_OPTIONS,
                           date_format_options=DATE_FORMAT_OPTIONS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
