# Lab v1 Validation

Validation date: 2026-05-13

## Files Verified

Required Lab v1 files exist:

- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/issue_inputs.json`
- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/manifest.json`
- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/dashboard_prompt.md`
- `/local/simulation/simulation-hermes-agent-expectation-trace/results.md`
- `/local/simulation/simulation-hermes-agent-expectation-trace/patches/expectation_trace_second_node.py`
- `/local/simulation/simulation-hermes-agent-expectation-trace/rubrics/recovery_diagnostics_rubric.md`
- `/local/simulation/simulation-hermes-agent-expectation-trace/dashboard/index.html`
- `/local/simulation/simulation-hermes-agent-expectation-trace/docs/index.html`

## Artifact Checks Passed

The Lab v1 pass verifies:

- Required file existence.
- JSON parsing for `manifest.json`, `study.json`, `issue_inputs.json`, `tasks.json`, `comparisons.json`, `metrics.json`, `conclusions.json`, and `chart_spec.json`.
- JSONL parsing for `runs.jsonl` and `traces.jsonl`.
- Dashboard data parsing for `dashboard/data/metrics.json`, `dashboard/data/comparisons.json`, `dashboard/data/issue_inputs.json`, and `dashboard/data/traces.jsonl`.
- Metrics consistency at the Lab v1 level:
  - total_tasks: 12
  - github_issue_tasks: 12
  - controlled_simulation_tasks: 0
  - total_expectation_traces: 24

The lab metrics record these artifact validation counts:

- tests_passed: 3 artifact checks
- tests_failed: 0 artifact checks
- tests_skipped: 1 targeted pytest suite group

## Files Compiled

The following Python files compile with in-memory `compile(...)` checks:

- `/local/simulation/simulation-hermes-agent-expectation-trace/generate_lab_db.py`
- `/local/simulation/simulation-hermes-agent-expectation-trace/patches/expectation_trace_second_node.py`
- `/local/simulation/hermes-expectation-trace/expectation_trace_patch.py`

## Still Partial

- The lab uses bounded issue fixtures, not full production replays.
- Some fixtures are PR-backed or release-linked evidence rather than standalone issue bodies.
- The second-node patch is a simulation artifact, not an upstream Hermes-Agent patch.
- Surprise scoring and recovery-hint quality are heuristic.
- Failure detection rates are fixture annotations, not production reliability measurements.
- Validation counts are artifact checks, not Hermes-Agent product test coverage.
- Pytest remains unavailable in this local artifact environment, so targeted pytest suites were not run.
- Maintainer-rated scoring has not replaced the heuristic rubric yet.

## Must Not Be Claimed Yet

- Do not claim Hermes-Agent forecasts or discovers issues.
- Do not claim Hermes-Agent implements the LeWorldModel paper.
- Do not claim the patch establishes production recovery.
- Do not claim the patch changes planning.
- Do not claim the metrics are production incident rates.
- Do not claim the validation counts are full test coverage.
- Do not claim statistical generalization beyond the selected Lab v1 fixtures.
- Do not claim production superiority or runtime superiority.

## Runnable Status

The lab is runnable as a deterministic artifact generator:

```bash
cd /local/simulation/simulation-hermes-agent-expectation-trace
python3 generate_lab_db.py
```

Running the generator rewrites the structured lab database from the fixed issue fixture set.
