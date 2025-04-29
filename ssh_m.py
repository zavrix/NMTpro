# ssh_m.py

import paramiko

def ssh_get_stats(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, timeout=5)

        stdin, stdout, stderr = client.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
        cpu_usage = float(stdout.read().decode().strip())

        stdin, stdout, stderr = client.exec_command("cat /proc/net/dev")
        net_data = stdout.read().decode()

        upload = download = 0
        for line in net_data.splitlines():
            if ":" in line:
                parts = line.split()
                download += int(parts[1])
                upload += int(parts[9])

        client.close()

        upload = round(upload / 1024, 2)
        download = round(download / 1024, 2)

        return cpu_usage, upload, download

    except Exception as e:
        print(f"[SSH ERROR] {ip}: {e}")
        return None, None, None
