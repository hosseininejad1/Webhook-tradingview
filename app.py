from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import Json

app = Flask(__name__)

# تنظیمات اتصال به دیتابیس
DB_CONFIG = {
    'dbname': 'tradingview_webhook',
    'user': 'postgres',  # نام کاربری PostgreSQL
    'password': '123456',  # رمز عبور PostgreSQL
    'host': 'localhost'
}

# تابع ذخیره داده در دیتابیس
def save_to_database(payload):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            # ذخیره داده‌ها به صورت رشته خام
            cursor.execute(
                "INSERT INTO webhook_data (payload) VALUES (%s)",
                [payload]
            )

# مسیر وب‌هوک
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # دریافت داده‌های خام ورودی
        raw_data = request.data.decode('utf-8')  # تبدیل داده‌های خام به رشته
        if not raw_data:
            return jsonify({'error': 'No data received'}), 400

        save_to_database(raw_data)  # ذخیره داده‌های خام در دیتابیس
        return jsonify({'message': 'Data saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)