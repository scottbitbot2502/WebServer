from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import pool

app = Flask(__name__)

# Database connection parameters
DB_CONNECTION_STRING = "postgresql://postgres.xcdiwzjteviapvrefbzu:Sc0tt062400!@aws-0-us-west-1.pooler.supabase.com:5432/postgres"

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(1, 10,
    dsn=DB_CONNECTION_STRING
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
            INSERT INTO public.SceeneData (DeviceID, Pax)
            VALUES (%s, %s)
        """, (device_name, pax_count))
        conn.commit()
    finally:
        cursor.close()
        connection_pool.putconn(conn)

    return jsonify({"message": "PAX data processed successfully!"}), 201

@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    conn = connection_pool.getconn()
    try:
        if conn:
            cursor = conn.cursor()
            # Insert sample data into SceeneData
            cursor.execute("""
                INSERT INTO public.SceeneData (DeviceID, Pax)
                VALUES (%s, %s)
            """, ("Test Device", 1))
            conn.commit()
            return jsonify({"message": "Database connection successful and sample data inserted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            connection_pool.putconn(conn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
