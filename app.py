from flask_cors import CORS
from flask import Flask, request, jsonify
import boto3
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

TO_EMAIL = "epissanos@outlook.com"
FROM_EMAIL = "epissanos@outlook.com"

def init_db():
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return "Email sender with DB is up!"

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('name')
    sender_email = data.get('email')
    message = data.get('message')

    if not all([name, sender_email, message]):
        return jsonify({"error": "Missing fields"}), 400

    timestamp = datetime.utcnow().isoformat()

    try:
        conn = sqlite3.connect('contact.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (name, sender_email, message, timestamp))
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    try:
        ses = boto3.client('ses', region_name='us-east-2')
        subject = f"New message from {name}"
        body = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"
        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [TO_EMAIL]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        return jsonify({"message": "Email sent and stored in database!"}), 200
    except Exception as e:
        return jsonify({"error": f"SES error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



