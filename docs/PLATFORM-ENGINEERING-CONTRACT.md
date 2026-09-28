# AIPusula Platform Engineering Contract

## Scope
Every repository in the AIPusula platform family follows the same engineering control loop:

**Code → Quality → Security → Test → Build → Runtime Evidence → SLO → Provenance**

## Enforcement
A repository is contract-compliant only when its reusable GitHub Actions contract completes successfully. A failed security, test, dependency, build, or contract-validation step is a failed contract.

No `|| true`, unconditional `echo` success, or empty foundation assertion is an acceptable substitute for validation.

## Runtime evidence
Services SHOULD emit these fields for every request/stage:

- request_id
- trace_id
- stage
- decision: ALLOW | DENY | FAIL
- timestamp
- latency_ms
- error
- cost_usd
- retry_count
- circuit_state

Authorization, policy, and safety boundaries are fail-closed: downstream uncertainty must not silently become ALLOW.

## Security
Python repositories run dependency integrity and `pip-audit`; Node repositories run `npm audit --audit-level=high`. Release builds produce provenance attestations where GitHub permissions and artifact availability allow it.

## Reliability
Each service declares SLO targets appropriate to its workload. Reliability behavior must be observable: retry count, timeout/failure classification, circuit state, and fallback/fail-closed outcome.

## Evidence
Every contract run publishes a machine-readable evidence artifact containing repository, commit, workflow/run identifiers, contract version, stage, decision, and validation checks.

## Governance
The platform repository is the source of truth for the reusable workflow, runtime schema, contract definition, and repository health matrix.
