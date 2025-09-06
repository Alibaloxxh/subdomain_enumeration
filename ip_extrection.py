import socket
import ipaddress
from prettytable import PrettyTable

def extract_ip_info(subdomains):
    results = []
    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)

            if ipaddress.ip_address(ip).is_private:
                ip_type = "Private IP"
            else:
                ip_type = "Public IP"

            results.append({
                "subdomain": sub,
                "origin_ip": ip,
                "category": ip_type
            })

        except socket.gaierror:
            results.append({
                "subdomain": sub,
                "origin_ip": "Unresolved",
                "category": "Unresolved"
            })

    return results

if __name__ == "__main__":
    
    subdomains = ["google.com", "localhost", "test.local"]

    print("\n=== IP Extraction Results ===\n")
    info = extract_ip_info(subdomains)

    table = PrettyTable()
    table.field_names = ["Subdomain", "Origin IP", "Category"]

    private_ips = []
    public_ips = []

    for item in info:
        table.add_row([item["subdomain"], item["origin_ip"], item["category"]])

        if item["category"] == "Private IP":
            private_ips.append(item["origin_ip"])
        elif item["category"] == "Public IP":
            public_ips.append(item["origin_ip"])

    print(table)

    print("\n=== Summary ===")
    print(f"Private IPs: {private_ips}")
    print(f"Public IPs : {public_ips}")