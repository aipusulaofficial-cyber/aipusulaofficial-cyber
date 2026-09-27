# AIPusula Platform Integration

The portfolio is organized as independently runnable systems connected by explicit contracts.

## End-to-end contract

```text
Gateway
  -> Policy
  -> Agent / RAG
  -> Inference
  -> Evaluation
  -> Registry / MLOps
  -> Observability
  -> Cost
  -> Evidence
```

Each stage carries request_id and trace_id and emits an ALLOW, DENY, or FAIL decision. Evidence is validated against platform/evidence.schema.json.

This repository is the control-plane documentation and contract surface; service-to-service production wiring must be demonstrated by executable integration tests before being claimed.
