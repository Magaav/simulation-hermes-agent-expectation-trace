# Recovery Diagnostics Rubric

This rubric defines the Lab v1 fixture-level heuristic scores. It is intended for controlled comparison between a baseline representation and a patched second node with a LeWorldModel-inspired expectation trace observer.

The scores are not maintainer ratings yet. They should be treated as provisional until Hermes-Agent maintainers review or replace them.

## Failure Detection Score

Failure detection is recorded as a boolean in `runs.jsonl`.

- `true`: the run surfaces the fixture's relevant failure class or violated precondition.
- `false`: the run misses the relevant failure class, reports only an unrelated symptom, or leaves the issue ambiguous.

The aggregate failure detection rate in `metrics.json` is the fraction of fixture runs where `failure_detected` is `true`.

## Recovery Hint Quality Score

Recovery hint quality is scored from 0 to 3.

- `0`: no actionable recovery hint.
- `1`: generic or weak hint that names a broad symptom but not the violated precondition.
- `2`: useful but incomplete hint that points toward the right subsystem but omits a concrete guard, repair path, or boundary.
- `3`: specific actionable hint naming the violated precondition and a concrete repair path.

This is a fixture-level heuristic score. It is not evidence of production recovery and should be replaced by maintainer-rated scoring before stronger claims.

## Diagnosis Step Count

Diagnosis step count estimates how many issue-harness steps are needed before a useful diagnosis appears.

- Lower counts mean the run surfaces the likely violated precondition earlier in the fixture.
- Higher counts mean the run reaches the diagnosis only after later symptoms, retries, or ambiguous generic errors.

This is not runtime latency and not a production measurement.

## Evidence Quality

Evidence quality describes how strongly the source URL supports the fixture.

- `high`: the issue or PR title/body directly states the observed failure and expected behavior, or local regression tests are tied to the issue.
- `medium`: the source supports the failure class but leaves some details to linked context, title-level evidence, or local test interpretation.
- `low`: the fixture is based on PR or release-linked evidence where the issue body is not the primary source, or where the observed behavior is narrower than a full reproduction.

Evidence quality should be shown prominently in dashboards and maintainer review.

## Inconclusive Fixtures

Mark a fixture inconclusive when any of these are true:

- The source URL cannot be verified.
- The expected behavior or observed failure cannot be stated without speculation.
- The fixture cannot distinguish the relevant failure class from a generic runtime failure.
- The baseline representation and observer outputs cannot be compared on the same input.
- Maintainers dispute the category, success criteria, or recovery-hint score.

Inconclusive fixtures should remain in the dataset only with explicit notes, or be removed from aggregate comparisons.

## Why Scores Are Heuristic

Lab v1 converts issue history into fixed input fixtures and scores diagnostic usefulness from structured evidence. That makes the harness inspectable, but it does not make the scores authoritative.

The scores remain heuristic unless maintainers rate the same fixture outputs or replace the rubric with project-owned criteria.
