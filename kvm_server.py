import socket
import pickle
from pynput import keyboard, mouse

# Network configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}...")
conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

# Input event capture
def send_event(event_type, event_data):
    """Send the input event to the client."""
    data = {'type': event_type, 'data': event_data}
    conn.sendall(pickle.dumps(data))

# Keyboard listener
def on_key_press(key):
    try:
        send_event('key_press', key.char)
    except AttributeError:
        send_event('key_press', str(key))

def on_key_release(key):
    send_event('key_release', str(key))

# Mouse listener
def on_mouse_move(x, y):
    send_event('mouse_move', (x, y))

def on_click(x, y, button, pressed):
    send_event('mouse_click', {'x': x, 'y': y, 'button': str(button), 'pressed': pressed})

def on_scroll(x, y, dx, dy):
    send_event('mouse_scroll', {'dx': dx, 'dy': dy})

# Start listeners
keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

# Keep the server running
try:
    keyboard_listener.join()
    mouse_listener.join()
except KeyboardInterrupt:
    print("Stopping server...")
    conn.close()
    server_socket.close()
