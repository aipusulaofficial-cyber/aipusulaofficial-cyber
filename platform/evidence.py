"""Cross-stage evidence contract and trace propagation helpers."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

DECISIONS = {"ALLOW", "DENY", "FAIL"}

@dataclass(frozen=True)
class TraceContext:
    request_id: str = field(default_factory=lambda: str(uuid4()))
    trace_id: str = field(default_factory=lambda: str(uuid4()))

def evidence(ctx: TraceContext, stage: str, decision: str, **data) -> dict:
    if not stage:
        raise ValueError("stage is required")
    if decision not in DECISIONS:
        raise ValueError(f"invalid decision: {decision}")
    return {
        "request_id": ctx.request_id,
        "trace_id": ctx.trace_id,
        "stage": stage,
        "decision": decision,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **data,
    }
