"""Pure cross-repository health aggregation, independent from GitHub I/O."""

import re
import urllib.error


def summarize_runs(runs):
    workflows = {}
    for run in runs:
        name = run.get("name") or "unnamed"
        current = {
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "run_id": run.get("id"),
            "updated_at": run.get("updated_at"),
        }
        # GitHub may return multiple attempts. Keep the latest per workflow name.
        previous = workflows.get(name)
        if previous is None or (current["updated_at"] or "") > (previous["updated_at"] or ""):
            workflows[name] = current

    if not workflows:
        return "not_run", "not_run", workflows
    statuses = [value["status"] for value in workflows.values()]
    conclusions = [value["conclusion"] for value in workflows.values()]
    if any(
        status in {"queued", "in_progress", "waiting", "requested", "pending"}
        for status in statuses
    ):
        return "in_progress", None, workflows
    if any(conclusion != "success" for conclusion in conclusions):
        return "completed", "failure", workflows
    return "completed", "success", workflows


def refresh_matrix(repository_items, fetcher):
    rows = []
    for previous in repository_items:
        # Matrix entries are dictionaries, not repository-name strings.
        name = previous["repository"]
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            raise ValueError("invalid repository name in health matrix")
        try:
            ref = fetcher(f"{name}/git/ref/heads/main")
            sha = ref["object"]["sha"]
            runs = fetcher(f"{name}/actions/runs?head_sha={sha}&per_page=100")[
                "workflow_runs"
            ]
            status, conclusion, workflows = summarize_runs(runs)
            latest = max(runs, key=lambda item: item.get("updated_at") or "", default=None)
            rows.append(
                {
                    "repository": name,
                    "status": status,
                    "conclusion": conclusion,
                    "sha": sha,
                    "run_id": latest.get("id") if latest else None,
                    "updated_at": latest.get("updated_at") if latest else None,
                    "workflow_count": len(workflows),
                    "workflows": workflows,
                }
            )
        except urllib.error.HTTPError as exc:
            rows.append(
                {
                    "repository": name,
                    "status": "unavailable" if exc.code == 404 else "error",
                    "conclusion": "repository access unavailable" if exc.code == 404
                        else f"HTTP {exc.code}",
                    "sha": None,
                    "run_id": None,
                    "updated_at": None,
                    "workflow_count": 0,
                    "workflows": {},
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "repository": name,
                    "status": "error",
                    "conclusion": f"{type(exc).__name__}: {str(exc)[:100]}",
                    "sha": None,
                    "run_id": None,
                    "updated_at": None,
                    "workflow_count": 0,
                    "workflows": {},
                }
            )
    return rows


def render_markdown(rows):
    lines = [
        "# Platform Engineering Control Plane",
        "",
        "This matrix reflects workflow runs attached to the latest observed main commit; "
        "unavailable repositories are not treated as passing.",
        "",
        "| Repository | Status | Conclusion | Commit | Gates |",
        "|---|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['repository']} | {row['status']} | {row['conclusion']} | "
            f"{(row['sha'] or '')[:8]} | {row['workflow_count']} |"
        )
    return "\n".join(lines) + "\n"
