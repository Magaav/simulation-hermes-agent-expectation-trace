# Interview Notes

## Core Containment

The experiment uses GitHub issues and PR-backed reports as fixed inputs. It must not frame Expectation Trace as issue forecasting or discovery.

## Maintainer Questions

- Which issue classes should become acceptable fixed simulation fixtures?
- Should the second-node patch live as a plugin hook, a debug flag, or a harness-only wrapper?
- What fields make an issue trace useful in a PR review?
- Should maintainers rate recovery_hint_quality to calibrate the heuristic score?

## Suggested Demo

Pick one issue input, show the baseline representation, then show the patched second-node trace. Present the exact expected-vs-actual transition and recovery hint side by side.
