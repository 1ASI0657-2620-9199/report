"""Capture real MVP responses and prepare a Postman collection for Sprint 1.

Run from report after installing the sibling back/requirements.txt.
This uses TestClient and temporary SQLite; it does not capture Postman or UI.
"""

import gc
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from datetime import datetime, timedelta, timezone


REPORT = Path(__file__).resolve().parents[1]
BACK = REPORT.parent / "back"
OUTPUT = REPORT / "evidencias/sprint-1"


def write_json(name, value):
    OUTPUT.joinpath(name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main():
    if not (BACK / "app/main.py").is_file():
        raise SystemExit("Clone back next to report and install its requirements first.")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(BACK))
    from fastapi.testclient import TestClient
    from app.main import create_app

    commit = subprocess.check_output(
        ["git", "-C", str(BACK), "rev-parse", "HEAD"], text=True
    ).strip()
    timestamp = datetime.now(timezone(timedelta(hours=-5))).isoformat(timespec="seconds")
    payload = {
        "account_id": "cash-account",
        "type": "income",
        "amount": "1000.00",
        "currency": "PEN",
        "category": "salary",
        "occurred_at": "2026-10-01T10:00:00Z",
        "description": "Ingreso de demostración Sprint 1",
    }
    expense = {**payload, "type": "expense", "amount": "125.50", "category": "food",
               "description": "Gasto de demostración Sprint 1"}
    steps = [
        ("01-health", "GET", "/health", None, None, 200),
        ("02-income", "POST", "/api/v1/transactions", payload, "income", 201),
        ("03-replay", "POST", "/api/v1/transactions", payload, "income", 200),
        ("04-conflict", "POST", "/api/v1/transactions", {**payload, "amount": "2000.00"}, "income", 409),
        ("05-expense", "POST", "/api/v1/transactions", expense, "expense", 201),
        ("06-list", "GET", "/api/v1/transactions", None, None, 200),
        ("07-summary", "GET", "/api/v1/summary?month=2026-10&currency=PEN", None, None, 200),
        ("08-invalid-month", "GET", "/api/v1/summary?month=2026-13&currency=PEN", None, None, 422),
    ]
    records = []
    with TemporaryDirectory(prefix="finanzen-evidence-") as directory:
        app = create_app(str(Path(directory) / "records.db"))
        with TestClient(app) as client:
            for name, method, path, body, key, expected in steps:
                headers = {} if path == "/health" else {"X-User-Id": "sprint1-evidence-user"}
                if key:
                    headers["Idempotency-Key"] = "sprint1-evidence-" + key
                options = {"headers": headers}
                if body is not None:
                    options["json"] = body
                response = client.request(method, path, **options)
                if response.status_code != expected:
                    raise RuntimeError(f"{name}: expected {expected}, got {response.status_code}")
                records.append({
                    "scenario": name, "method": method, "path": path,
                    "request_headers": headers, "request_body": body,
                    "status_code": response.status_code,
                    "idempotent_replayed": response.headers.get("Idempotent-Replayed"),
                    "response_body": response.json(),
                })
        gc.collect()
    write_json("respuestas-api.json", {
        "captured_at_america_lima": timestamp,
        "backend_commit": commit,
        "execution": "FastAPI TestClient; temporary SQLite; synthetic demonstration data",
        "requests": records,
    })
    pytest = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=BACK, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    OUTPUT.joinpath("pytest.txt").write_text(
        f"Captured at (America/Lima): {timestamp}\nBackend commit: {commit}\n"
        "Command: python -m pytest -q -p no:cacheprovider\n\n"
        + pytest.stdout + pytest.stderr, encoding="utf-8",
    )
    if pytest.returncode:
        raise SystemExit(pytest.returncode)

    items = []
    for name, method, path, body, key, expected in steps:
        headers = [] if path == "/health" else [
            {"key": "X-User-Id", "value": "evidence-{{evidenceRunId}}"}
        ]
        if key:
            headers += [
                {"key": "Idempotency-Key", "value": key + "-{{evidenceRunId}}"},
                {"key": "Content-Type", "value": "application/json"},
            ]
        request = {"method": method, "header": headers, "url": "{{baseUrl}}" + path}
        if body is not None:
            request["body"] = {"mode": "raw", "raw": json.dumps(body, ensure_ascii=False, indent=2),
                               "options": {"raw": {"language": "json"}}}
        checks = [f"pm.test('HTTP {expected}', function () {{ pm.response.to.have.status({expected}); }});"]
        if name == "03-replay":
            checks.append("pm.test('Same movement ID', function () { pm.expect(pm.response.json().id).to.eql(pm.collectionVariables.get('incomeId')); });")
        if name == "02-income":
            checks.append("pm.collectionVariables.set('incomeId', pm.response.json().id);")
        if name == "07-summary":
            checks.append("pm.test('Monthly totals', function () { const r = pm.response.json(); pm.expect(Number(r.income)).to.eql(1000); pm.expect(Number(r.expenses)).to.eql(125.5); pm.expect(Number(r.balance)).to.eql(874.5); pm.expect(r.transaction_count).to.eql(2); });")
        if name == "06-list":
            checks.append("pm.test('Two movements', function () { pm.expect(pm.response.json().length).to.eql(2); });")
        events = [{"listen": "test", "script": {"type": "text/javascript", "exec": checks}}]
        if name == "01-health":
            events.insert(0, {"listen": "prerequest", "script": {"type": "text/javascript", "exec": [
                "pm.collectionVariables.set('evidenceRunId', pm.variables.replaceIn('{{$guid}}'));"
            ]}})
        items.append({"name": name, "request": request, "event": events})
    write_json("FinanZen-Sprint1.postman_collection.json", {
        "info": {
            "name": "FinanZen - Sprint 1 evidence",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "description": "Run requests 01 through 08 in order. Each run starts a new demo user; captures and video are pending.",
        },
        "variable": [{"key": "baseUrl", "value": "http://127.0.0.1:8000"},
                     {"key": "evidenceRunId", "value": ""}],
        "item": items,
    })
    print("Captured 8 API responses; existing pytest suite passed; Postman collection prepared.")


if __name__ == "__main__":
    main()
