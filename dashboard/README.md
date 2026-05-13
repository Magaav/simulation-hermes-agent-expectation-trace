# Expectation Trace Lab v0 Dashboard

This is a static, GitHub Pages-compatible dashboard for Lab v0.

It uses only local copied data files:

- `data/metrics.json`
- `data/comparisons.json`
- `data/traces.jsonl`
- `data/issue_inputs.json`

Run locally:

```bash
cd /local/simulation/simulation-hermes-agent-expectation-trace/dashboard
python3 -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080
```

Claim boundary:

Bounded simulation artifact. Not a production benchmark. Not proof of runtime superiority.
