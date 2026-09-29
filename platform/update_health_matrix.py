import json
import os
import urllib.error
import urllib.request
from pathlib import Path

OWNER = "aipusulaofficial-cyber"
BASE = f"https://api.github.com/repos/{OWNER}"
repos = json.loads(Path("platform/health-matrix.json").read_text())["repositories"]
token = os.environ["GITHUB_TOKEN"]


def get(path):
    req = urllib.request.Request(
        f"{BASE}/{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def summarize_runs(runs):
    workflows = {}
    for run in runs:
        workflows[run["name"]] = {
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "run_id": run.get("id"),
            "updated_at": run.get("updated_at"),
        }

    statuses = [item["status"] for item in workflows.values()]
    conclusions = [item["conclusion"] for item in workflows.values()]
    if any(
        status in {"queued", "in_progress", "waiting", "requested", "pending"}
        for status in statuses
    ):
        overall_status = "in_progress"
        overall_conclusion = None
    elif any(conclusion != "success" for conclusion in conclusions):
        overall_status = "completed"
        overall_conclusion = "failure"
    elif workflows:
        overall_status = "completed"
        overall_conclusion = "success"
    else:
        overall_status = "not_run"
        overall_conclusion = "not_run"

    return overall_status, overall_conclusion, workflows


rows = []
for name in repos:
    previous = next(item for item in repos if item["repository"] == name)
    try:
        ref = get(f"{name}/git/ref/heads/main")
        sha = ref["object"]["sha"]
        runs = get(f"{name}/actions/runs?head_sha={sha}&per_page=100")["workflow_runs"]
        status, conclusion, workflows = summarize_runs(runs)
        latest_run = max(runs, key=lambda run: run.get("updated_at") or "", default=None)
        rows.append(
            {
                "repository": name,
                "status": status,
                "conclusion": conclusion,
                "sha": sha,
                "run_id": latest_run.get("id") if latest_run else None,
                "updated_at": latest_run.get("updated_at") if latest_run else None,
                "workflow_count": len(workflows),
                "workflows": workflows,
            }
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            rows.append(
                {
                    **previous,
                    "status": "unavailable",
                    "conclusion": "repository access unavailable",
                    "workflow_count": 0,
                    "workflows": {},
                }
            )
        else:
            rows.append(
                {
                    **previous,
                    "status": "error",
                    "conclusion": f"HTTP {exc.code}",
                    "workflow_count": 0,
                    "workflows": {},
                }
            )
    except Exception as exc:
        rows.append(
            {
                **previous,
                "status": "error",
                "conclusion": str(exc)[:120],
                "workflow_count": 0,
                "workflows": {},
            }
        )

Path("platform/health-matrix.json").write_text(
    json.dumps({"contract_version": "2.0", "repositories": rows}, indent=2) + "\n",
    encoding="utf-8",
)

lines = [
    "# Platform Engineering Control Plane",
    "",
    "The matrix evaluates workflow runs attached to the current main commit rather than treating an older Engineering Contract run as repository health.",
    "",
    "| Repository | Status | Conclusion | Commit | Gates |",
    "|---|---|---|---|---:|",
]
for item in rows:
    lines.append(
        f"| {item['repository']} | {item['status']} | {item['conclusion']} | "
        f"{(item['sha'] or '')[:8]} | {item['workflow_count']} |"
    )
Path("docs/PLATFORM-HEALTH-MATRIX.md").write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
)
