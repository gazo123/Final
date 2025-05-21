import socket
import json
import os

HOST = "100.88.231.34"  # Tailscale IP of this machine here
PORT_SHARE = 9001
SAVE_FILE = "received_shares.json"


def start_foreign_server():
    print(f"[+] Starting Foreign Server 1 at {HOST}:{PORT_SHARE}")
    
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT_SHARE))
        server_socket.listen(5)
        print("[*] Waiting for connection from Relay...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[>] Connection from {addr}")
                data = conn.recv(4096)
                
                if not data:
                    print("[!] No data received.")
                    continue
                
                try:
                    share_data = json.loads(data.decode())
                    print(f"[+] Received share data: {share_data}")

                    # Save to file (append if already exists)
                    if os.path.exists(SAVE_FILE):
                        with open(SAVE_FILE, "r") as f:
                            existing = json.load(f)
                    else:
                        existing = {}

                    existing.update(share_data)

                    with open(SAVE_FILE, "w") as f:
                        json.dump(existing, f, indent=4)

                    print(f"[+] Saved to {SAVE_FILE}")
                
                except json.JSONDecodeError:
                    print("[!] Received invalid JSON.")

if __name__ == "__main__":
    start_foreign_server()
