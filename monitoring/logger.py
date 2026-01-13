import time

def log_event(event):
    event["timestamp"] = time.time()
    with open("logs.txt", "a") as f:
        f.write(str(event) + "\n")
