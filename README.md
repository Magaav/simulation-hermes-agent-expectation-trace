# Issue-Fixture Recovery Diagnostics for Hermes-Agent

A bounded Lab v1 simulation artifact using real issue and PR-linked fixtures.

Links:
- Dashboard: https://magaav.github.io/simulation-hermes-agent-expectation-trace/
- Paper: ./paper.md
- Results: ./results.md
- Rubric: ./rubrics/recovery_diagnostics_rubric.md
- Lab DB: ./lab_db

## Abstract

This Lab v1 artifact converts real Hermes-Agent GitHub issues and PR-linked regressions into fixed input fixtures for recovery-diagnostic evaluation. It compares a baseline representation against a second node with a LeWorldModel-inspired expectation trace observer. The purpose is not to prove runtime superiority, but to test whether issue history can become a reusable evaluation surface for agent recovery behavior.

## Final Conclusion

On 12 fixed issue/PR-linked fixtures, the expectation trace observer produced higher fixture-level heuristic scores than the baseline representation:

- failure detection: 0.83 -> 1.00
- recovery hint quality: 0.92 -> 2.75
- diagnosis steps: 3.67 -> 1.00

These results are bounded to the selected fixtures and scoring rubric. They are not production reliability measurements, not statistical proof, and not evidence of a full LeWorldModel implementation.

> This page reports fixture-level heuristic scores only. It does not claim issue prediction, production superiority, statistical significance, runtime superiority, or a full LeWorldModel implementation.

## Reproduce

From the lab root:

```bash
python3 generate_lab_db.py
```

Validate JSON and JSONL without regenerating:

```bash
python3 - <<'PY'
import json
from pathlib import Path

root = Path(".")
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
    Path("generate_lab_db.py"),
    Path("patches/expectation_trace_second_node.py"),
]:
    compile(path.read_text(), str(path), "exec")
    print(f"compiled: {path}")
PY
```

## Fixture List

The Lab v1 fixture set contains 12 fixed input fixtures:

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

## Metrics

Current Lab v1 metrics:

- total_tasks: 12
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

These numbers are fixture-level heuristic scores from the controlled Lab v1 dataset. They are not production incident rates, statistical estimates, or evidence of autonomous recovery.

## Nodes

### Baseline Representation

The baseline representation is derived from the selected issue, PR, and release-linked evidence. It is not patched with the expectation trace observer, and it should not be read as a full production replay.

### Patched Second Node

The patched second node uses the same fixed input fixtures with a measurement-only observer patch:

- `patches/expectation_trace_second_node.py`

The patch records diagnostic traces only. It is a simulation artifact, not an upstream Hermes-Agent runtime change. It does not alter planning, establish recovery, or implement the LeWorldModel paper.

## Lab Database

Canonical structured database:

- `lab_db`

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

## Static Dashboard

The static dashboard is included in:

- `dashboard`
- `docs`

`docs` is the GitHub Pages mirror. The dashboard uses copied local data files from `lab_db`:

- `dashboard/data/metrics.json`
- `dashboard/data/comparisons.json`
- `dashboard/data/traces.jsonl`
- `dashboard/data/issue_inputs.json`

View locally:

```bash
cd dashboard
python3 -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080
```

## Value for Hermes-Agent

1. Every fixed issue can become a permanent recovery eval.
2. Issue history becomes structured evaluation data.
3. Recovery strategies can be compared before runtime changes.
4. Maintainer-rated scoring can replace heuristic scoring later.
5. The harness can become a CI-style regression surface over time.

## Scoring Rubric

The Lab v1 scoring rubric is documented in:

- `rubrics/recovery_diagnostics_rubric.md`

The rubric defines failure detection score, recovery hint quality score, diagnosis step count, evidence quality, when to mark a fixture inconclusive, and why scores remain heuristic unless maintainer-rated.

## GitHub Pages

GitHub Pages is served from `main` / `docs`:

- https://magaav.github.io/simulation-hermes-agent-expectation-trace/

## Limitations

- This is a bounded simulation artifact, not a full production replay.
- The issue fixtures are fixed inputs and must not be described as forecasts.
- Surprise scoring is heuristic.
- Recovery hint quality is heuristic and should be maintainer-rated in a later study.
- Failure detection rate is a fixture annotation rate, not a measured production reliability rate.
- The validation count refers to artifact checks, not Hermes-Agent product test coverage.
- The second-node patch is a simulation artifact, not an upstream Hermes-Agent change.
- No learned latent model, CEM planning, or long-horizon evaluation is implemented.
- Targeted pytest suites remain skipped in this artifact.
