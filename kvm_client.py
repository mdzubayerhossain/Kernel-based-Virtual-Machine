import socket
import pickle
import pyautogui

# Network configuration
SERVER_IP = '192.168.1.104'  # Replace with the server's IP address
PORT = 5000

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f"Connected to server at {SERVER_IP}:{PORT}")

# Handle received events
def handle_event(data):
    event_type = data['type']
    event_data = data['data']
    
    if event_type == 'key_press':
        pyautogui.typewrite(event_data)
    elif event_type == 'key_release':
        pass  # Optional: Handle key release if needed
    elif event_type == 'mouse_move':
        pyautogui.moveTo(event_data[0], event_data[1])
    elif event_type == 'mouse_click':
        if event_data['pressed']:
            pyautogui.click(event_data['x'], event_data['y'], button=event_data['button'])
        else:
            pyautogui.mouseUp(button=event_data['button'])
    elif event_type == 'mouse_scroll':
        pyautogui.scroll(event_data['dy'])

# Main loopKey.downKey.up
try:
    while True:
        data = client_socket.recv(4096)
        if data:
            event = pickle.loads(data)
            handle_event(event)
except KeyboardInterrupt:
    print("Stopping client...")
    client_socket.close()
