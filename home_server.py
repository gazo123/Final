import json
import random
import socket
import time
<<<<<<< Updated upstream
RELAY_IP = "192.168.0.10"  # Replace with relay's Tailscale IP
=======
RELAY_IP = "192.158.0.10"  # Replace with relay's Tailscale IP
>>>>>>> Stashed changes
RELAY_PORT = 8000
SHARE_FILES = ["share_1.json", "share_2.json", "share_3.json"]
USERS_FILE = "users.json"

def register_users():
    print("=== Register 3 Users ===")
    users = {}
    for i in range(3):
        username = input(f"Enter username for user {i+1}: ").strip()
        while True:
            try:
                key = int(input(f"Enter secret key (integer) for {username}: "))
                break
            except ValueError:
                print("Key must be an integer. Try again.")
        users[username] = key

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    print(f"[+] Saved 3 users to {USERS_FILE}")
    return users

def generate_shares(secret, n=3, t=2):
    """
    Generate n shares with threshold t=2 using simplified linear polynomial: f(x) = secret + a*x
    Returns: list of (x, y)
    """
    a = random.randint(1, 9999)
    shares = []
    for x in range(1, n + 1):
        y = secret + a * x
        shares.append((x, y))
    return shares  # list of tuples

def split_keys_and_save_shares(users):
    shares = {1: {}, 2: {}, 3: {}}  # share_1, share_2, share_3

    for username, key in users.items():
        s = generate_shares(key)  # [(1, y1), (2, y2), (3, y3)]
        for i in range(3):
            share_index = s[i][0]
            share_value = s[i][1]
            shares[share_index][username] = share_value

    for i in range(1, 4):
        filename = f"share_{i}.json"
        with open(filename, 'w') as f:              #saving the share file
            json.dump({i: shares[i]}, f, indent=4)
        print(f"[+] Saved {filename}")

def send_share_to_relay(file_path):
    try:
        with open(file_path, 'r') as f:
            share_data = json.load(f)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((RELAY_IP, RELAY_PORT))
            s.sendall(json.dumps(share_data).encode())
            print(f"[>] Sent {file_path} to relay.")
    except Exception as e:
        print(f"[!] Error sending {file_path}: {e}")

def loop_and_send_shares():
    for i in range(3):
        file_name = SHARE_FILES[i]
        send_share_to_relay(file_name)
        if i < 2:
            time.sleep(10)

if __name__ == "__main__":
    users = register_users()
    split_keys_and_save_shares(users)

    loop_and_send_shares()
