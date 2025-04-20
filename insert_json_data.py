import json
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="blackcoffer",
    user="tarun",
    password="blackcoffer",
    host="localhost"
)

# Load JSON data from file with explicit encoding
with open('jsondata.json', encoding='utf-8') as file:
    data = json.load(file)

# Insert JSON data into PostgreSQL
cursor = conn.cursor()
for item in data:
    cursor.execute("""
        INSERT INTO data (end_year, intensity, sector, topic, insight, url, region, start_year, impact, added, published, country, relevance, pestle, source, title, likelihood)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        item.get('end_year') if item.get('end_year') else None,
        item.get('intensity') if item.get('intensity') else None,
        item.get('sector') if item.get('sector') else None,
        item.get('topic') if item.get('topic') else None,
        item.get('insight') if item.get('insight') else None,
        item.get('url') if item.get('url') else None,
        item.get('region') if item.get('region') else None,
        item.get('start_year') if item.get('start_year') else None,
        item.get('impact') if item.get('impact') else None,
        item.get('added') if item.get('added') else None,
        item.get('published') if item.get('published') else None,
        item.get('country') if item.get('country') else None,
        item.get('relevance') if item.get('relevance') else None,
        item.get('pestle') if item.get('pestle') else None,
        item.get('source') if item.get('source') else None,
        item.get('title') if item.get('title') else None,
        item.get('likelihood') if item.get('likelihood') else None
    ))
conn.commit()

# Close cursor and connection
cursor.close()
conn.close()

print("Data inserted successfully.")
