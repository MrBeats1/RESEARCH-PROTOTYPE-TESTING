import requests
import serial

# Flask server URL
server_url = "http://192.168.1.2:5000/qr-data"  # Update with your server's IP address

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

# downloading modules
# py -m pip install requests
# py -m pip install pyserial