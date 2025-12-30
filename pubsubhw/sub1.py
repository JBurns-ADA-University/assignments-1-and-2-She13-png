import yaml
import time
import re
from google.cloud import pubsub_v1
projid = "silver-script-482812-u0"
email = "sheinlyna13"
subid = "1"     
reload_sec = 10
levels = ["INFO", "WARN", "ERROR", "DEBUG", "ALERT"]
sub = pubsub_v1.SubscriberClient()
subs = {
    lvl: sub.subscription_path(projid, f"{lvl}-{email}-sub")
    for lvl in levels
}
rules = []
last_load = 0
def load_rules():
    global rules, last_load
    f = open("rules.yaml")
    data = yaml.safe_load(f)
    rules = data["subscribers"].get(subid, [])
    last_load = time.time()
    print(f"[sub{subid}] rules loaded")
print("sub id", subid, "started.")
def need_reload():
    return time.time() - last_load > reload_sec
def mk_cb(lvl):
    def cb(msg):
        if need_reload():
            load_rules()

        txt = msg.data.decode()

        for r in rules:
            if r["level"] == lvl and re.search(r["pattern"], txt):
                print(f"[sub{subid}] {lvl}: {txt}")
                break

        msg.ack()
    return cb
def run_sub():
    load_rules()
    streaming_futures = []
    for lvl in levels:
        future = sub.subscribe(subs[lvl], callback=mk_cb(lvl))
        streaming_futures.append(future)

    print(f"[sub{subid}] listening.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\ninterrupted")
        for future in streaming_futures:
            future.cancel()

if __name__ == "__main__":
    run_sub()