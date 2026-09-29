import json
import os
import urllib.request
from pathlib import Path

OWNER = "aipusulaofficial-cyber"
REPO = "aipusulaofficial-cyber"
BASE = f"https://api.github.com/repos/{OWNER}"
repos = json.loads(Path("platform/health-matrix.json").read_text())["repositories"]
token = os.environ["GITHUB_TOKEN"]

def get(path):
    req = urllib.request.Request(
        f"{BASE}/{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

rows = []
for name in repos:
    try:
        runs = get(f"{name}/actions/runs?per_page=30")["workflow_runs"]
        contract = sorted(
            (r for r in runs if r.get("name") == "Engineering Contract"),
            key=lambda r: r.get("created_at") or "",
            reverse=True,
        )
        latest = contract[0] if contract else None
        rows.append({
            "repository": name,
            "status": latest.get("status") if latest else "not_run",
            "conclusion": latest.get("conclusion") if latest else "not_run",
            "sha": latest.get("head_sha") if latest else None,
            "run_id": latest.get("id") if latest else None,
            "updated_at": latest.get("updated_at") if latest else None,
        })
    except Exception as exc:
        rows.append({
            "repository": name,
            "status": "error",
            "conclusion": str(exc)[:120],
            "sha": None,
            "run_id": None,
            "updated_at": None,
        })

Path("platform/health-matrix.json").write_text(
    json.dumps({"contract_version":"1.0","repositories":rows}, indent=2) + "\n",
    encoding="utf-8",
)
lines = [
    "# Platform Engineering Control Plane",
    "",
    "| Repository | Status | Conclusion | Commit | Run |",
    "|---|---|---|---|---|",
]
for x in rows:
    lines.append(f"| {x['repository']} | {x['status']} | {x['conclusion']} | {(x['sha'] or '')[:8]} | {x['run_id'] or ''} |")
Path("docs/PLATFORM-HEALTH-MATRIX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
