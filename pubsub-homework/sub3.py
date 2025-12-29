import time
import yaml
import re
from threading import Thread
from google.cloud import pubsub_v1

PROJECT_ID = "inft-6000"
UNIQUE_ID = "sheinlyna13"
SUBSCRIBER_ID = "3"

RULES_FILE = "rules.yaml"
RELOAD_INTERVAL = 10

compiled_rules = {}

def load_rules():
    global compiled_rules
    with open(RULES_FILE) as f:
        data = yaml.safe_load(f)

    rules = data["subscribers"].get(SUBSCRIBER_ID, [])
    compiled_rules = {}

    for rule in rules:
        level = rule["level"]
        pattern = re.compile(rule["pattern"])
        compiled_rules.setdefault(level, []).append(pattern)

    print(f"[Sub {SUBSCRIBER_ID}] rules reloaded")

def reload_loop():
    while True:
        load_rules()
        time.sleep(RELOAD_INTERVAL)

def callback(message):
    level = message.attributes.get("level")
    text = message.data.decode("utf-8")

    for pattern in compiled_rules.get(level, []):
        if pattern.search(text):
            print(f"[Sub {SUBSCRIBER_ID}] MATCH {level}: {text}")
            break

    message.ack()

def main():
    load_rules()
    subscriber = pubsub_v1.SubscriberClient()

    subscriptions = []

    for level in compiled_rules.keys():
        topic = f"{level}-{UNIQUE_ID}"
        sub_name = f"sub-{SUBSCRIBER_ID}-{level}-{UNIQUE_ID}"

        topic_path = subscriber.topic_path(PROJECT_ID, topic)
        sub_path = subscriber.subscription_path(PROJECT_ID, sub_name)

        try:
            subscriber.create_subscription(name=sub_path, topic=topic_path)
        except Exception:
            pass

        subscriptions.append(sub_path)

    Thread(target=reload_loop, daemon=True).start()

    for sub in subscriptions:
        subscriber.subscribe(sub, callback)
        print(f"[Subscriber {SUBSCRIBER_ID}] Listening on {sub}")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
