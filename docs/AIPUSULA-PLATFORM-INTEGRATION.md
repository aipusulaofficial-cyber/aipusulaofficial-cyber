# AIPusula Platform Integration Contract

## Purpose

This repository defines the cross-repository contract for the AIPusula AI platform. The
contract is intentionally deterministic: it validates trace propagation, stage ordering,
decision semantics, and evidence generation without pretending that local tests are live
production deployments.

## Required stages

1. gateway
2. policy
3. rag
4. inference
5. evaluation
6. registry
7. observability
8. cost

Every stage must preserve the same `request_id` and `trace_id`.

## Decision contract

A stage may emit only:

- `ALLOW`
- `DENY`
- `FAIL`

The default production posture for authorization, policy, and safety boundaries is
fail-closed. A downstream failure must not silently become an `ALLOW`.

## Evidence contract

Every evidence record must contain:

- `request_id`
- `trace_id`
- `stage`
- `decision`
- `timestamp`

The canonical schema is `platform/evidence.schema.json`.

## Validation

The platform gate must:

1. validate the evidence schema;
2. execute the deterministic end-to-end contract tests;
3. compile the platform helpers;
4. generate a trace artifact from the same test flow;
5. upload that artifact for inspection.

The integration test is a contract harness, not a claim that all component repositories are
deployed and reachable from the GitHub runner.
