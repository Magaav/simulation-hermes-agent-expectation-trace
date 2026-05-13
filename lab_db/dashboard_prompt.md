# Dashboard Generation Prompt

You are given a scientific lab database from an experiment named:

    Expectation Trace Lab

Your task is to generate a serious scientific dashboard from the structured files in this directory.

Use these files:
- manifest.json
- study.json
- issue_inputs.json
- tasks.json
- runs.jsonl
- traces.jsonl
- comparisons.json
- metrics.json
- conclusions.json
- chart_spec.json

Dashboard goal:
Visualize whether a minimal JEPA/LeWorldModel-inspired Expectation Trace patch produced higher fixture-level diagnostic and recovery-hint scores than the baseline representation on the same issue inputs.

Important scientific constraints:
- Do not overclaim.
- Do not say Hermes-Agent has a full world model.
- Do not say the system predicts issues.
- Issues are inputs to the simulation.
- Treat all metrics as fixture-level heuristic scores, not production reliability measurements.
- Treat validation counts as artifact checks, not full product test coverage.
- Distinguish live issue bodies, issue-closing PRs, and release-linked evidence.
- Show inconclusive or weak evidence clearly.
- Include limitations prominently.
- Prefer measured language: "preliminary evidence", "supports", "mixed", "inconclusive".
- Use conclusions.json for scientific interpretation, but use manifest.json and VALIDATION.md as the stricter claim boundary.
- If interpretation files disagree, choose the narrower and less promotional claim.
- Use chart_spec.json as the authority for dashboard panels.
- Use issue_inputs.json for the issue evidence.
- Use metrics.json for aggregate charts.
- Use comparisons.json for per-issue comparison.
- Use traces.jsonl for expected-vs-actual examples.

Required dashboard sections:
1. Overview
2. Research Question
3. Method
4. Issue Inputs
5. Current Node vs Patched Second Node
6. Surprise Distribution
7. Per-Issue Results
8. Expected vs Actual Trace Examples
9. Failure Taxonomy
10. Scientific Conclusion
11. Limitations
12. Recommended Next PR

Visual tone:
Serious, clean, research-style.
No hype.
No fake certainty.
No "breakthrough" language unless explicitly supported by the data.

Core interpretation:
The experiment does not prove Hermes-Agent has LeWorldModel.
It evaluates whether a small expected-vs-actual runtime trace patch produces clearer structured diagnostics under the frozen Lab v0 fixture scoring rules.

Output:
Generate a dashboard-ready design or implementation using the available data.
