# sshnotworking.py

import json
import os
import datetime

SSH_FAILURE_LOG = "ssh_not_working.json"

def log_ssh_failure(ip, reason="Unknown Error"):
    log_entry = {
        "ip": ip,
        "reason": reason,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(SSH_FAILURE_LOG):
        try:
            with open(SSH_FAILURE_LOG, "r") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(SSH_FAILURE_LOG, "w") as f:
        json.dump(logs, f, indent=4)

def get_ssh_failures():
    if os.path.exists(SSH_FAILURE_LOG):
        with open(SSH_FAILURE_LOG, "r") as f:
            return json.load(f)
    return []
