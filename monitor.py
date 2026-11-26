import argparse
import csv
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
def load_config(path):
    """Read sites.yaml and return it as a Python dictionary."""
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Checking (same ideas as Stage 1)
# ---------------------------------------------------------------------------
def check_url(url, timeout):
    """Visit the URL. Return (status_code, response_time_ms).
    If the site can't be reached at all, return (None, None)."""
    try:
        start = time.perf_counter()
        response = requests.get(url, timeout=timeout)
        end = time.perf_counter()
        return response.status_code, (end - start) * 1000
    except requests.exceptions.RequestException:
        return None, None


def is_healthy(status, response_ms, max_ms):
    """Healthy = status 200 AND faster than max_ms."""
    if status is None:
        return False
    return status == 200 and response_ms < max_ms


# ---------------------------------------------------------------------------
# Saving history
# ---------------------------------------------------------------------------
def save_result(results_file, row):
    """Add one row to the CSV file. Write the header first if the file is new."""
    is_new_file = not Path(results_file).exists()
    with open(results_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "name", "url", "status", "response_ms", "healthy"])
        if is_new_file:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# One full round of checks
# ---------------------------------------------------------------------------
def run_checks(config):
    settings = config["settings"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nChecking {len(config['sites'])} sites at {timestamp}")

    for site in config["sites"]:
        status, response_ms = check_url(site["url"], settings["timeout_seconds"])
        healthy = is_healthy(status, response_ms, settings["max_response_ms"])

        if status is None:
            print(f"💥 {site['name']:<28} UNREACHABLE")
        elif healthy:
            print(f"✅ {site['name']:<28} {status}  {response_ms:6.0f} ms")
        else:
            print(f"❌ {site['name']:<28} {status}  {response_ms:6.0f} ms")

        save_result(settings["results_file"], {
            "timestamp": timestamp,
            "name": site["name"],
            "url": site["url"],
            "status": status if status is not None else "",
            "response_ms": round(response_ms) if response_ms is not None else "",
            "healthy": healthy,
        })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Simple website uptime monitor")
    parser.add_argument("--config", default="sites.yaml", help="path to the config file")
    parser.add_argument("--watch", action="store_true", help="keep checking until Ctrl+C")
    args = parser.parse_args()

    config = load_config(args.config)

    if not args.watch:
        run_checks(config)
        return

    interval = config["settings"]["check_interval_seconds"]
    print(f"Watching every {interval} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            run_checks(config)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped. Results are in", config["settings"]["results_file"])


if __name__ == "__main__":
    main()