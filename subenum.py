#!/usr/bin/env python3
import typer
from rich.console import Console

app = typer.Typer(help="subenum - minimal subdomain enumeration CLI")
console = Console()

@app.command()
def live(
    domain: str = typer.Option(..., "-d", "--domain", help="Target domain"),
    probe_http: bool = typer.Option(False, "--probe-http", help="Probe HTTP/HTTPS for responsive hosts"),
    concurrency: int = typer.Option(50, "-c", "--concurrency", help="Async concurrency"),
):
    """
    Perform live subdomain enumeration.
    """
    console.print(f"[bold green]Enumerating {domain}[/bold green]")
    console.print(f"probe_http={probe_http}, concurrency={concurrency}")

if __name__ == "__main__":
    app()
