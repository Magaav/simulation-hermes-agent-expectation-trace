# Expectation Trace Lab v1

This repository is a controlled Lab v1 artifact for an issue-driven Hermes-Agent simulation.

The purpose of the lab is to compare a baseline representation against a patched second node on the same fixed input fixtures from real Hermes-Agent issues, PR-linked regressions, and release-linked evidence. The patched second node adds a measurement-only LeWorldModel-inspired expectation trace observer: expected-vs-actual transition records, heuristic surprise scores, failure taxonomy, and recovery hints.

This lab treats issues and PRs as fixed input fixtures only. The harness is the main contribution.

## Claim Boundary

Bounded simulation artifact. Not a production benchmark. Not proof of runtime superiority.

Safe claim: on the selected fixed input fixtures, the patched second node received higher fixture-level heuristic diagnostic and recovery-hint scores than the baseline representation.

Unsafe claims:

- Hermes-Agent forecasts or discovers issues.
- Hermes-Agent implements the LeWorldModel paper.
- The observer establishes production recovery.
- The observer changes autonomous planning.
- The fixture scores are statistically generalizable.
- The fixture-level heuristic scores show production superiority or runtime superiority.

## Nodes

### Baseline Node

Path: `/local/simulation/hermes-baseline`

Represents baseline behavior as captured by the selected issue, PR, and release-linked evidence. It is not patched with the Expectation Trace observer, and it should not be read as a full production replay.

### Patched Second Node

Path: `/local/simulation/hermes-expectation-trace`

Represents the same fixed input fixtures with a measurement-only observer patch:

- `/local/simulation/simulation-hermes-agent-expectation-trace/patches/expectation_trace_second_node.py`
- `/local/simulation/hermes-expectation-trace/expectation_trace_patch.py`

The patch records diagnostic traces only. It is a simulation artifact, not an upstream Hermes-Agent runtime change. It does not alter planning, establish recovery, or implement the LeWorldModel paper.

## Issue Inputs

Dataset fixture file:

- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/issue_inputs.json`

The current Lab v1 fixture set contains 12 fixed input fixtures:

- #24154: runtime identity context mismatch
- #19785 / PR #21204: `hermes mcp add` dispatch mismatch
- #20982: empty OpenRouter key with fallback providers
- #21055 / PR #21329: malformed numeric MCP tool parameters
- PR #19628: empty cron prerun output
- PR #21193 / release-linked evidence: default secret redaction
- #2104: event loop closed after vision/chained tool calls
- #6843: UnicodeEncodeError boundary handling
- #5211: dotted provider model names normalized into failing identifiers
- #8340: terminal hangs with detached background services
- #14726: delegate_task stalls with long context and secondary toolset
- #220: skill_view path traversal and secret exposure risk

Some fixtures are issue bodies. Some are PR-backed or release-linked evidence. They are all treated as bounded simulation inputs, not as newly forecast or discovered issues.

## Metrics Collected

Metrics live in:

- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/metrics.json`

Collected metrics include:

- failure detection rate
- recovery hint quality
- time to diagnosis steps
- surprise score
- surprise level
- category distribution
- source type distribution
- evidence quality distribution
- secret redaction pass/fail
- JSONL export validity
- validation test counts

## Current Results

Lab status: `partial`

These numbers are fixture-level heuristic scores from the controlled Lab v1 dataset. They are not production incident rates, statistical estimates, or evidence of autonomous recovery.

- total_tasks: 12
- github_issue_tasks: 12
- controlled_simulation_tasks: 0
- total_expectation_traces: 24
- baseline_failure_detection_rate: 0.83
- expectation_trace_failure_detection_rate: 1.00
- baseline_avg_recovery_hint_quality: 0.92
- expectation_trace_avg_recovery_hint_quality: 2.75
- baseline_avg_time_to_diagnosis_steps: 3.67
- expectation_trace_avg_time_to_diagnosis_steps: 1.00
- artifact_validation_checks_passed: 3
- tests_failed: 0
- targeted_pytest_suites_skipped: 1

Interpretation: On these 12 fixed input fixtures, the patched second node received higher fixture-level heuristic diagnostic and recovery-hint scores than the baseline representation. This is an artifact-level result only. It does not establish production recovery or world-model capability.

## Value for Hermes-Agent

1. Every fixed issue can become a permanent recovery eval.
2. Issue history becomes structured evaluation data.
3. Recovery strategies can be compared before runtime changes.
4. Maintainer-rated scoring can replace heuristic scoring later.
5. The harness can become a CI-style regression surface over time.

## Scoring Rubric

The Lab v1 scoring rubric is documented in:

- `/local/simulation/simulation-hermes-agent-expectation-trace/rubrics/recovery_diagnostics_rubric.md`

The rubric defines failure detection score, recovery hint quality score, diagnosis step count, evidence quality, when to mark a fixture inconclusive, and why scores remain heuristic unless maintainer-rated.

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

print("Lab v1 JSON/JSONL validation passed")
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
5. Select `/docs`.

The repository includes `/docs` as a mirror of the dashboard because GitHub Pages commonly supports `/docs` as a branch source.

## Limitations

- This is a bounded simulation artifact, not a full production replay.
- The issue fixtures are fixed inputs and must not be described as forecasts.
- Surprise scoring is heuristic.
- Recovery hint quality is heuristic and should be maintainer-rated in a later study.
- Failure detection rate is a fixture annotation rate, not a measured production reliability rate.
- The validation count refers to artifact checks, not Hermes-Agent product test coverage.
- The second-node patch is a simulation artifact, not an upstream Hermes-Agent change.
- No learned latent model, CEM planning, or long-horizon evaluation is implemented.
- Pytest remains unavailable in this local artifact environment, so targeted pytest suites remain skipped.
