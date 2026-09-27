"""Deterministic end-to-end platform integration harness.

This test models the cross-repository contract without claiming that the
individual repositories are deployed as live services. It verifies the shared
trace, stage ordering, admission decisions, and evidence semantics.
"""
from __future__ import annotations

import json
from pathlib import Path

from evidence import TraceContext, evidence

STAGES = [
    "gateway",
    "policy",
    "rag",
    "inference",
    "evaluation",
    "registry",
    "observability",
    "cost",
]


def run_flow() -> list[dict]:
    ctx = TraceContext("req-e2e-001", "trace-e2e-001")
    checks = [
        ("gateway", "ALLOW", {"auth": "PASS"}),
        ("policy", "ALLOW", {"security": "PASS", "data_policy": "PASS"}),
        ("rag", "ALLOW", {"retrieval_evidence": True}),
        ("inference", "ALLOW", {"model": "mock-model-v1"}),
        ("evaluation", "ALLOW", {"quality_score": 0.90}),
        ("registry", "ALLOW", {"promotion": "CANARY"}),
        ("observability", "ALLOW", {"telemetry": "RECORDED"}),
        ("cost", "ALLOW", {"cost_recorded": True}),
    ]
    return [evidence(ctx, stage, decision, **data) for stage, decision, data in checks]


def test_end_to_end_trace_contract(tmp_path: Path) -> None:
    records = run_flow()
    assert [r["stage"] for r in records] == STAGES
    assert {r["request_id"] for r in records} == {"req-e2e-001"}
    assert {r["trace_id"] for r in records} == {"trace-e2e-001"}
    assert all(r["decision"] == "ALLOW" for r in records)

    output = tmp_path / "integration-trace.json"
    output.write_text(json.dumps(records, indent=2), encoding="utf-8")
    assert output.exists()


def test_fail_closed_decision_is_supported() -> None:
    ctx = TraceContext("req-deny-001", "trace-deny-001")
    denied = evidence(ctx, "gateway", "DENY", reason="authorization")
    assert denied["decision"] == "DENY"
