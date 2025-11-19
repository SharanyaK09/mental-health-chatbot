# keep_alive.py
import threading
import time
import requests
import os

def keep_alive():
    # use your Render URL or environment var
    url = os.environ.get("KEEP_ALIVE_URL", "https://mental-health-chatbot-2-py14.onrender.com")
    while True:
        try:
            requests.get(url, timeout=10)
            print("Pinged:", url)
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(240)  # every 4 minutes

def start_keep_alive():
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
