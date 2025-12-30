# Google Cloud Pub/Sub Log Streaming Project
# Youtube Link: https://youtu.be/7Wjg2yfKs1U

# Overview: This project demonstrates a real-time log streaming system using Google Cloud Pub/Sub.  
We created:
# 1. 
A **publisher script** (`pub.py`) that reads log messages from `logs.csv` and publishes them to topics categorized by log levels (INFO, WARN, ERROR, DEBUG, ALERT).  
# 2.
Multiple **subscriber scripts** (`sub0.py`, `sub1.py`, etc.) that listen to specific subscriptions, filter messages dynamically based on rules defined in `rules.yaml`, and print matching log entries.  
# 3.
Automation scripts (`script.py`) to **setup** and **teardown** all Pub/Sub topics and subscriptions easily.
# Bonus
I Implemented automation for creating and deleting topics and subscriptions with a single script, using command-line arguments (`setup` and `teardown`).
