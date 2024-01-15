from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import desc
import os
import socket
import webbrowser  # Import the webbrowser module

templates_path = os.path.join(os.getcwd(), 'templates')

app = Flask(__name__, template_folder=templates_path)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for QR code data
class QRCodeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    # Fetch the latest two entries based on the timestamp
    qr_code_data = QRCodeData.query.order_by(desc(QRCodeData.timestamp)).limit(2).all()

    if not qr_code_data or len(qr_code_data) < 2:
        # If there are no entries or less than two entries, create and add a new entry with an initial value of "1"
        new_data = QRCodeData(data="1")
        db.session.add(new_data)
        db.session.commit()
        qr_code_data = [new_data]
    else:
        # Reverse the order to get the entry that came before the latest one
        qr_code_data = qr_code_data[::-1]

    # Ensure that qr_code_data has at least two elements
    if len(qr_code_data) >= 2:
        return render_template('index.html', qr_code_data=qr_code_data[1].data)
    else:
        # Handle the case when there are not enough elements
        return render_template('index.html', qr_code_data="1")

@app.route('/qr-data', methods=['POST'])
def receive_qr_data():
    qr_code_data = request.json.get('qrCodeData')
    print(f"Received QR Code Data: {qr_code_data}")

    # Save QR code data to the database
    new_data = QRCodeData(data=qr_code_data)
    db.session.add(new_data)
    db.session.commit()

    return {'status': 'success'}

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables before running the app
        db.create_all()

    local_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server running at http://{local_ip}:5000/")

    # Open the default web browser to the Flask app
    webbrowser.open(f"http://{local_ip}:5000/")

    # Use Waitress as the server
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
