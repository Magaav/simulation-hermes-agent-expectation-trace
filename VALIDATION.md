# Lab v0 Validation

Validation date: 2026-05-13

## Files Verified

Required Lab v0 files exist:

- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/issue_inputs.json`
- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/manifest.json`
- `/local/simulation/simulation-hermes-agent-expectation-trace/lab_db/dashboard_prompt.md`
- `/local/simulation/simulation-hermes-agent-expectation-trace/results.md`
- `/local/simulation/simulation-hermes-agent-expectation-trace/patches/expectation_trace_second_node.py`

## Artifact Checks Passed

The stabilization pass verified:

- Required file existence.
- JSON parsing for `manifest.json`, `study.json`, `issue_inputs.json`, `tasks.json`, `comparisons.json`, `metrics.json`, `conclusions.json`, and `chart_spec.json`.
- JSONL parsing for `runs.jsonl` and `traces.jsonl`.
- Metrics consistency at the Lab v0 level:
  - total_tasks: 6
  - github_issue_tasks: 6
  - controlled_simulation_tasks: 0
  - total_expectation_traces: 12

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
- Some fixtures are PR-backed or release-linked evidence rather than standalone live issue bodies.
- The second-node patch is a simulation artifact, not an upstream Hermes-Agent patch.
- Surprise scoring and recovery-hint quality are heuristic.
- Failure detection rates are fixture annotations, not production reliability measurements.
- Validation counts are artifact checks, not Hermes-Agent product test coverage.
- Pytest was unavailable, so targeted pytest suites were not run.
- No dashboard visuals have been generated.

## Must Not Be Claimed Yet

- Do not claim Hermes-Agent predicts issues.
- Do not claim Hermes-Agent implements LeWorldModel.
- Do not claim the patch proves production recovery.
- Do not claim the patch improves planning.
- Do not claim the metrics are production incident rates.
- Do not claim the validation counts are full test coverage.
- Do not claim statistical generalization beyond the six Lab v0 fixtures.

## Runnable Status

The lab is runnable as a deterministic artifact generator:

```bash
cd /local/simulation/simulation-hermes-agent-expectation-trace
python3 generate_lab_db.py
```

Running the generator rewrites the structured lab database from the fixed issue fixture set.
