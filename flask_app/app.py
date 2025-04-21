from flask import Flask, jsonify, request, render_template
import os
import json
from sqlalchemy import create_engine, text
import pandas as pd

app = Flask(__name__)

# Configure SQLAlchemy to connect to PostgreSQL
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

# Define route to fetch filtered data
@app.route('/data', methods=['GET'])
def get_data():
    # Retrieve filter values from query parameters
    year = request.args.get('end_year')
    topics = request.args.get('topic')
    sector = request.args.get('sector')
    region = request.args.get('region')
    pest = request.args.get('pestle')
    source = request.args.get('source')

    # Build SQL query dynamically and safely
    query = "SELECT * FROM data WHERE 1=1"
    filters = {}

    if year:
        query += " AND end_year = :year"
        filters["year"] = year
    if topics:
        query += " AND topic ILIKE :topic"
        filters["topic"] = f"%{topics}%"
    if sector:
        query += " AND sector = :sector"
        filters["sector"] = sector
    if region:
        query += " AND region = :region"
        filters["region"] = region
    if pest:
        query += " AND pestle = :pest"
        filters["pest"] = pest
    if source:
        query += " AND source = :source"
        filters["source"] = source

    print('Executing query:', query)  # Debugging

    # Execute query and fetch data into a DataFrame
    df = pd.read_sql(text(query), engine, params=filters)

    # Convert DataFrame to JSON and return as response
    return df.to_json(orient='records')

# Define route to render the dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Route to load data from JSON file into the database
@app.route('/load-json', methods=['POST'])
def load_json():
    try:
        with open('jsondata.json') as f:
            data_list = json.load(f)

        with engine.begin() as conn:
            for item in data_list:
                conn.execute(text("""
                    INSERT INTO data (intensity, likelihood, relevance, year, country, topics, region, city)
                    VALUES (:intensity, :likelihood, :relevance, :year, :country, :topics, :region, :city)
                """), {
                    "intensity": item.get("intensity"),
                    "likelihood": item.get("likelihood"),
                    "relevance": item.get("relevance"),
                    "year": item.get("year"),
                    "country": item.get("country"),
                    "topics": item.get("topics"),
                    "region": item.get("region"),
                    "city": item.get("city")
                })

        return jsonify({"message": "Data loaded successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
