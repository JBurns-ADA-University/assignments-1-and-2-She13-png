from google.cloud import pubsub_v1

PROJECT_ID = "inft-6000"
EMAIL_SUFFIX = "sheinlyna13"
TOPICS = ["INFO", "WARN", "ERROR", "DEBUG", "ALERT"]

publisher = pubsub_v1.PublisherClient()

def delete_topics():
    for level in TOPICS:
        topic_name = f"{level}-{EMAIL_SUFFIX}"
        topic_path = publisher.topic_path(PROJECT_ID, topic_name)
        try:
            publisher.delete_topic(topic=topic_path)
            print(f"Deleted topic: {topic_name}")
        except Exception as e:
            print(f"Could not delete topic {topic_name}: {e}")

if __name__ == "__main__":
    delete_topics()
