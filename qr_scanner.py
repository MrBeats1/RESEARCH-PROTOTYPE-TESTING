import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import requests  # Import the requests library

# Flask server URL
server_url = "http://192.168.1.2:5000/qr-data"  # Update with your server's IP address

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    decoded_objects = decode(frame, symbols=[ZBarSymbol.QRCODE])
    
    for obj in decoded_objects:
        qr_code_data = obj.data.decode('utf-8')
        print(f"QR Code Data: {qr_code_data}")

        # Send QR code data to Flask server
        try:
            response = requests.post(server_url, json={'qrCodeData': qr_code_data})
            print(f"Server Response: {response.json()}")
        except requests.RequestException as e:
            print(f"Error sending data to server: {e}")

    cv2.imshow("big balls", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
