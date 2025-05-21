import socket
import json
import time
# ---------------- FOREIGN_SERVERS ----------------
FOREIGN_SERVERS = {
    1: "100.88.231.34",
    2: "100.88.74.36",
    3: "100.88.74.38"
}

RECEIVE_PORT = 8000  # Listen for sharelists here
BASE_SEND_PORT = 9000  # FS1 → 9001, FS2 → 9002, FS3 → 9003
BUFFER_SIZE = 4096

# --------------- Helpers ----------------
def send_to_foreign_server(server_id, message_dict):
    ip = FOREIGN_SERVERS.get(server_id)
    port = BASE_SEND_PORT + server_id

    if not ip:
        print(f"[!] No IP found for server ID {server_id}")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            serialized_msg = json.dumps(message_dict)
            s.sendall(serialized_msg.encode())
            print(f"[+] Sent to FS{server_id} at {ip}:{port}")
    except Exception as e:
        print(f"[!] Error sending to FS{server_id} — {e}")

# --------------- Main Server ----------------
def start_relay_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(('', RECEIVE_PORT))
        server_sock.listen()
        print(f"[~] Relay listening for sharelists on port {RECEIVE_PORT}...")

        while True:
            conn, addr = server_sock.accept()
            with conn:
                print(f"[+] Connection from {addr}")
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    continue

                try:
                    sharelist = json.loads(data.decode())
                    print(f"[>] Received sharelist: {sharelist}")

                    for server_id, share_data in sharelist.items():
                        send_to_foreign_server(int(server_id), share_data)

                except json.JSONDecodeError as je:
                    print(f"[!] JSON error: {je}")
                except Exception as e:
                    print(f"[!] Unexpected error: {e}")
            time.sleep(8)

# --------------- Run ----------------
if __name__ == "__main__":
    start_relay_server()
