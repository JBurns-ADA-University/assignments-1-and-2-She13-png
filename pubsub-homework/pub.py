import time
import csv
from google.cloud import pubsub_v1

PROJECT_ID = "inft-6000"
UNIQUE_ID = "sheinlyna13"

LOGS_FILE = "logs.csv"
LEVELS = ["INFO", "WARN", "ERROR", "DEBUG", "ALERT"]

def main():
    publisher = pubsub_v1.PublisherClient()

    topic_paths = {
        level: publisher.topic_path(PROJECT_ID, f"{level}-{UNIQUE_ID}")
        for level in LEVELS
    }


    logs = []
    with open(LOGS_FILE, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            logs.append((row[0].strip(), row[1].strip()))

    index = 0
    while True:
        level, message = logs[index % len(logs)]
        index += 1

        if level in topic_paths:
            publisher.publish(
                topic_paths[level],
                message.encode("utf-8"),
                level=level
            )
            print(f"[PUBLISHER] {level}: {message}")

        time.sleep(2)

if __name__ == "__main__":
    main()

