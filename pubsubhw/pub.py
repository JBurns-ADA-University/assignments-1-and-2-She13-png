import csv
import time
from google.cloud import pubsub_v1

projid = "silver-script-482812-u0"
email = "sheinlyna13"
levels = ["INFO", "WARN", "ERROR", "DEBUG", "ALERT"]
pub = pubsub_v1.PublisherClient()
tops = {
    lvl: pub.topic_path(projid, f"{lvl}-{email}")
    for lvl in levels
}
print("Pub started.")
try:
    while True:
        f = open("logs.csv", "r", encoding="utf-8")
        rdr = csv.reader(f)
        for row in rdr:
                ts = row[0]
                lvl = row[1].strip()
                msg = row[2].strip()
                if lvl not in tops:
                    continue
                pub.publish(tops[lvl], msg.encode("utf-8"))
                print(f"[pub] {lvl}: {msg}")
                time.sleep(2)

except KeyboardInterrupt:
     print("interrupted")         