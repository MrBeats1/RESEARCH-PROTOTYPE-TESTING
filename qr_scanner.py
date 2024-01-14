import serial
from serial.tools import list_ports
import requests
import socket

# Get the local IP address of the computer (useful for mobile phone connection)
local_ip = socket.gethostbyname(socket.gethostname())

# Flask server URL
server_url = f"http://{local_ip}:5000/qr-data"  # Update with your server's IP address and port

def open_serial_port(port):
    return serial.Serial(port, baudrate=9600, timeout=1)

def detect_qr_scanner():
    # List all available serial ports
    available_ports = list_ports.comports()

    print("Available Ports:")
    for idx, port in enumerate(available_ports):
        print(f"{idx + 1}. Name: {port.name}, Description: {port.description}")

    # Manually select the port where the QR scanner is connected
    selected_index = input("Enter the index of the port where the QR scanner is connected: ")

    try:
        selected_index = int(selected_index) - 1
        selected_port = available_ports[selected_index].device

        # Open the selected serial port
        ser = open_serial_port(selected_port)

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

    except (ValueError, IndexError):
        print("Invalid index. Please enter a valid index.")

if __name__ == "__main__":
    detect_qr_scanner()
