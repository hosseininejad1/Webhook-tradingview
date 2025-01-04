from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# تنظیمات اتصال به دیتابیس
DB_CONFIG = {
    "dbname": "trading_webhook",
    "user": "postgres",
    "password": "Data__Password",  # جایگزین کنید
    "host": "localhost",
    "port": 5432
}

# اتصال به دیتابیس
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)
@app.route('/webhook', methods=['POST'])
def webhook():
    # دریافت داده به صورت متن ساده
    data = request.data.decode('utf-8')  # تبدیل داده‌های ورودی به رشته

    if not data:
        return jsonify({"error": "No data received"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # ذخیره داده در جدول signals
        cur.execute(
            """
            INSERT INTO signals (data) VALUES (%s)
            """,
            (data,)  # ذخیره داده به صورت رشته در ستون 'data'
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
