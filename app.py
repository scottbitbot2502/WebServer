import os
from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Initialize Supabase client
url: str = "https://xcdiwzjteviapvrefbzu.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjZGl3emp0ZXZpYXB2cmVmYnp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE3MDgwMjMsImV4cCI6MjA1NzI4NDAyM30.PXB3Yva-mgjGyhJgzahAbupCg-efD49Df41Ar0ZoFbs"
supabase: Client = create_client(url, key)

@app.route('/process_pax_data', methods=['POST'])
def process_pax_data():
    data = request.json

    # Extract device name and PAX count from the incoming data
    device_name = data.get('device_name')
    pax_count = data.get('pax_count')

    # Insert data into the database using Supabase client
    response = (
        supabase.table("SceeneData")
        .insert({"DeviceID": device_name, "Pax": pax_count})
        .execute()
    )

    return jsonify({"message": "PAX data processed successfully!", "response": response}), 201

@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    # Insert sample data into SceeneData
    response = (
        supabase.table("SceeneData")
        .insert({"DeviceID": "Test Device", "Pax": 1})
        .execute()
    )
    return jsonify({"message": "Database connection successful and sample data inserted!", "response": response}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
