"""Read and validate the four live Docker service health endpoints."""
from datetime import datetime
import json
from pathlib import Path
import urllib.request
from zoneinfo import ZoneInfo

SERVICES = ("financial", "budgets", "notifications", "devices")
ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    results = []
    for service in SERVICES:
        url = f"http://127.0.0.1:8080/services/{service}/health"
        with urllib.request.urlopen(url, timeout=10) as response:
            body = json.load(response)
            status = response.status
        assert status == 200 and body["status"] == "ok"
        assert body["transport"] == "kafka" and all(body["workers"].values())
        print(f"GET {url}")
        print(f"HTTP {status} | status={body['status']} | transport={body['transport']}")
        print("Outbox:", json.dumps(body["outbox"], ensure_ascii=False))
        print("Workers:", json.dumps(body["workers"], ensure_ascii=False))
        print()
        results.append({"url": url, "http_status": status, "response": body})
    output = ROOT / "evidencias/sprint-3/docker/health-checks.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"checked_at": datetime.now(ZoneInfo("America/Lima")).isoformat(),
                                  "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
