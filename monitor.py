import time
import requests

# The websites we want to monitor
SITES = [
    "https://www.google.com",
    "https://www.github.com",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/3",
    "https://this-site-does-not-exist-12345.com",
]

# Rules for "healthy"
MAX_RESPONSE_MS = 2000


def check_url(url):
    """Visit the URL. Return (status_code, response_time_ms).
    If the site can't be reached at all, return (None, None)."""
    try:
        start = time.perf_counter()
        response = requests.get(url, timeout=5)
        end = time.perf_counter()
        response_ms = (end - start) * 1000
        return response.status_code, response_ms
    except requests.exceptions.RequestException:
        return None, None


def is_healthy(status, response_ms):
    """Healthy = status 200 AND faster than MAX_RESPONSE_MS."""
    if status is None:
        return False
    return status == 200 and response_ms < MAX_RESPONSE_MS


def main():
    """Check every site and print one line per site."""
    print("Checking sites...\n")
    for url in SITES:
        status, response_ms = check_url(url)

        if status is None:
            print(f"💥 {url:<45} UNREACHABLE")
        elif is_healthy(status, response_ms):
            print(f"✅ {url:<45} {status}  {response_ms:6.0f} ms")
        else:
            print(f"❌ {url:<45} {status}  {response_ms:6.0f} ms")


main()