import requests
import pandas as pd
import psycopg2

# STEP 1: EXTRACT from AviationStack API
url = "http://api.aviationstack.com/v1/flights"
params = {
    'access_key': 'cf6918c34e113d9935e6bc438a1f80ce',  # Replace with your real key
    'dep_iata': 'JFK',
    'arr_iata': 'LAX'
}

response = requests.get(url, params=params)
data = response.json()

# STEP 2: TRANSFORM into a DataFrame
flights = []
for flight in data['data']:
    flights.append({
        'flight_code': flight['flight']['iata'],
        'airline': flight['airline']['name'],
        'departure_time': flight['departure']['scheduled'],
        'arrival_time': flight['arrival']['scheduled']
    })

df = pd.DataFrame(flights)
print("Extracted Flights:")
print(df)

# STEP 3: LOAD into PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="etl_demo",
        user="yogitaadari",  # change if needed
        password="",         # or use your actual password
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_code TEXT,
            airline TEXT,
            departure_time TIMESTAMP,
            arrival_time TIMESTAMP
        );
    """)

    # Insert data
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO flights (flight_code, airline, departure_time, arrival_time) VALUES (%s, %s, %s, %s)",
            (row['flight_code'], row['airline'], row['departure_time'], row['arrival_time'])
        )

    conn.commit()
    cur.close()
    conn.close()
    print("\n✅ Flight data loaded into PostgreSQL!")

except Exception as e:
    print("\n❌ Error:", e)
