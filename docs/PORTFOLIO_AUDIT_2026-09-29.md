# Cross-repository principal audit — 2026-09-29

**Status:** remediation in progress. A draft pull request is not production certification. Do not label an individual repository GREEN until all required checks pass on its latest reviewed commit.

## Review queue

| Repository | Review PR |
| --- | --- |
| ai-evaluation-platform | [PR #2](https://github.com/aipusulaofficial-cyber/ai-evaluation-platform/pull/2) |
| mlops-model-platform | [PR #8](https://github.com/aipusulaofficial-cyber/mlops-model-platform/pull/8) |
| real-time-ai-pipeline | [PR #10](https://github.com/aipusulaofficial-cyber/real-time-ai-pipeline/pull/10) |
| ai-observability-platform | [PR #10](https://github.com/aipusulaofficial-cyber/ai-observability-platform/pull/10) |
| aipusula-report | [PR #2](https://github.com/aipusulaofficial-cyber/aipusula-report/pull/2) |
| ai-reliability-platform | [PR #10](https://github.com/aipusulaofficial-cyber/ai-reliability-platform/pull/10) |
| secure-ai-gateway | [PR #10](https://github.com/aipusulaofficial-cyber/secure-ai-gateway/pull/10) |
| autonomous-agent-orchestrator | [PR #10](https://github.com/aipusulaofficial-cyber/autonomous-agent-orchestrator/pull/10) |
| ai-security-platform | [PR #8](https://github.com/aipusulaofficial-cyber/ai-security-platform/pull/8) |
| ai-model-registry | [PR #8](https://github.com/aipusulaofficial-cyber/ai-model-registry/pull/8) |
| agentic-engineering-platform | [PR #2](https://github.com/aipusulaofficial-cyber/agentic-engineering-platform/pull/2) |
| ai-feature-store | [PR #8](https://github.com/aipusulaofficial-cyber/ai-feature-store/pull/8) |
| ai-evaluation-framework | [PR #10](https://github.com/aipusulaofficial-cyber/ai-evaluation-framework/pull/10) |
| ai-workflow-engine | [PR #10](https://github.com/aipusulaofficial-cyber/ai-workflow-engine/pull/10) |
| ai-data-governance-platform | [PR #10](https://github.com/aipusulaofficial-cyber/ai-data-governance-platform/pull/10) |
| ai-api-platform | [PR #11](https://github.com/aipusulaofficial-cyber/ai-api-platform/pull/11) |
| event-driven-ai-platform | [PR #10](https://github.com/aipusulaofficial-cyber/event-driven-ai-platform/pull/10) |
| ai-cost-optimization-platform | [PR #11](https://github.com/aipusulaofficial-cyber/ai-cost-optimization-platform/pull/11) |
| distributed-ai-inference-platform | [PR #10](https://github.com/aipusulaofficial-cyber/distributed-ai-inference-platform/pull/10) |
| enterprise-rag-platform | [PR #7](https://github.com/aipusulaofficial-cyber/enterprise-rag-platform/pull/7) |
| cloud-native-ai-platform | [PR #10](https://github.com/aipusulaofficial-cyber/cloud-native-ai-platform/pull/10) |

**Private design system:** review/change blocked by the available security controls; not marked remediated.

## Merge gates for every repository
1. Quality and format checks green on the latest PR head; reproduce any failures from job logs.
2. Production and contract tests green, covering the specific failure repaired by the PR.
3. Security and dependency/SBOM checks reviewed; any risk acceptance documented.
4. Runtime/deployment/evidence claims backed by executable artifacts, not only README text.
5. PR diff reviewed for compatibility, tests and architectural invariants before merge.

**Scope:** the linked PRs are targeted audit fixes. Full principal-level certification additionally requires deeper architecture review, end-to-end deployment validation, and realistic load/failure testing.

## September 29 evidence integrity remediation

The first 22 draft PR heads (21 application repositories plus this portfolio) passed their configured checks before the later evidence-quality corrections. **Do not reuse that earlier GREEN snapshot** for any PR whose head subsequently changed.

- Report application: [PR #2](https://github.com/aipusulaofficial-cyber/aipusula-report/pull/2) now has a separately scoped `server/index.ts` coverage gate; its verified sample was 15 tests, 93.93% line coverage, 100% function coverage and 80% branch coverage. The front-end is *not* covered by this metric.
- Python repositories: 20 draft PRs now correct a shared JUnit parser error that read test counts from the top-level `testsuites` element and falsely reported zero tests. The workflows sum the actual `testsuite` attributes and reject zero-test evidence. Reverify each updated PR head before merge.
- Security gateway: readiness now requires a deployed JWT verification secret. Its local rate limiter remains *process-local* and is not a shared production quota service.

## Known architectural follow-ups

- [Gateway multi-replica quotas and trusted client identity](https://github.com/aipusulaofficial-cyber/secure-ai-gateway/issues/11): requires shared atomic storage, identity-bound keys, multi-instance failure and concurrency testing. The currently deployed design must not claim consistent fleet-wide rate limiting.
- [Report frontend coverage and browser-level behavior](https://github.com/aipusulaofficial-cyber/aipusula-report/issues/3): a server-only coverage percentage cannot stand in for the whole app.
- [Report reproducible coverage dependencies](https://github.com/aipusulaofficial-cyber/aipusula-report/issues/4): the coverage job still installs its provider dynamically and requires a regenerated, committed pnpm lockfile.
- The private design-system's independent contract workflow validates tokens/components; its main CI file was not modified because the write attempt was blocked.

## Coverage denominator integrity

Python repositories previously measured `--cov=.`, which included regression test implementation files in the coverage denominator. Their 20 audit PRs now include an explicit `.coveragerc` or equivalent scope to omit test implementation from the source measurement, while retaining the corrected JUnit suite counts. The gateway's independently verified scoped result is **36 tests and 87.12% source line coverage**, subject to verification against each subsequent PR head. These corrected measurements are not comparable with the older test-inclusive figures.

Coverage gates must be agreed against the **source-only** baseline. In particular, JUnit test counts, application source coverage and runtime production evidence are three separate claims; do not conflate them. Subsequent changes invalidate an earlier GREEN snapshot until GitHub Actions completes again.
