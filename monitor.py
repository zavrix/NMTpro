import platform, subprocess, psutil, time, json, os, datetime
from alert import send_email
from config import GMAIL_RECEIVER as RECIPIENT
from devices import devices

STATUS_FILE = "status.json"
LAST_REPORT_FILE = "last_report.txt"

def ping(ip):
    cmd = ['ping', '-n' if platform.system() == 'Windows' else '-c', '1', ip]
    return subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode == 0

def load_previous_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_current_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)

def should_send_report():
    if os.path.exists(LAST_REPORT_FILE):
        with open(LAST_REPORT_FILE, "r") as f:
            last_time = float(f.read().strip())
            return time.time() - last_time >= 3600  # 1 hour
    return True

def update_last_report_time():
    with open(LAST_REPORT_FILE, "w") as f:
        f.write(str(time.time()))

def generate_html_email(cpu, memory, upload, download, device_statuses):
    rows = ""
    for device in device_statuses:
        status_color = "#4CAF50" if device["status"] == "Online" else "#F44336"
        rows += f"""
            <tr>
                <td>{device['ip']}</td>
                <td style=\"color: {status_color};\">{device['status']}</td>
            </tr>
        """

    return f"""
    <html>
    <body style=\"font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px;\">
        <div style=\"max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 10px;\">
            <h2 style=\"color: #333;\">🌐 Network Monitoring Report</h2>
            <p><strong>🧠 CPU Usage:</strong> {cpu}%</p>
            <p><strong>💾 Memory Usage:</strong> {memory}%</p>
            <p><strong>📤 Upload:</strong> {upload:.2f} KB/s</p>
            <p><strong>📥 Download:</strong> {download:.2f} KB/s</p>

            <h4 style=\"margin-top: 30px;\">📋 Device Statuses</h4>
            <table width=\"100%\" cellpadding=\"10\" cellspacing=\"0\" style=\"border-collapse: collapse;\">
                <thead style=\"background: #333; color: #fff;\">
                    <tr>
                        <th>IP Address</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>

            <p style=\"margin-top: 30px; color: #999;\">Generated automatically by Network Monitor</p>
        </div>
    </body>
    </html>
    """

def get_status_data():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    upload = (net2.bytes_sent - net1.bytes_sent) / 1024
    download = (net2.bytes_recv - net1.bytes_recv) / 1024

    previous_status = load_previous_status()
    current_status = {}
    report_lines = []
    alert_needed = False

    online, offline = 0, 0
    device_statuses = []

    for ip in devices:
        is_online = ping(ip)
        status = "Online" if is_online else "Offline"
        current_status[ip] = status

        if not is_online and previous_status.get(ip) != "Offline":
            alert_needed = True

        if status == "Online":
            online += 1
        else:
            offline += 1

        device_statuses.append({"ip": ip, "status": status})
        report_lines.append(f"{ip} - {status}")

    save_current_status(current_status)

    if alert_needed or should_send_report():
        html_content = generate_html_email(cpu, memory, upload, download, device_statuses)
        send_email("📊 Hourly Network Report", html_content, RECIPIENT, html=True)
        update_last_report_time()

    return {
        "cpu": cpu,
        "memory": memory,
        "upload": round(upload, 2),
        "download": round(download, 2),
        "total": len(devices),
        "online": online,
        "offline": offline,
        "devices": device_statuses
    }
