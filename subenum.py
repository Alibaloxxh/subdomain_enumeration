#!/usr/bin/env python3#!/usr/bin/env python3
import typer
from rich.console import Console
import requests
import socket

app = typer.Typer(help="subenum - minimal subdomain enumeration CLI")
console = Console()


def fetch_subdomains(domain: str):
    """Fetch subdomains from crt.sh"""
    console.print(f"[cyan][+] Fetching subdomains for {domain} from crt.sh...[/cyan]")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            console.print("[red][-] Error fetching data from crt.sh[/red]")
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
        console.print(f"[red][-] Exception: {e}[/red]")
        return []


def resolve_subdomains(subdomains):
    """Resolve subdomains to IPs"""
    console.print("[cyan][+] Resolving subdomains...[/cyan]")
    live = []
    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)
            console.print(f"[green][LIVE][/green] {sub} -> {ip}")
            live.append((sub, ip))
        except socket.gaierror:
            pass
    return live


@app.command()
def live(
    domain: str = typer.Option(..., "-d", "--domain", help="Target domain"),
    probe_http: bool = typer.Option(False, "--probe-http", help="Probe HTTP/HTTPS for responsive hosts"),
    concurrency: int = typer.Option(50, "-c", "--concurrency", help="Async concurrency"),
):
    """Perform live subdomain enumeration"""
    console.print(f"[bold green]Enumerating {domain}[/bold green]")

    subs = fetch_subdomains(domain)
    if not subs:
        console.print("[red][-] No subdomains found.[/red]")
        raise typer.Exit()

    live_hosts = resolve_subdomains(subs)
    console.print(f"\n[bold cyan][+] Found {len(live_hosts)} live subdomains.[/bold cyan]")


if __name__ == "__main__":
    app()
