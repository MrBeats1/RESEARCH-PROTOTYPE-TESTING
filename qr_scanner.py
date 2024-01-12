import requests
import serial
import socket

# Get the local IP address of the computer (useful for mobile phone connection)
local_ip = socket.gethostbyname(socket.gethostname())

# Flask server URL
server_url = f"http://{local_ip}:5000/qr-data"  # Update with your server's IP address and port

# Set the port for your USB-CDC QR scanner
serial_port = 'COM4'  # Update with your actual port

# Open the serial port
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

while True:
    # Read data from the serial port
    qr_code_data = ser.readline().decode('utf-8').strip()
    
    if qr_code_data:
        print(f"QR Code Data: {qr_code_data}")

        # Send QR code data to Flask server
        try:
            response = requests.post(server_url, json={'qrCodeData': qr_code_data})
            print(f"Server Response: {response.json()}")
        except requests.RequestException as e:
            print(f"Error sending data to server: {e}")

# Close the serial port when done
ser.close()

# download modules
# py -m pip install requests
# py -m pip install pyserial