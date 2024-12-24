import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import Json

app = Flask(__name__)

# تنظیمات اتصال به دیتابیس از طریق متغیر محیطی
DB_URL = os.getenv('DATABASE_URL')

def save_to_database(payload):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO webhook_data (payload) VALUES (%s)",
        [Json(payload)]
    )
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid payload'}), 400
        save_to_database(data)
        return jsonify({'message': 'Data saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)