#!/usr/bin/env python3
import requests
import socket
import sys

def fetch_subdomains(domain):
    print(f"[+] Fetching subdomains for {domain} from crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("[-] Error fetching data from crt.sh")
            return []
        data = response.json()
        subdomains = set()
        for entry in data:
            name_value = entry.get("name_value")
            if name_value:
                for sub in name_value.split("\n"):
                    if sub.endswith(domain):
                        subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        print(f"[-] Exception: {e}")
        return []

def resolve_subdomains(subdomains):
    print("[+] Resolving subdomains...")
    live = []
    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)
            print(f"[LIVE] {sub} -> {ip}")
            live.append((sub, ip))
        except socket.gaierror:
            print(f"[-] Dead: {sub}")
            pass
    return live

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    subs = fetch_subdomains(domain)

    if not subs:
        print("[-] No subdomains found.")
        sys.exit(0)

    # Save all extracted subdomains
    with open("extracted_subdomains.txt", "w") as f:
        for sub in subs:
            f.write(sub + "\n")
    print(f"[+] Saved {len(subs)} subdomains to extracted_subdomains.txt")

    # Resolve and save live subdomains
    live = resolve_subdomains(subs)
    with open("live_subdomains.txt", "w") as f:
        for sub, ip in live:
            f.write(f"{sub} -> {ip}\n")
    print(f"[+] Saved {len(live)} live subdomains to live_subdomains.txt")

    print(f"\n[+] Found {len(live)} live subdomains out of {len(subs)} total.")
