# Expectation Trace Lab v0

This folder is a frozen Lab v0 artifact for an issue-driven Hermes-Agent simulation.

The purpose of the lab is to compare a baseline representation against a patched second node on the same fixed set of GitHub issue and PR-backed regression fixtures. The patched second node adds a measurement-only Expectation Trace observer: expected-vs-actual transition records, heuristic surprise scores, failure taxonomy, and recovery hints.

This lab does not predict issues. Issues and PRs are fixed input fixtures.

## Nodes

### Baseline Node

Path: `/local/simulation/hermes-baseline`

Represents baseline behavior as captured by the selected issue and PR evidence. It is not patched with Expectation Trace, and it should not be read as a full production replay.

### Patched Second Node

Path: `/local/simulation/hermes-expectation-trace`

Represents the same issue inputs with a measurement-only observer patch:

- `/local/simulation/simulation-hermes-agent-expectation-trace/patches/expectation_trace_second_node.py`
- `/local/simulation/hermes-expectation-trace/expectation_trace_patch.py`

The patch records diagnostic traces only. It is a simulation artifact, not an upstream Hermes-Agent change. It does not alter planning, prove recovery, or implement the LeWorldModel paper.

## Issue Inputs

Dataset fixture file:

- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/issue_inputs.json`

The current Lab v0 fixture set contains six issue-derived inputs:

- #24154: runtime identity context mismatch
- #19785 / PR #21204: `hermes mcp add` dispatch mismatch
- #20982: empty OpenRouter key with fallback providers
- #21055 / PR #21329: malformed numeric MCP tool parameters
- PR #19628: empty cron prerun output
- PR #21193 / release-linked evidence: default secret redaction

Some fixtures are live issue bodies. Some are PR-backed or release-linked evidence. They are all treated as bounded simulation inputs, not as newly discovered or predicted issues.

## Metrics Collected

Metrics live in:

- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/metrics.json`

Collected metrics include:

- failure detection rate
- recovery hint quality
- time to diagnosis steps
- surprise score
- surprise level
- secret redaction pass/fail
- JSONL export validity
- validation test counts

## Current Results

Lab status: `partial`

These numbers are fixture-level heuristic scores from the frozen Lab v0 dataset. They are not production incident rates, statistical estimates, or proof of autonomous recovery.

- total_tasks: 6
- github_issue_tasks: 6
- controlled_simulation_tasks: 0
- total_expectation_traces: 12
- baseline_failure_detection_rate: 0.67
- expectation_trace_failure_detection_rate: 1.00
- baseline_avg_recovery_hint_quality: 0.67
- expectation_trace_avg_recovery_hint_quality: 2.67
- artifact_validation_checks_passed: 3
- tests_failed: 0
- targeted_pytest_suites_skipped: 1

Interpretation: On these six fixed fixtures, the patched second node received higher heuristic diagnostic and recovery-hint scores than the baseline representation. This is an artifact-level result only. It does not prove production recovery or world-model capability.

## Lab Database

Canonical structured database:

- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db`

Important files:

- `manifest.json`
- `issue_inputs.json`
- `tasks.json`
- `runs.jsonl`
- `traces.jsonl`
- `comparisons.json`
- `metrics.json`
- `conclusions.json`
- `chart_spec.json`
- `dashboard_prompt.md`
- `data_dictionary.md`

The fixture-to-result chain is:

`issue_inputs.json` -> `tasks.json` -> `runs.jsonl` and `traces.jsonl` -> `comparisons.json` and `metrics.json` -> `results.md`

## Reproduce

From the lab root:

```bash
cd /local/simulation/simulation-hermes-agent-expectation-trace
python3 generate_lab_db.py
```

Validate JSON and JSONL without regenerating:

```bash
python3 - <<'PY'
import json
from pathlib import Path

root = Path("/local/simulation/simulation-hermes-agent-expectation-trace")
for name in [
    "manifest.json",
    "study.json",
    "issue_inputs.json",
    "tasks.json",
    "comparisons.json",
    "metrics.json",
    "conclusions.json",
    "chart_spec.json",
]:
    json.loads((root / "lab_db" / name).read_text())

for name in ["runs.jsonl", "traces.jsonl"]:
    for line in (root / "lab_db" / name).read_text().splitlines():
        json.loads(line)

print("Lab v0 JSON/JSONL validation passed")
PY
```

Compile-check the generator and patch without writing bytecode:

```bash
python3 - <<'PY'
from pathlib import Path

for path in [
    Path("/local/simulation/simulation-hermes-agent-expectation-trace/generate_lab_db.py"),
    Path("/local/simulation/simulation-hermes-agent-expectation-trace/patches/expectation_trace_second_node.py"),
    Path("/local/simulation/hermes-expectation-trace/expectation_trace_patch.py"),
]:
    compile(path.read_text(), str(path), "exec")
    print(f"compiled: {path}")
PY
```

## Static Dashboard

The static dashboard is included in:

- `/local/simulation/simulation-hermes-agent-expectation-trace/dashboard`

It uses copied local data files from `lab_db`:

- `dashboard/data/metrics.json`
- `dashboard/data/comparisons.json`
- `dashboard/data/traces.jsonl`
- `dashboard/data/issue_inputs.json`

View locally:

```bash
cd /local/simulation/simulation-hermes-agent-expectation-trace/dashboard
python3 -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080
```

## GitHub Pages

GitHub Pages setup:

1. Open repository Settings.
2. Go to Pages.
3. Choose Deploy from branch.
4. Select `main`.
5. Select `/dashboard` if GitHub Pages supports that source in the repository.
6. If `/dashboard` is not available, select `/docs`.

This repository includes `/docs` as a mirror of the dashboard because GitHub Pages commonly supports `/docs` as a branch source.

## Limitations

- This is a bounded simulation artifact, not a full production replay.
- The issue fixtures are fixed inputs and must not be described as predictions.
- Surprise scoring is heuristic.
- Recovery hint quality is heuristic and should be maintainer-rated in a later study.
- Failure detection rate is a fixture annotation rate, not a measured production reliability rate.
- The validation count refers to artifact checks, not Hermes-Agent product test coverage.
- The second-node patch is a simulation artifact, not an upstream Hermes-Agent change.
- No learned latent model, CEM planning, or long-horizon evaluation is implemented.
- Pytest was unavailable during Lab v0 stabilization, so targeted pytest suites remain skipped.

## Claim Boundary

Safe claim: the patched second node produced more specific structured diagnostics under the Lab v0 fixture scoring rules.

Unsafe claims:

- Hermes-Agent predicts issues.
- Hermes-Agent implements LeWorldModel.
- The patch proves production recovery.
- The patch improves autonomous planning.
- The fixture scores are statistically generalizable.
