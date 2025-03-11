from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import pool

app = Flask(__name__)

# Database connection parameters
DB_HOST = "aws-0-us-west-1.pooler.supabase.com"
DB_NAME = "postgres"
DB_USER = "postgres.xcdiwzjteviapvrefbzu"
DB_PASS = "Sc0tt062400!"

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(1, 10,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    database=DB_NAME
)

@app.route('/process_pax_data', methods=['POST'])
def process_pax_data():
    data = request.json

    # Extract device name and PAX count from the incoming data
    device_name = data.get('device_name')
    pax_count = data.get('pax_count')

    # Insert data into the database
    conn = connection_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pax_data (device_name, pax_count)
            VALUES (%s, %s)
        """, (device_name, pax_count))
        conn.commit()
    finally:
        cursor.close()
        connection_pool.putconn(conn)

    return jsonify({"message": "PAX data processed successfully!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
