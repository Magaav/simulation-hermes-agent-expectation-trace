# Data Dictionary

## Overview

This lab database is the canonical structured output for an issue-driven Expectation Trace experiment. GitHub issues, PR-backed regression reports, and release-linked evidence are inputs to the simulation. The second node is patched with a measurement-only expected-vs-actual observer.

Status: partial.

## Source Data Files

### manifest.json

Indexes artifacts, local paths, project status, and honesty notes.

### issue_inputs.json

The issue evidence used as simulation input. This is the primary source file for the corrected methodology.

Important fields:

- id: Stable fixture identifier.
- source_url: Primary URL used by the fixture.
- source_type: issue, pr, or release_linked.
- category: Failure category used by the harness.
- expected_behavior: Expected behavior extracted from the issue, PR, or release-linked evidence.
- observed_failure: Observed failure behavior extracted from the issue, PR, or release-linked evidence.
- evidence_quality: high, medium, or low evidence strength for fixture scoring.
- success_criteria: Diagnostic success condition for the fixture.
- scoring_notes: Notes describing why fixture-level heuristic scores were assigned.
- issue_number, issue_url, evidence_url, source_basis, issue_summary, trace_hint: compatibility and provenance fields retained for inspection.

### tasks.json

Task catalog derived from issue_inputs.json. Each selected task has source=github_issue for compatibility with the earlier lab schema; use issue_inputs.json source_type to distinguish issue, PR, and release-linked fixtures.

### runs.jsonl

One row per node run. Every selected issue input has a baseline run and a patched second-node run.

### traces.jsonl

One row per Expectation Trace transition emitted by the patched second node. Baseline runs intentionally do not emit these rows.

## Derived Data Files

### comparisons.json

Per-issue comparison of the baseline representation versus patched second-node behavior.

### metrics.json

Aggregate metrics computed from tasks, runs, and traces.

### conclusions.json

Scientific interpretation and honesty layer.

### chart_spec.json

Dashboard panel contract.

### rubrics/recovery_diagnostics_rubric.md

Human-readable scoring rubric for failure detection, recovery hint quality, diagnosis step count, evidence quality, and inconclusive fixtures.

## Scoring Rules

### recovery_hint_quality

- 0: no actionable recovery hint.
- 1: generic or weak hint.
- 2: useful but incomplete hint.
- 3: specific actionable hint naming the violated precondition and repair path.

### surprise_score

Heuristic mismatch score from 0.0 to 1.0. It is issue-input diagnostic scoring, not issue discovery.

- 0.00 to 0.33: low surprise.
- 0.34 to 0.66: medium surprise.
- 0.67 to 1.00: high surprise.

### time_to_diagnosis_steps

Conceptual count of issue-harness steps before a useful diagnosis appears. Lower is better.

## Patch Artifact

patches/expectation_trace_second_node.py and /local/simulation/hermes-expectation-trace/expectation_trace_patch.py contain the measurement-only second-node patch used by the simulation.

## Known Limitations

- Small issue set.
- Bounded fixtures, not full production replay.
- Some evidence is PR-backed or release-linked.
- Surprise scoring is heuristic.
- Pytest unavailable.
- No learned latent model.
- No CEM planning.
- No long-horizon evaluation.
