"""Refresh current-main GitHub Actions evidence without confusing stale or private runs."""

import json
import os
import urllib.request
from pathlib import Path

from matrix_core import refresh_matrix, render_markdown

OWNER = "aipusulaofficial-cyber"
BASE = f"https://api.github.com/repos/{OWNER}"
ROOT = Path(__file__).resolve().parents[1]


def get(path):
    token = os.environ["GITHUB_TOKEN"]
    request = urllib.request.Request(
        f"{BASE}/{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def main():
    matrix_file = ROOT / "platform" / "health-matrix.json"
    repositories = json.loads(matrix_file.read_text(encoding="utf-8"))["repositories"]
    rows = refresh_matrix(repositories, get)
    matrix_file.write_text(
        json.dumps({"contract_version": "2.0", "repositories": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / "docs" / "PLATFORM-HEALTH-MATRIX.md").write_text(
        render_markdown(rows), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
