from flask import Flask, jsonify, request, render_template
import os
from sqlalchemy import create_engine
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

    # Build SQL query dynamically based on filters
    query = "SELECT * FROM data WHERE 1=1"
    if year:
        query += f" AND end_year={year}"
    if topics:
        query += f" AND topic LIKE '%{topics}%'"
    if sector:
        query += f" AND sector='{sector}'"
    if region:
        query += f" AND region='{region}'"
    if pest:
        query += f" AND pestle='{pest}'"
    if source:
        query += f" AND source='{source}'"

    print('Executing query:', query)  # Debugging line

    # Execute query and fetch data into a DataFrame
    df = pd.read_sql(query, engine)

    # Convert DataFrame to JSON and return as response
    return df.to_json(orient='records')

# Define index route to render the dashboard
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
