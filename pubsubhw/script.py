import sys
from google.cloud import pubsub_v1
projid = "silver-script-482812-u0"
email = "sheinlyna13"
levels = ["INFO", "WARN", "ERROR", "DEBUG", "ALERT"]
subids = ["0", "1", "2", "3"]
pub = pubsub_v1.PublisherClient()
sub = pubsub_v1.SubscriberClient()
def setup():
    for lvl in levels:
        topic = pub.topic_path(projid, f"{lvl}-{email}")
        try:
            pub.create_topic(name=topic)
            print(f"topic created: {lvl}-{email}")
        except Exception:
            print(f"topic exist: {lvl}-{email}")

    for subid in subids:
        for lvl in levels:
            sub_name = sub.subscription_path(projid, f"{lvl}-{email}-sub-{subid}")
            topic = pub.topic_path(projid, f"{lvl}-{email}")
            try:
                sub.create_subscription(name=sub_name, topic=topic)
                print(f"sub created: {lvl}-{email}-sub-{subid}")
            except Exception:
                print(f"sub exists: {lvl}-{email}-sub-{subid}")

def teardown():
    for subid in subids:
        for lvl in levels:
            sub_name = sub.subscription_path(projid, f"{lvl}-{email}-sub-{subid}")
            try:
                sub.delete_subscription(subscription=sub_name)
                print(f"sub deleted: {lvl}-{email}-sub-{subid}")
            except Exception as e:
                print(f"error sub deleting {lvl}-{email}-sub-{subid}: {e}")

    for lvl in levels:
        topic = pub.topic_path(projid, f"{lvl}-{email}")
        try:
            pub.delete_topic(topic=topic)
            print(f"top deleted: {lvl}-{email}")
        except Exception as e:
            print(f"error top deleting {lvl}-{email}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["setup", "teardown"]:
        print("setup|teardown")
        sys.exit(1)

    if sys.argv[1] == "setup":
        setup()
    else:
        teardown()
