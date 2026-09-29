# GitHub Workflow Evidence Guide

The AIPUSULA portfolio uses GitHub Actions as executable engineering evidence across its core repositories.

## Portfolio workflow model

Each repository follows the same evidence vocabulary while retaining domain-specific checks:

`Trigger → Runner → Setup → Quality Gate → Domain Evidence → Tests → Security/Build Checks → Artifacts → Result`

### Trigger
Workflow files under `.github/workflows/` define when verification runs, such as pushes, pull requests, or manual dispatch.

### Job
A job is an independent verification unit executed on a runner.

### Step
Each job is made of ordered actions or shell commands. The step log is the lowest-level execution evidence.

### Gate
Formatting, linting, typing, tests, security checks, benchmarks, and domain assertions can act as explicit pass/fail gates.

### Artifact
Important outputs are preserved as workflow artifacts: JUnit results, coverage reports, benchmark evidence, build evidence, and machine-readable summaries.

## How to review a repository

1. Open the repository's **Actions** tab.
2. Select the workflow run for the commit under review.
3. Identify the first failed step if the run is red.
4. Inspect downstream skipped steps as consequences rather than separate root causes.
5. Open uploaded artifacts for machine-readable evidence.
6. Verify the replacement commit's complete workflow set after a fix.

## Core repository guides

Each core repository now contains `docs/GITHUB_WORKFLOW_GUIDE.md` with its domain-specific workflow evidence focus.

The guides complement `docs/PORTFOLIO_EVIDENCE.md`: the workflow guide explains **how the evidence executes**, while the portfolio evidence map explains **what engineering claim the evidence supports**.

## Evidence principle

A successful workflow demonstrates that the configured checks passed for a specific commit. It is not an unlimited production-performance guarantee. The portfolio uses executable checks, deterministic reference-path evidence, and preserved artifacts to make engineering claims inspectable and reproducible.
