from flask import Flask, render_template, request
import socket
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variable to store the scanned QR code data
qr_code_data = None

@app.route('/')
def index():
    return render_template('index.html', qr_code_data=qr_code_data)

@app.route('/qr-data', methods=['POST'])
def receive_qr_data():
    global qr_code_data
    qr_code_data = request.json.get('qrCodeData')
    print(f"Received QR Code Data: {qr_code_data}")
    return {'status': 'success'}

if __name__ == '__main__':
    # Get the local IP address of the computer (useful for mobile phone connection)
    local_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server running at http://{local_ip}:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)
    