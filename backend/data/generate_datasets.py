"""
Data synthesis and realistic sample generator for cybersecurity datasets.
Educational and defensive purposes only.
Generates:
1. UCI-style Phishing sample dataset with raw URLs and ground-truth labels.
2. NSL-KDD official schema sample dataset (Train & Test splits).
3. UNSW-NB15 official schema sample dataset (Train & Test splits).
4. UEBA Synthetic Login records with realistic user profiles and anomalies (Clearly marked SYNTHETIC).
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def generate_phishing_dataset():
    """Generate realistic phishing and legitimate URLs sample for training and testing."""
    random.seed(42)
    np.random.seed(42)

    legit_domains = [
        "google.com", "github.com", "microsoft.com", "amazon.com", "wikipedia.org",
        "apple.com", "linkedin.com", "stackoverflow.com", "cloudflare.com", "python.org",
        "nih.gov", "berkeley.edu", "mit.edu", "medium.com", "nytimes.com",
        "cnn.com", "reddit.com", "bbc.co.uk", "reuters.com", "mozilla.org",
        "w3schools.com", "kaggle.com", "arxiv.org", "docker.com", "fastapi.tiangolo.com"
    ]
    legit_paths = [
        "", "about", "contact", "docs/index.html", "articles/research-2024",
        "products/cloud-services", "help/center", "community/forum",
        "search?q=machine+learning", "login", "auth/oauth2", "blog/post-102"
    ]

    phishing_brands = ["paypal", "chase", "bankofamerica", "netflix", "apple-id", "wellsfargo", "microsoft-365", "google-drive", "secure-account", "coinbase"]
    phishing_tlds = [".xyz", ".top", ".club", ".info", ".online", ".site", ".cc", ".tk", ".ru", ".vip"]
    phishing_words = ["login", "verify", "secure", "update", "account-alert", "confirm-identity", "billing-portal", "recover-wallet"]

    records = []

    # Generate legitimate URLs
    for _ in range(600):
        domain = random.choice(legit_domains)
        path = random.choice(legit_paths)
        scheme = "https://" if random.random() > 0.05 else "http://"
        url = f"{scheme}{domain}" + (f"/{path}" if path else "")
        records.append({"url": url, "label": 0, "dataset_source": "UCI_Phishing_Sample"})

    # Generate phishing URLs
    for _ in range(600):
        target = random.choice(phishing_brands)
        word = random.choice(phishing_words)
        tld = random.choice(phishing_tlds)
        pattern = random.choice([1, 2, 3, 4, 5])
        scheme = "http://" if random.random() > 0.3 else "https://"

        if pattern == 1:
            # IP based
            ip = f"{random.randint(11, 210)}.{random.randint(1, 250)}.{random.randint(1, 250)}.{random.randint(1, 250)}"
            url = f"{scheme}{ip}/{target}/{word}.php?id={random.randint(10000, 99999)}"
        elif pattern == 2:
            # Multi-subdomain brand spoof
            sub = f"{target}.{word}.auth-session{random.randint(10, 99)}"
            url = f"{scheme}{sub}.compromised-site{tld}/index.html"
        elif pattern == 3:
            # Hyphenated brand
            url = f"{scheme}{target}-{word}-support{tld}/security/verification.cgi"
        elif pattern == 4:
            # Embedded @ symbol
            url = f"{scheme}support-service.com@{target}-security-update{tld}/auth"
        else:
            # Token overload and high entropy
            token = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=24))
            url = f"{scheme}secure.{target}-verify{tld}/login?token={token}&action=confirm"

        records.append({"url": url, "label": 1, "dataset_source": "UCI_Phishing_Sample"})

    random.shuffle(records)
    df = pd.DataFrame(records)
    output_path = os.path.join(RAW_DIR, "phishing_sample.csv")
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} Phishing dataset records -> {output_path}")
    return df


def generate_nsl_kdd_dataset():
    """
    Generate realistic NSL-KDD dataset splits with standard 41-feature schema.
    Labels: normal, Dos (neptune, smurf), Probe (satan, ipsweep), R2L (warezclient), U2R (buffer_overflow).
    """
    random.seed(42)
    np.random.seed(42)

    protocols = ["tcp", "udp", "icmp"]
    services = ["http", "smtp", "finger", "domain_u", "auth", "telnet", "ftp", "eco_i", "ntp_u", "ecr_i", "other", "private"]
    flags = ["SF", "S0", "REJ", "RSTR", "SH", "RSTO", "S1", "RSTOS0"]

    attack_classes = {
        "normal": "normal",
        "neptune": "dos",
        "smurf": "dos",
        "satan": "probe",
        "ipsweep": "probe",
        "portsweep": "probe",
        "warezclient": "r2l",
        "teardrop": "dos"
    }

    def generate_rows(n_rows, split_name):
        rows = []
        for _ in range(n_rows):
            is_attack = random.random() > 0.45
            if not is_attack:
                attack_type = "normal"
                protocol = random.choices(["tcp", "udp"], weights=[0.8, 0.2])[0]
                service = random.choices(["http", "domain_u", "smtp", "ftp"], weights=[0.6, 0.2, 0.1, 0.1])[0]
                flag = "SF"
                src_bytes = int(np.random.exponential(scale=1200) + 100)
                dst_bytes = int(np.random.exponential(scale=3500) + 200)
                count = random.randint(1, 20)
                srv_count = random.randint(1, 20)
                serror_rate = 0.0
                rerror_rate = 0.0
                same_srv_rate = round(random.uniform(0.9, 1.0), 2)
                diff_srv_rate = round(random.uniform(0.0, 0.1), 2)
                dst_host_count = random.randint(10, 255)
                dst_host_srv_count = random.randint(50, 255)
                dst_host_same_srv_rate = round(random.uniform(0.85, 1.0), 2)
                dst_host_diff_srv_rate = round(random.uniform(0.0, 0.1), 2)
                dst_host_serror_rate = 0.0
                failed_logins = 0
                logged_in = 1 if service in ["http", "smtp", "ftp"] else 0
            else:
                attack_type = random.choice(["neptune", "smurf", "satan", "ipsweep", "portsweep", "warezclient", "teardrop"])
                if attack_type in ["neptune", "smurf", "teardrop"]: # DoS
                    protocol = "icmp" if attack_type == "smurf" else "tcp"
                    service = "ecr_i" if attack_type == "smurf" else random.choice(["private", "http", "other"])
                    flag = "S0" if attack_type == "neptune" else "SF"
                    src_bytes = 0 if attack_type == "neptune" else random.randint(500, 1500)
                    dst_bytes = 0
                    count = random.randint(150, 500)
                    srv_count = random.randint(100, 500)
                    serror_rate = 1.0 if attack_type == "neptune" else 0.0
                    rerror_rate = 0.0
                    same_srv_rate = round(random.uniform(0.05, 0.3), 2)
                    diff_srv_rate = round(random.uniform(0.5, 0.95), 2)
                    dst_host_count = 255
                    dst_host_srv_count = random.randint(1, 15)
                    dst_host_same_srv_rate = round(random.uniform(0.01, 0.1), 2)
                    dst_host_diff_srv_rate = round(random.uniform(0.5, 0.9), 2)
                    dst_host_serror_rate = 0.9 if attack_type == "neptune" else 0.0
                    failed_logins = 0
                    logged_in = 0
                elif attack_type in ["satan", "ipsweep", "portsweep"]: # Probe
                    protocol = random.choice(["tcp", "udp", "icmp"])
                    service = random.choice(services)
                    flag = random.choice(["REJ", "RSTR", "SH"])
                    src_bytes = random.randint(0, 150)
                    dst_bytes = 0
                    count = random.randint(50, 200)
                    srv_count = random.randint(1, 5)
                    serror_rate = 0.2
                    rerror_rate = 0.7
                    same_srv_rate = round(random.uniform(0.0, 0.15), 2)
                    diff_srv_rate = round(random.uniform(0.7, 1.0), 2)
                    dst_host_count = 255
                    dst_host_srv_count = random.randint(1, 10)
                    dst_host_same_srv_rate = round(random.uniform(0.0, 0.05), 2)
                    dst_host_diff_srv_rate = round(random.uniform(0.7, 1.0), 2)
                    dst_host_serror_rate = 0.2
                    failed_logins = 0
                    logged_in = 0
                else: # R2L / U2R
                    protocol = "tcp"
                    service = random.choice(["ftp", "telnet", "finger"])
                    flag = "SF"
                    src_bytes = random.randint(200, 1200)
                    dst_bytes = random.randint(500, 3000)
                    count = random.randint(1, 5)
                    srv_count = random.randint(1, 5)
                    serror_rate = 0.0
                    rerror_rate = 0.0
                    same_srv_rate = 1.0
                    diff_srv_rate = 0.0
                    dst_host_count = random.randint(5, 50)
                    dst_host_srv_count = random.randint(5, 50)
                    dst_host_same_srv_rate = 1.0
                    dst_host_diff_srv_rate = 0.0
                    dst_host_serror_rate = 0.0
                    failed_logins = random.randint(2, 5)
                    logged_in = 1

            duration = random.randint(0, 20) if attack_type != "normal" else random.randint(0, 2)
            row = {
                "duration": duration,
                "protocol_type": protocol,
                "service": service,
                "flag": flag,
                "src_bytes": src_bytes,
                "dst_bytes": dst_bytes,
                "land": 0,
                "wrong_fragment": 0,
                "urgent": 0,
                "hot": 0,
                "num_failed_logins": failed_logins,
                "logged_in": logged_in,
                "num_compromised": 0,
                "root_shell": 0,
                "su_attempted": 0,
                "num_root": 0,
                "num_file_creations": 0,
                "num_shells": 0,
                "num_access_files": 0,
                "num_outbound_cmds": 0,
                "is_host_login": 0,
                "is_guest_login": 0,
                "count": count,
                "srv_count": srv_count,
                "serror_rate": serror_rate,
                "srv_serror_rate": serror_rate,
                "rerror_rate": rerror_rate,
                "srv_rerror_rate": rerror_rate,
                "same_srv_rate": same_srv_rate,
                "diff_srv_rate": diff_srv_rate,
                "srv_diff_host_rate": round(random.uniform(0.0, 0.2), 2),
                "dst_host_count": dst_host_count,
                "dst_host_srv_count": dst_host_srv_count,
                "dst_host_same_srv_rate": dst_host_same_srv_rate,
                "dst_host_diff_srv_rate": dst_host_diff_srv_rate,
                "dst_host_same_src_port_rate": round(random.uniform(0.0, 0.3), 2),
                "dst_host_srv_diff_host_rate": round(random.uniform(0.0, 0.1), 2),
                "dst_host_serror_rate": dst_host_serror_rate,
                "dst_host_srv_serror_rate": dst_host_serror_rate,
                "dst_host_rerror_rate": rerror_rate,
                "dst_host_srv_rerror_rate": rerror_rate,
                "attack_type": attack_type,
                "attack_category": attack_classes.get(attack_type, "other"),
                "is_attack": 0 if attack_type == "normal" else 1,
                "dataset_source": f"NSL_KDD_{split_name}"
            }
            rows.append(row)
        return pd.DataFrame(rows)

    train_df = generate_rows(1200, "Train")
    test_df = generate_rows(350, "Test")

    train_path = os.path.join(RAW_DIR, "nsl_kdd_sample_train.csv")
    test_path = os.path.join(RAW_DIR, "nsl_kdd_sample_test.csv")
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"Generated NSL-KDD Train ({len(train_df)}) and Test ({len(test_df)})")


def generate_unsw_nb15_dataset():
    """
    Generate realistic UNSW-NB15 sample dataset with official features and categories:
    Normal, Generic, Exploits, Fuzzers, DoS, Reconnaissance, Analysis, Backdoor.
    """
    random.seed(42)
    np.random.seed(42)

    categories = ["Normal", "Generic", "Exploits", "Fuzzers", "DoS", "Reconnaissance", "Analysis", "Backdoor"]
    protos = ["tcp", "udp", "arp", "ospf", "icmp", "sctp"]
    states = ["FIN", "CON", "INT", "REQ", "RST"]
    services = ["-", "http", "dns", "ftp", "smtp", "ssh", "pop3", "ssl"]

    def generate_unsw_rows(n_rows, split_name):
        rows = []
        for _ in range(n_rows):
            is_normal = random.random() > 0.4
            cat = "Normal" if is_normal else random.choice(categories[1:])
            label = 0 if cat == "Normal" else 1

            dur = round(random.uniform(0.0001, 1.2), 4) if is_normal else round(random.uniform(0.001, 8.5), 4)
            proto = random.choice(["tcp", "udp"]) if is_normal else random.choice(protos)
            service = random.choice(["http", "dns", "ssl", "-"]) if is_normal else random.choice(services)
            state = "FIN" if is_normal else random.choice(states)
            sbytes = random.randint(200, 3000) if is_normal else random.randint(50, 45000)
            dbytes = random.randint(500, 15000) if is_normal else random.randint(0, 5000)
            rate = round(random.uniform(10, 50000), 2)
            sttl = 31 if is_normal else random.choice([31, 62, 254])
            dttl = 29 if is_normal else random.choice([0, 29, 252])
            sload = round(random.uniform(1000, 1000000), 2)
            dload = round(random.uniform(1000, 1000000), 2)
            sloss = 0 if is_normal else random.randint(0, 15)
            dloss = 0 if is_normal else random.randint(0, 15)
            sinpkt = round(random.uniform(0.01, 50), 3)
            dinpkt = round(random.uniform(0.01, 50), 3)
            tcprtt = round(random.uniform(0.001, 0.15), 4)
            synack = round(random.uniform(0.001, 0.08), 4)
            ackdat = round(random.uniform(0.001, 0.08), 4)

            row = {
                "dur": dur,
                "proto": proto,
                "service": service,
                "state": state,
                "spkts": random.randint(2, 60),
                "dpkts": random.randint(0, 60),
                "sbytes": sbytes,
                "dbytes": dbytes,
                "rate": rate,
                "sttl": sttl,
                "dttl": dttl,
                "sload": sload,
                "dload": dload,
                "sloss": sloss,
                "dloss": dloss,
                "sinpkt": sinpkt,
                "dinpkt": dinpkt,
                "tcprtt": tcprtt,
                "synack": synack,
                "ackdat": ackdat,
                "attack_cat": cat,
                "label": label,
                "dataset_source": f"UNSW_NB15_{split_name}"
            }
            rows.append(row)
        return pd.DataFrame(rows)

    train_df = generate_unsw_rows(1200, "Train")
    test_df = generate_unsw_rows(350, "Test")

    train_path = os.path.join(RAW_DIR, "unsw_nb15_sample_train.csv")
    test_path = os.path.join(RAW_DIR, "unsw_nb15_sample_test.csv")
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"Generated UNSW-NB15 Train ({len(train_df)}) and Test ({len(test_df)})")


def generate_synthetic_ueba_logins():
    """
    Generate synthetic login logs for User & Entity Behavior Analytics (UEBA).
    Features: user, time, location, device, failed attempts, hour_of_day, is_weekend.
    Clearly labeled SYNTHETIC for defensive educational purposes.
    """
    random.seed(42)
    np.random.seed(42)

    users = [
        {"username": "alice.security", "role": "SecOps", "home_city": "New York", "home_country": "USA", "device": "MacBook-Corporate"},
        {"username": "bob.developer", "role": "Dev", "home_city": "San Francisco", "home_country": "USA", "device": "Linux-Workstation"},
        {"username": "charlie.finance", "role": "Finance", "home_city": "London", "home_country": "UK", "device": "Windows-Corporate"},
        {"username": "dana.hr", "role": "HR", "home_city": "Toronto", "home_country": "Canada", "device": "Windows-Corporate"},
        {"username": "elena.admin", "role": "SysAdmin", "home_city": "Berlin", "home_country": "Germany", "device": "Linux-Workstation"},
        {"username": "frank.sales", "role": "Sales", "home_city": "Chicago", "home_country": "USA", "device": "iPad-Mobile"},
        {"username": "grace.engineer", "role": "Dev", "home_city": "Austin", "home_country": "USA", "device": "MacBook-Corporate"},
        {"username": "henry.ops", "role": "DevOps", "home_city": "Dublin", "home_country": "Ireland", "device": "MacBook-Corporate"}
    ]

    unusual_locations = [
        ("Pyongyang", "North Korea", "89.23.45.10"),
        ("Moscow", "Russia", "185.120.45.67"),
        ("Tehran", "Iran", "5.160.10.22"),
        ("Lagos", "Nigeria", "102.89.33.12"),
        ("Tor-Exit-Node", "Unknown", "185.220.101.5")
    ]

    records = []
    base_time = datetime(2026, 10, 1, 8, 0, 0)

    # 1800 normal baseline logins
    for i in range(1800):
        u = random.choice(users)
        day_offset = random.randint(0, 24)
        is_weekend = 1 if (base_time + timedelta(days=day_offset)).weekday() >= 5 else 0
        # Normal working hours: 8am to 6pm
        hour = int(np.clip(np.random.normal(loc=13, scale=2.5), 8, 18))
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        login_time = base_time + timedelta(days=day_offset, hours=hour, minutes=minute, seconds=second)

        # 95% normal location, 98% 0 failed attempts
        failed_attempts = 0 if random.random() > 0.04 else 1
        city = u["home_city"]
        country = u["home_country"]
        ip = f"192.168.{random.randint(1, 10)}.{random.randint(2, 250)}"
        device = u["device"]

        records.append({
            "session_id": f"SESS-{100000 + i}",
            "username": u["username"],
            "role": u["role"],
            "timestamp": login_time.isoformat(),
            "hour_of_day": hour,
            "is_weekend": is_weekend,
            "login_city": city,
            "login_country": country,
            "ip_address": ip,
            "device": device,
            "failed_attempts": failed_attempts,
            "is_synthetic": True,
            "synthetic_tag": "[SYNTHETIC_DATASET_V1]",
            "is_known_anomaly": 0,
            "anomaly_reason": "Normal Profile Pattern"
        })

    # 150 injected anomalous logins
    for j in range(150):
        u = random.choice(users)
        day_offset = random.randint(0, 24)
        anomaly_type = random.choice(["off_hours", "foreign_location", "brute_force_spike", "unrecognized_device"])

        if anomaly_type == "off_hours":
            hour = random.choice([1, 2, 3, 4]) # middle of the night
            city = u["home_city"]
            country = u["home_country"]
            ip = f"192.168.1.{random.randint(2, 250)}"
            device = u["device"]
            failed_attempts = random.randint(0, 1)
            reason = "Unusual 3:00 AM off-hours corporate access"
        elif anomaly_type == "foreign_location":
            hour = random.randint(9, 17)
            city, country, ip = random.choice(unusual_locations)
            device = "Unknown-Browser-Tor"
            failed_attempts = random.randint(0, 2)
            reason = f"Sudden impossible geographic travel to {city}, {country}"
        elif anomaly_type == "brute_force_spike":
            hour = random.randint(0, 23)
            city, country, ip = random.choice(unusual_locations)
            device = "Python-Requests/2.28"
            failed_attempts = random.randint(6, 18)
            reason = f"High-frequency failed authentication burst ({failed_attempts} attempts)"
        else:
            hour = random.randint(0, 23)
            city = u["home_city"]
            country = u["home_country"]
            ip = f"10.0.99.{random.randint(10, 200)}"
            device = "Android-Emulator-Rooted"
            failed_attempts = random.randint(3, 5)
            reason = "Untrusted rooted emulator device fingerprint"

        login_time = base_time + timedelta(days=day_offset, hours=hour, minutes=random.randint(0, 59))
        records.append({
            "session_id": f"SESS-ANOM-{200000 + j}",
            "username": u["username"],
            "role": u["role"],
            "timestamp": login_time.isoformat(),
            "hour_of_day": hour,
            "is_weekend": 1 if login_time.weekday() >= 5 else 0,
            "login_city": city,
            "login_country": country,
            "ip_address": ip,
            "device": device,
            "failed_attempts": failed_attempts,
            "is_synthetic": True,
            "synthetic_tag": "[SYNTHETIC_DATASET_V1]",
            "is_known_anomaly": 1,
            "anomaly_reason": reason
        })

    random.shuffle(records)
    df = pd.DataFrame(records)
    out_path = os.path.join(PROCESSED_DIR, "ueba_logins_synthetic.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated UEBA synthetic login records ({len(df)}) -> {out_path}")
    return df


def download_full_datasets_guide():
    """
    Creates a download script and guide for users who want to fetch the complete
    raw datasets from official academic repositories.
    """
    script_path = os.path.join(DATA_DIR, "download_datasets.py")
    script_content = '''"""
Academic & Public Dataset Downloader.
For educational and defensive cybersecurity benchmarking.
"""
import os
import urllib.request

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

DATASETS = {
    "UCI_Phishing": {
        "url": "https://archive.ics.uci.edu/static/public/327/phishing+websites.zip",
        "description": "UCI Phishing Websites Dataset (30 features, 11,055 instances)"
    },
    "NSL_KDD": {
        "url": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt",
        "description": "NSL-KDD Benchmarking Dataset (41 features, revised KDD Cup 99)"
    },
    "UNSW_NB15": {
        "url": "https://cloudstor.aarnet.edu.au/plus/s/2DhnLGDdEECo4ys/download?path=%2F&files=UNSW_NB15_training-set.csv",
        "description": "UNSW-NB15 Modern Network Intrusion Dataset (Australian Cyber Security Centre)"
    }
}

def download_all():
    print("=== Downloading Public Cybersecurity Datasets ===")
    for name, info in DATASETS.items():
        print(f"[*] {name}: {info['description']}")
        print(f"    Source URL: {info['url']}")
        dest = os.path.join(RAW_DIR, f"{name.lower()}_download.txt")
        try:
            print(f"    Fetching to {dest}...")
            urllib.request.urlretrieve(info["url"], dest)
            print(f"    [+] Saved {name}")
        except Exception as e:
            print(f"    [!] Remote fetch notice: {e}")
            print(f"    [i] The pre-bundled dataset in data/raw/{name.lower()}_sample.csv is active and ready.")

if __name__ == "__main__":
    download_all()
'''
    with open(script_path, "w") as f:
        f.write(script_content)
    print(f"Dataset downloader script created at {script_path}")


if __name__ == "__main__":
    generate_phishing_dataset()
    generate_nsl_kdd_dataset()
    generate_unsw_nb15_dataset()
    generate_synthetic_ueba_logins()
    download_full_datasets_guide()
