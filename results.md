# Expectation Trace Lab Results

## Lab Status

partial

## Key Metrics

These metrics are fixture-level heuristic scores from the controlled Lab v1 dataset. They are not production reliability measurements or statistical estimates.

- total_tasks: 12
- github_issue_tasks: 12
- controlled_simulation_tasks: 0
- baseline_runs: 12
- expectation_trace_runs: 12
- total_expectation_traces: 24
- baseline_failure_detection_rate: 0.83
- expectation_trace_failure_detection_rate: 1.00
- baseline_avg_recovery_hint_quality: 0.92
- expectation_trace_avg_recovery_hint_quality: 2.75
- baseline_avg_time_to_diagnosis_steps: 3.67
- expectation_trace_avg_time_to_diagnosis_steps: 1.00
- artifact_validation_checks_passed: 3
- artifact_validation_checks_failed: 0
- targeted_pytest_suites_skipped: 1

## Data Chain

- Issue fixtures: `lab_db/issue_inputs.json`
- Manifest and artifact index: `lab_db/manifest.json`
- Run records: `lab_db/runs.jsonl`
- Patched-node trace records: `lab_db/traces.jsonl`
- Derived comparisons and metrics: `lab_db/comparisons.json`, `lab_db/metrics.json`

## Per-Issue Result

The comparison label from `comparisons.json` is a fixture-scoring label, not a production benchmark result.

| Task | Category | Fixture-Scored Higher | Evidence | Interpretation |
| --- | --- | --- | --- | --- |
| T001 | context_mismatch | expectation_trace | medium | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T002 | platform_error | expectation_trace | medium | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T003 | auth_missing | expectation_trace | high | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T004 | malformed_output | expectation_trace | medium | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T005 | empty_output | expectation_trace | low | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T006 | secret_leak_risk | expectation_trace | low | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T007 | platform_error | expectation_trace | high | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T008 | platform_error | expectation_trace | medium | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T009 | provider_misconfigured | expectation_trace | high | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T010 | platform_error | expectation_trace | high | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T011 | context_mismatch | expectation_trace | high | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |
| T012 | secret_leak_risk | expectation_trace | high | Under the fixture-level heuristic scoring rules, the patched second node received a higher diagnostic/recovery score tied to issue evidence. |

## Method Correction

Issues are inputs to the simulation. The second node is patched with Expectation Trace and compared against the baseline representation on those same issue inputs. The experiment does not forecast or discover issues.

The baseline node is a baseline representation derived from issue and PR evidence, not a complete replay of production Hermes-Agent.

## Limitations

- Issue reports were converted into bounded fixtures, not fully replayed in production.
- Some inputs are PR-backed regression evidence rather than standalone open issue bodies.
- Surprise scoring is heuristic.
- Recovery-hint quality is heuristic and not yet maintainer-rated.
- Failure detection rate is a fixture annotation rate, not a production incident rate.
- Pytest was unavailable, so targeted pytest suites were skipped.
- No learned latent model, CEM planning, or long-horizon evaluation.
