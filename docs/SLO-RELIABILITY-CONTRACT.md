# SLO & Reliability Contract

Each runtime repository must define measurable service objectives rather than only utility-level retry code.

## Required dimensions

| Dimension | Required evidence |
|---|---|
| Latency | p50/p95/p99 or equivalent |
| Availability | successful requests / eligible requests |
| Error budget | SLO target and consumed budget |
| Failure handling | timeout + classified retry policy |
| Circuit breaker | state transitions and open/half-open behavior |
| Idempotency | safe retry boundary where applicable |
| Fallback | explicit fallback or FAIL/DENY outcome |
| Observability | request_id + trace_id + stage + decision |

## Default policy

- Retry only transient, classified failures.
- Bound retries and total request time.
- Add jitter to backoff where retries are used.
- Do not retry authorization or validation failures by default.
- Open a circuit after a defined failure threshold.
- Preserve trace context across retries and fallbacks.
- Emit evidence for the final outcome.

The exact numerical SLO target is service-specific and must be declared by each production-facing repository.
