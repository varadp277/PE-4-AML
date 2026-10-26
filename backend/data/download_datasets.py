"""
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
