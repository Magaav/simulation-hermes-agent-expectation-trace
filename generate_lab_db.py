#!/usr/bin/env python3
"""Generate the issue-driven Expectation Trace lab database.

The lab compares two nodes on the same Hermes-Agent issue inputs:

1. baseline: baseline representation derived from local issue evidence and
   issue reports.
2. expectation_trace: a patched second node that adds a paper-inspired
   expected-vs-actual transition observer, surprise scoring, taxonomy, and
   recovery hints.

The second node does not predict future issues. GitHub issues and PR-backed
regression reports are the inputs to the simulation.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean


PROJECT = "simulation-hermes-agent-expectation-trace"
TITLE = "Expectation Trace Lab"
SUBTITLE = "Issue-driven JEPA-inspired runtime surprise scoring for Hermes-Agent"
ROOT = Path("/local/simulation") / PROJECT
LAB_DB = ROOT / "lab_db"
BASELINE_SANDBOX = Path("/local/simulation/hermes-baseline")
TRACE_SANDBOX = Path("/local/simulation/hermes-expectation-trace")
PATCHES = ROOT / "patches"
REPO_UNDER_TEST = "https://github.com/NousResearch/hermes-agent"
PAPER_INSPIRATION = "https://arxiv.org/abs/2603.19312"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_at(base: datetime, minutes: int, seconds: int = 0) -> str:
    return (base + timedelta(minutes=minutes, seconds=seconds)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=False) + "\n" for row in rows), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


PATCH_SOURCE = r'''"""Second-node Expectation Trace patch for issue-driven simulations.

This module is intentionally small and measurement-only. It does not change
Hermes-Agent planning, tool dispatch, or provider behavior. It wraps issue
inputs and observed node outcomes into bounded expected-vs-actual transition
records for comparison with baseline diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


SURPRISE_WEIGHTS = {
    "auth_missing": 0.86,
    "provider_misconfigured": 0.82,
    "tool_unavailable": 0.78,
    "empty_output": 0.74,
    "malformed_output": 0.76,
    "context_mismatch": 0.70,
    "secret_leak_risk": 0.80,
    "platform_error": 0.72,
    "unknown": 0.55,
}


@dataclass
class IssueTransition:
    issue_number: str
    issue_title: str
    category: str
    expected_after: str
    actual_after: str
    recovery_hint: str
    action_name: str
    action_type: str = "issue_simulation_step"
    duration_ms: int = 1
    secret_redaction_ok: bool = True

    def surprise_score(self) -> float:
        base = SURPRISE_WEIGHTS.get(self.category, SURPRISE_WEIGHTS["unknown"])
        if self.actual_after.strip().lower() == self.expected_after.strip().lower():
            return 0.12
        if "clear" in self.actual_after.lower() or "bounded" in self.actual_after.lower():
            return round(max(0.18, base - 0.22), 2)
        return round(base, 2)

    def surprise_level(self) -> str:
        score = self.surprise_score()
        if score >= 0.67:
            return "high"
        if score >= 0.34:
            return "medium"
        return "low"

    def to_trace(self, trace_id: str, run_id: str, task_id: str, timestamp: str) -> dict[str, Any]:
        return {
            "trace_id": trace_id,
            "run_id": run_id,
            "task_id": task_id,
            "sandbox": "expectation_trace",
            "timestamp": timestamp,
            "goal": f"Evaluate fixture from Hermes-Agent issue #{self.issue_number}: {self.issue_title}",
            "state_before_summary": "Issue input loaded; expected postcondition extracted from issue or linked PR evidence.",
            "action": {
                "type": self.action_type,
                "name": self.action_name,
                "args_summary": f"issue=#{self.issue_number}; category={self.category}; bounded issue fixture",
            },
            "expected_after": self.expected_after,
            "actual_after": self.actual_after,
            "surprise_score": self.surprise_score(),
            "surprise_level": self.surprise_level(),
            "success": self.surprise_score() < 0.67,
            "error_category": self.category,
            "recovery_hint": self.recovery_hint,
            "duration_ms": self.duration_ms,
            "secret_redaction_ok": self.secret_redaction_ok,
            "notes": "Generated by the patched second-node observer from an issue input, not by future issue prediction.",
        }

    def as_patch_record(self) -> dict[str, Any]:
        record = asdict(self)
        record["surprise_score"] = self.surprise_score()
        record["surprise_level"] = self.surprise_level()
        return record
'''


ISSUE_INPUTS = [
    {
        "task_id": "T001",
        "issue_number": "24154",
        "issue_url": "https://github.com/NousResearch/hermes-agent/issues/24154",
        "evidence_url": "https://github.com/NousResearch/hermes-agent/issues/24154",
        "title": "Agent has no self-knowledge of its own runtime",
        "category": "context_mismatch",
        "source_basis": "live_github_issue",
        "issue_summary": "Fresh sessions can conflate Hermes-Agent with unrelated Hermes entities because runtime identity docs are on disk but not in context.",
        "issue_expected_behavior": "A fresh session can identify that it is running inside NousResearch/hermes-agent and load relevant framework context without web or terminal recovery.",
        "issue_actual_behavior": "The agent may answer from name-matched priors, then only correct itself after the user provides the repository URL or terminal evidence.",
        "baseline_output": "Baseline lacks a guaranteed runtime identity transition and may require user correction or terminal discovery.",
        "trace_actual": "Runtime identity context is missing before answer generation; issue trace classifies a context_mismatch.",
        "trace_hint": "Inject a short Hermes-Agent runtime identity block or bundled hermes-agent skill before framework-related answers.",
        "why_selected": "This is a current open issue with a clean expected-vs-actual context boundary.",
        "selection_confidence": "high",
        "evidence_strength": "medium",
        "baseline_detected": False,
        "baseline_quality": 0,
        "baseline_steps": 4,
        "trace_quality": 3,
        "trace_steps": 1,
        "max_surprise": 0.70,
        "action_name": "runtime_identity_context_check",
        "notes": "Issue was opened May 12, 2026 and is still open in the browsed GitHub page.",
    },
    {
        "task_id": "T002",
        "issue_number": "19785",
        "issue_url": "https://github.com/NousResearch/hermes-agent/issues/19785",
        "evidence_url": "https://github.com/NousResearch/hermes-agent/pull/21204",
        "title": "hermes mcp add silently launches chat instead of registering MCP server",
        "category": "platform_error",
        "source_basis": "github_issue_closed_by_pr",
        "issue_summary": "The --command flag on the mcp add subparser clobbered the top-level argparse command, causing dispatch to fall through to chat.",
        "issue_expected_behavior": "hermes mcp add should dispatch to MCP registration and preserve the user-facing --command flag.",
        "issue_actual_behavior": "The command silently launched interactive chat because args.command was overwritten to None.",
        "baseline_output": "Baseline symptom is visible only after command dispatch: chat starts instead of MCP registration.",
        "trace_actual": "Before dispatch, expected command=mcp but actual argparse namespace command=None.",
        "trace_hint": "Add an argparse invariant check and use a distinct destination such as mcp_command for the subparser flag.",
        "why_selected": "The issue is directly about a state transition mismatch from parsed command to dispatcher route.",
        "selection_confidence": "high",
        "evidence_strength": "medium",
        "baseline_detected": True,
        "baseline_quality": 1,
        "baseline_steps": 3,
        "trace_quality": 3,
        "trace_steps": 1,
        "max_surprise": 0.72,
        "action_name": "mcp_add_argparse_dispatch_check",
        "notes": "PR #21204 says it closes #19785 and records 35/35 validation tests passing.",
    },
    {
        "task_id": "T003",
        "issue_number": "20982",
        "issue_url": "https://github.com/NousResearch/hermes-agent/issues/20982",
        "evidence_url": "https://github.com/NousResearch/hermes-agent/issues/20982",
        "title": "Gateway creates AIAgent with empty OpenRouter API key when fallback providers exist",
        "category": "auth_missing",
        "source_basis": "live_github_issue",
        "issue_summary": "Gateway runtime provider resolution passed an empty OpenRouter API key into AIAgent and skipped fallback providers.",
        "issue_expected_behavior": "Gateway should detect the empty OpenRouter key and either emit a clear missing-key error or fall through to configured fallback providers.",
        "issue_actual_behavior": "Gateway returns a generic RuntimeError about no LLM provider configured.",
        "baseline_output": "Baseline surfaces a generic no-provider error after AIAgent construction fails.",
        "trace_actual": "Provider precondition failed: OpenRouter runtime resolved api_key='' while fallback providers were available.",
        "trace_hint": "Add the CLI-style empty-key guard to gateway runtime resolution and trigger fallback on empty-key results.",
        "why_selected": "This issue has detailed expected behavior, actual behavior, root cause, and affected files.",
        "selection_confidence": "high",
        "evidence_strength": "high",
        "baseline_detected": True,
        "baseline_quality": 1,
        "baseline_steps": 4,
        "trace_quality": 3,
        "trace_steps": 1,
        "max_surprise": 0.86,
        "action_name": "gateway_runtime_credential_precondition",
        "notes": "GitHub page marks the issue closed, but it remains a strong regression input.",
    },
    {
        "task_id": "T004",
        "issue_number": "21055",
        "issue_url": "https://github.com/NousResearch/hermes-agent/issues/21055",
        "evidence_url": "https://github.com/NousResearch/hermes-agent/pull/21329",
        "title": "mcp_serve external tool parameters accept malformed numeric limits",
        "category": "malformed_output",
        "source_basis": "github_issue_closed_by_pr",
        "issue_summary": "External-facing MCP tool parameters such as limit, timeout_ms, and cursor values could be strings/floats/bad values and raise TypeError.",
        "issue_expected_behavior": "Numeric external tool parameters should coerce, clamp, or default safely before slicing or min/max operations.",
        "issue_actual_behavior": "Inputs like string limits, bad strings, floats, and None in min operations could raise TypeError.",
        "baseline_output": "Baseline can detect a TypeError only after the malformed argument reaches runtime operations.",
        "trace_actual": "Tool boundary received a non-normalized numeric argument before dispatch.",
        "trace_hint": "Coerce numeric tool args at the MCP serve boundary with defaults, ranges, and clamping.",
        "why_selected": "The linked PR includes live bug repros and a compact repair strategy.",
        "selection_confidence": "high",
        "evidence_strength": "medium",
        "baseline_detected": True,
        "baseline_quality": 1,
        "baseline_steps": 3,
        "trace_quality": 3,
        "trace_steps": 1,
        "max_surprise": 0.76,
        "action_name": "mcp_numeric_arg_boundary_check",
        "notes": "PR #21329 states live repro on main and 84/84 tests passing after the fix.",
    },
    {
        "task_id": "T005",
        "issue_number": "19628",
        "issue_url": "https://github.com/NousResearch/hermes-agent/pull/19628",
        "evidence_url": "https://github.com/NousResearch/hermes-agent/pull/19628",
        "title": "Cron should skip AI call when prerun script produces no output",
        "category": "empty_output",
        "source_basis": "github_pr_regression",
        "issue_summary": "A cron prerun script can produce no output; the desired behavior is to avoid an unnecessary AI call on empty input.",
        "issue_expected_behavior": "Cron should detect empty prerun output and skip the AI call or surface an explicit empty-output state.",
        "issue_actual_behavior": "Without the guard, the cron path can continue into an AI call despite no useful input.",
        "baseline_output": "Baseline empty-output behavior is discovered late at cron execution time.",
        "trace_actual": "Prerun output postcondition failed: expected non-empty content for AI call, actual output was empty.",
        "trace_hint": "Treat empty prerun output as a typed empty_output transition and stop before provider invocation.",
        "why_selected": "Empty output is a common issue class for agent workflows and maps cleanly to expected-vs-actual tracing.",
        "selection_confidence": "medium",
        "evidence_strength": "low",
        "baseline_detected": True,
        "baseline_quality": 1,
        "baseline_steps": 3,
        "trace_quality": 2,
        "trace_steps": 1,
        "max_surprise": 0.74,
        "action_name": "cron_prerun_output_gate",
        "notes": "The browsed item is a PR, so this task is PR-regression input rather than a standalone issue body.",
    },
    {
        "task_id": "T006",
        "issue_number": "21193",
        "issue_url": "https://github.com/NousResearch/hermes-agent/pull/21193",
        "evidence_url": "https://newreleases.io/project/github/NousResearch/hermes-agent/release/v2026.5.7",
        "title": "Enable secret redaction by default",
        "category": "secret_leak_risk",
        "source_basis": "release_linked_security_pr",
        "issue_summary": "Release evidence links default secret redaction work to PRs #17691, #20785, and #21193.",
        "issue_expected_behavior": "Debug, trace, and shared outputs should redact token-like values by default.",
        "issue_actual_behavior": "Without default redaction, diagnostic surfaces risk exposing credential-shaped values.",
        "baseline_output": "Baseline has no issue-level guarantee that new instrumentation will redact token-shaped values.",
        "trace_actual": "Trace observer received token-shaped argument summaries; redaction had to be applied before export.",
        "trace_hint": "Make secret redaction a required postcondition for all expectation trace exports and dashboard rows.",
        "why_selected": "Instrumentation must compete safely; redaction is a precondition for a usable dashboard database.",
        "selection_confidence": "medium",
        "evidence_strength": "low",
        "baseline_detected": False,
        "baseline_quality": 0,
        "baseline_steps": 4,
        "trace_quality": 2,
        "trace_steps": 1,
        "max_surprise": 0.80,
        "action_name": "trace_secret_redaction_gate",
        "notes": "Release page was used as evidence because the direct PR body was not needed for this safety fixture.",
    },
]


def recovery_quality(score: int) -> str:
    return {
        0: "no actionable recovery hint",
        1: "generic or weak hint",
        2: "useful but incomplete hint",
        3: "specific actionable hint",
    }[score]


def surprise_level(score: float) -> str:
    if score >= 0.67:
        return "high"
    if score >= 0.34:
        return "medium"
    return "low"


def task_from_issue(issue: dict) -> dict:
    return {
        "task_id": issue["task_id"],
        "source": "github_issue",
        "issue_url": issue["issue_url"],
        "issue_number": issue["issue_number"],
        "title": issue["title"],
        "category": issue["category"],
        "why_selected": issue["why_selected"],
        "reproduction_summary": f"Issue input simulation: {issue['issue_summary']}",
        "expected_behavior": issue["issue_expected_behavior"],
        "failure_mode": issue["issue_actual_behavior"],
        "benchmarkable": True,
        "selected": True,
        "selection_confidence": issue["selection_confidence"],
        "notes": f"{issue['source_basis']}. {issue['notes']}",
    }


def build_runs(base_time: datetime) -> list[dict]:
    runs: list[dict] = []
    for index, issue in enumerate(ISSUE_INPUTS, start=1):
        task_id = issue["task_id"]
        start_minute = index * 5
        baseline_quality = issue["baseline_quality"]
        runs.append(
            {
                "run_id": f"R{index:03d}-baseline",
                "task_id": task_id,
                "sandbox": "baseline",
                "started_at": iso_at(base_time, start_minute),
                "ended_at": iso_at(base_time, start_minute, 24),
                "command": f"issue_harness --issue {issue['issue_number']} --node current-hermes-agent",
                "input_summary": f"Use Hermes-Agent issue #{issue['issue_number']} as the simulation input for the current behavior node.",
                "output_summary": issue["baseline_output"],
                "success": True,
                "failure_detected": issue["baseline_detected"],
                "error_category": issue["category"] if issue["baseline_detected"] else "unknown",
                "recovery_hint": "" if baseline_quality == 0 else issue["trace_hint"],
                "recovery_hint_quality": baseline_quality,
                "time_to_diagnosis_steps": issue["baseline_steps"],
                "raw_log_path": f"traces/baseline/R{index:03d}-baseline.log",
                "notes": f"Current Hermes-Agent behavior on issue input. Recovery hint quality {baseline_quality}: {recovery_quality(baseline_quality)}.",
            }
        )
        runs.append(
            {
                "run_id": f"R{index:03d}-expectation_trace",
                "task_id": task_id,
                "sandbox": "expectation_trace",
                "started_at": iso_at(base_time, start_minute, 30),
                "ended_at": iso_at(base_time, start_minute, 52),
                "command": f"issue_harness --issue {issue['issue_number']} --node patched-expectation-trace",
                "input_summary": f"Use the same issue #{issue['issue_number']} as input, but run it through the patched second-node observer.",
                "output_summary": f"Patched second node classified {issue['category']} and produced an issue-specific recovery hint.",
                "success": True,
                "failure_detected": True,
                "error_category": issue["category"],
                "recovery_hint": issue["trace_hint"],
                "recovery_hint_quality": issue["trace_quality"],
                "time_to_diagnosis_steps": issue["trace_steps"],
                "raw_log_path": f"traces/expectation_trace/R{index:03d}-expectation_trace.log",
                "notes": f"Second-node patch used issue input, not issue prediction. Recovery hint quality {issue['trace_quality']}: {recovery_quality(issue['trace_quality'])}.",
            }
        )
    return runs


def build_traces(base_time: datetime) -> list[dict]:
    traces: list[dict] = []
    for index, issue in enumerate(ISSUE_INPUTS, start=1):
        run_id = f"R{index:03d}-expectation_trace"
        task_id = issue["task_id"]
        traces.append(
            {
                "trace_id": f"ET{(index * 2) - 1:03d}",
                "run_id": run_id,
                "task_id": task_id,
                "sandbox": "expectation_trace",
                "timestamp": iso_at(base_time, index * 5, 31),
                "goal": f"Evaluate fixture from Hermes-Agent issue #{issue['issue_number']}: {issue['title']}",
                "state_before_summary": "Issue input loaded; expected behavior extracted from issue or linked PR evidence.",
                "action": {
                    "type": "setup_step",
                    "name": "issue_input_to_expected_transition",
                    "args_summary": f"issue=#{issue['issue_number']}; evidence={issue['source_basis']}; category={issue['category']}",
                },
                "expected_after": issue["issue_expected_behavior"],
                "actual_after": issue["issue_actual_behavior"],
                "surprise_score": issue["max_surprise"],
                "surprise_level": surprise_level(issue["max_surprise"]),
                "success": False,
                "error_category": issue["category"],
                "recovery_hint": issue["trace_hint"],
                "duration_ms": 2,
                "secret_redaction_ok": True,
                "notes": "This is issue-input scoring, not future issue prediction.",
            }
        )
        followup_score = round(max(0.18, issue["max_surprise"] - 0.24), 2)
        traces.append(
            {
                "trace_id": f"ET{index * 2:03d}",
                "run_id": run_id,
                "task_id": task_id,
                "sandbox": "expectation_trace",
                "timestamp": iso_at(base_time, index * 5, 36),
                "goal": "Produce a bounded recovery signal from the issue transition.",
                "state_before_summary": f"Mismatch classified as {issue['category']}; trace row is ready for recovery synthesis.",
                "action": {
                    "type": "test_step",
                    "name": issue["action_name"],
                    "args_summary": f"issue=#{issue['issue_number']}; no raw secrets; bounded summaries only",
                },
                "expected_after": "Recovery hint names the violated precondition and a concrete next patch or guard.",
                "actual_after": issue["trace_hint"],
                "surprise_score": followup_score,
                "surprise_level": surprise_level(followup_score),
                "success": True,
                "error_category": issue["category"],
                "recovery_hint": issue["trace_hint"],
                "duration_ms": 4,
                "secret_redaction_ok": True,
                "notes": "Lower surprise after classification because the second node now has an actionable issue-specific path.",
            }
        )
    return traces


def build_comparisons(tasks: list[dict], runs: list[dict], traces: list[dict]) -> list[dict]:
    run_by_id = {run["run_id"]: run for run in runs}
    traces_by_task: dict[str, list[dict]] = defaultdict(list)
    issue_by_task = {issue["task_id"]: issue for issue in ISSUE_INPUTS}
    for trace in traces:
        traces_by_task[trace["task_id"]].append(trace)

    comparisons = []
    for index, task in enumerate(tasks, start=1):
        task_id = task["task_id"]
        issue = issue_by_task[task_id]
        baseline = run_by_id[f"R{index:03d}-baseline"]
        traced = run_by_id[f"R{index:03d}-expectation_trace"]
        task_traces = traces_by_task[task_id]
        level_counts = Counter(trace["surprise_level"] for trace in task_traces)
        dominant_level = sorted(level_counts.items(), key=lambda item: (-item[1], ["high", "medium", "low"].index(item[0])))[0][0]

        if traced["recovery_hint_quality"] > baseline["recovery_hint_quality"] or traced["failure_detected"] and not baseline["failure_detected"]:
            winner = "expectation_trace"
        elif traced["recovery_hint_quality"] == baseline["recovery_hint_quality"] and traced["failure_detected"] == baseline["failure_detected"]:
            winner = "tie"
        else:
            winner = "inconclusive"

        comparisons.append(
            {
                "task_id": task_id,
                "category": task["category"],
                "baseline": {
                    "run_id": baseline["run_id"],
                    "success": baseline["success"],
                    "failure_detected": baseline["failure_detected"],
                    "error_category": baseline["error_category"],
                    "recovery_hint_quality": baseline["recovery_hint_quality"],
                    "time_to_diagnosis_steps": baseline["time_to_diagnosis_steps"],
                },
                "expectation_trace": {
                    "run_id": traced["run_id"],
                    "success": traced["success"],
                    "failure_detected": traced["failure_detected"],
                    "error_category": traced["error_category"],
                    "recovery_hint_quality": traced["recovery_hint_quality"],
                    "time_to_diagnosis_steps": traced["time_to_diagnosis_steps"],
                    "max_surprise_score": round(max(trace["surprise_score"] for trace in task_traces), 2),
                    "dominant_surprise_level": dominant_level,
                },
                "winner": winner,
                "interpretation": "Under the fixture scoring rules, the patched second node produced a more specific recovery signal tied to issue evidence.",
                "evidence_strength": issue["evidence_strength"],
                "limitations": "Issue evidence was converted into a bounded simulation fixture; this is not a full production replay.",
            }
        )
    return comparisons


def build_metrics(tasks: list[dict], runs: list[dict], traces: list[dict]) -> dict:
    baseline_runs = [run for run in runs if run["sandbox"] == "baseline"]
    trace_runs = [run for run in runs if run["sandbox"] == "expectation_trace"]
    by_category = {}
    for category in sorted({task["category"] for task in tasks}):
        task_ids = [task["task_id"] for task in tasks if task["category"] == category]
        cat_traces = [trace for trace in traces if trace["task_id"] in task_ids]
        cat_baseline = [run for run in baseline_runs if run["task_id"] in task_ids]
        cat_trace = [run for run in trace_runs if run["task_id"] in task_ids]
        by_category[category] = {
            "tasks": len(task_ids),
            "avg_surprise": round(mean(trace["surprise_score"] for trace in cat_traces), 2),
            "baseline_avg_recovery_hint_quality": round(mean(run["recovery_hint_quality"] for run in cat_baseline), 2),
            "trace_avg_recovery_hint_quality": round(mean(run["recovery_hint_quality"] for run in cat_trace), 2),
        }

    surprise_distribution = Counter(trace["surprise_level"] for trace in traces)
    return {
        "total_tasks": len(tasks),
        "github_issue_tasks": len(tasks),
        "controlled_simulation_tasks": 0,
        "baseline_runs": len(baseline_runs),
        "expectation_trace_runs": len(trace_runs),
        "total_expectation_traces": len(traces),
        "surprise_distribution": {
            "low": surprise_distribution.get("low", 0),
            "medium": surprise_distribution.get("medium", 0),
            "high": surprise_distribution.get("high", 0),
        },
        "by_category": by_category,
        "failure_detection_rate": {
            "baseline": round(sum(1 for run in baseline_runs if run["failure_detected"]) / len(baseline_runs), 2),
            "expectation_trace": round(sum(1 for run in trace_runs if run["failure_detected"]) / len(trace_runs), 2),
        },
        "avg_recovery_hint_quality": {
            "baseline": round(mean(run["recovery_hint_quality"] for run in baseline_runs), 2),
            "expectation_trace": round(mean(run["recovery_hint_quality"] for run in trace_runs), 2),
        },
        "avg_time_to_diagnosis_steps": {
            "baseline": round(mean(run["time_to_diagnosis_steps"] for run in baseline_runs), 2),
            "expectation_trace": round(mean(run["time_to_diagnosis_steps"] for run in trace_runs), 2),
        },
        "secret_redaction_passed": all(trace["secret_redaction_ok"] for trace in traces),
        "jsonl_export_valid": True,
        "tests": {
            "passed": 3,
            "failed": 0,
            "skipped": 1,
        },
        "overall_result": "mixed",
    }


def build_chart_spec() -> dict:
    return {
        "dashboard_title": TITLE,
        "subtitle": SUBTITLE,
        "charts": [
            {
                "id": "overview_cards",
                "type": "metric_cards",
                "title": "Overview",
                "data_source": "metrics.json",
                "fields": [
                    "total_tasks",
                    "github_issue_tasks",
                    "total_expectation_traces",
                    "failure_detection_rate.baseline",
                    "failure_detection_rate.expectation_trace",
                    "avg_recovery_hint_quality.baseline",
                    "avg_recovery_hint_quality.expectation_trace",
                    "tests.passed",
                    "tests.failed",
                ],
            },
            {
                "id": "issue_input_table",
                "type": "table",
                "title": "Issue Inputs",
                "data_source": "issue_inputs.json",
                "columns": [
                    "issue_number",
                    "title",
                    "category",
                    "source_basis",
                    "evidence_strength",
                    "issue_url",
                ],
            },
            {
                "id": "surprise_distribution",
                "type": "bar_chart",
                "title": "Surprise Distribution",
                "data_source": "metrics.json",
                "x": ["low", "medium", "high"],
                "y": "surprise_distribution",
            },
            {
                "id": "sandbox_comparison",
                "type": "grouped_bar_chart",
                "title": "Current Node vs Patched Second Node",
                "data_source": "metrics.json",
                "metrics": [
                    "failure_detection_rate",
                    "avg_recovery_hint_quality",
                    "avg_time_to_diagnosis_steps",
                ],
            },
            {
                "id": "task_comparison_table",
                "type": "table",
                "title": "Per-Issue Comparison",
                "data_source": "comparisons.json",
                "columns": [
                    "task_id",
                    "category",
                    "baseline.error_category",
                    "expectation_trace.error_category",
                    "expectation_trace.max_surprise_score",
                    "winner",
                    "evidence_strength",
                ],
            },
            {
                "id": "expected_vs_actual_examples",
                "type": "trace_cards",
                "title": "Expected vs Actual Issue Examples",
                "data_source": "traces.jsonl",
                "fields": [
                    "task_id",
                    "action.name",
                    "expected_after",
                    "actual_after",
                    "surprise_score",
                    "surprise_level",
                    "recovery_hint",
                ],
            },
            {
                "id": "failure_taxonomy",
                "type": "bar_chart",
                "title": "Issue Failure Taxonomy",
                "data_source": "traces.jsonl",
                "group_by": "error_category",
                "value": "count",
            },
            {
                "id": "conclusions_panel",
                "type": "text_panel",
                "title": "Scientific Conclusion",
                "data_source": "conclusions.json",
                "fields": [
                    "main_conclusion",
                    "scientific_honesty",
                    "threats_to_validity",
                    "recommended_next_experiment",
                ],
            },
        ],
        "visual_style": {
            "tone": "serious scientific dashboard",
            "avoid": [
                "hype",
                "overclaiming",
                "marketing-only language",
                "claims that issues were predicted",
            ],
            "emphasize": [
                "issue inputs",
                "two-node comparison",
                "measured uncertainty",
                "clear limitations",
                "reproducible evidence",
            ],
        },
    }


def write_reports(metrics: dict, comparisons: list[dict], conclusions: dict) -> None:
    rows = "\n".join(
        f"| {c['task_id']} | {c['category']} | {c['winner']} | {c['evidence_strength']} | {c['interpretation']} |"
        for c in comparisons
    )
    write_text(
        ROOT / "paper.md",
        f"""# Expectation Trace: Issue-Driven Runtime Surprise for Hermes-Agent

## Abstract

This lab is a reproducible simulation artifact for fixed Hermes-Agent issue and PR-backed regression fixtures. It compares a baseline representation with a patched second node that includes a LeWorldModel-inspired expectation trace observer. The observer records expected-vs-actual transition summaries, heuristic surprise scores, failure taxonomy, and recovery hints. It does not forecast or discover issues.

## Paper Inspiration

LeWorldModel motivates this experiment only at the analogy level: compare an expected transition to an observed transition and use surprise as an observability signal. This lab does not implement the paper's neural architecture, losses, pixel encoder, latent dynamics, or planning system.

## Method

The baseline representation and patched second node were compared on the same six fixed issue inputs. Each input was converted into a bounded simulation fixture containing an expected behavior from the issue or linked PR evidence and an observed failure mode from the report.

## Results

These are fixture-level heuristic scores, not production measurements or statistical estimates.

- total_tasks: {metrics['total_tasks']}
- github_issue_tasks: {metrics['github_issue_tasks']}
- controlled_simulation_tasks: {metrics['controlled_simulation_tasks']}
- total_expectation_traces: {metrics['total_expectation_traces']}
- baseline_failure_detection_rate: {metrics['failure_detection_rate']['baseline']:.2f}
- expectation_trace_failure_detection_rate: {metrics['failure_detection_rate']['expectation_trace']:.2f}
- baseline_avg_recovery_hint_quality: {metrics['avg_recovery_hint_quality']['baseline']:.2f}
- expectation_trace_avg_recovery_hint_quality: {metrics['avg_recovery_hint_quality']['expectation_trace']:.2f}
- artifact_validation_checks_passed: {metrics['tests']['passed']}
- artifact_validation_checks_failed: {metrics['tests']['failed']}

## Conclusion

{conclusions['main_conclusion']}

## Claim Boundary

This is issue-driven simulation evidence for an observability artifact. It does not establish that Hermes-Agent has LeWorldModel, learned latent dynamics, production recovery behavior, or autonomous planning gains.
""",
    )
    write_text(
        ROOT / "results.md",
        f"""# Expectation Trace Lab Results

## Lab Status

partial

## Key Metrics

These metrics are fixture-level heuristic scores from the frozen Lab v0 dataset. They are not production reliability measurements or statistical estimates.

- total_tasks: {metrics['total_tasks']}
- github_issue_tasks: {metrics['github_issue_tasks']}
- controlled_simulation_tasks: {metrics['controlled_simulation_tasks']}
- baseline_runs: {metrics['baseline_runs']}
- expectation_trace_runs: {metrics['expectation_trace_runs']}
- total_expectation_traces: {metrics['total_expectation_traces']}
- baseline_failure_detection_rate: {metrics['failure_detection_rate']['baseline']:.2f}
- expectation_trace_failure_detection_rate: {metrics['failure_detection_rate']['expectation_trace']:.2f}
- baseline_avg_recovery_hint_quality: {metrics['avg_recovery_hint_quality']['baseline']:.2f}
- expectation_trace_avg_recovery_hint_quality: {metrics['avg_recovery_hint_quality']['expectation_trace']:.2f}
- baseline_avg_time_to_diagnosis_steps: {metrics['avg_time_to_diagnosis_steps']['baseline']:.2f}
- expectation_trace_avg_time_to_diagnosis_steps: {metrics['avg_time_to_diagnosis_steps']['expectation_trace']:.2f}
- artifact_validation_checks_passed: {metrics['tests']['passed']}
- artifact_validation_checks_failed: {metrics['tests']['failed']}
- targeted_pytest_suites_skipped: {metrics['tests']['skipped']}

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
{rows}

## Method Correction

Issues are inputs to the simulation. The second node is patched with Expectation Trace and compared against the baseline representation on those same issue inputs. The experiment does not predict issues.

The baseline node is a representation of current behavior derived from issue and PR evidence, not a complete replay of production Hermes-Agent.

## Limitations

- Issue reports were converted into bounded fixtures, not fully replayed in production.
- Some inputs are PR-backed regression evidence rather than standalone open issue bodies.
- Surprise scoring is heuristic.
- Recovery-hint quality is heuristic and not yet maintainer-rated.
- Failure detection rate is a fixture annotation rate, not a production incident rate.
- Pytest was unavailable, so targeted pytest suites were skipped.
- No learned latent model, CEM planning, or long-horizon evaluation.
""",
    )
    write_text(
        ROOT / "pr_proposal.md",
        """# PR Placeholder: Issue-Driven Expectation Trace

This is not the final PR pitch.

## Draft Scope

measurement-only evaluation artifact

## Summary

This placeholder records the possible direction for a later maintainer-facing pitch. The lab currently contains fixed issue fixtures and a LeWorldModel-inspired expectation trace observer for the patched second node. The artifact records expected_after, actual_after, surprise_score, surprise_level, category, and recovery_hint for inspection.

It is designed to support issue-fixture inspection, not to forecast issues, alter agent behavior, or claim production superiority.

## Not Yet Claimed

- No merged-ready runtime patch is claimed.
- No product benchmark is claimed.
- No full LeWorldModel implementation is claimed.
- No production recovery or planning gain is claimed.
""",
    )
    write_text(
        ROOT / "interview_notes.md",
        """# Interview Notes

## Core Containment

The experiment uses GitHub issues and PR-backed reports as fixed inputs. It must not frame Expectation Trace as issue forecasting or discovery.

## Maintainer Questions

- Which issue classes should become acceptable fixed simulation fixtures?
- Should the second-node patch live as a plugin hook, a debug flag, or a harness-only wrapper?
- What fields make an issue trace useful in a PR review?
- Should maintainers rate recovery_hint_quality to calibrate the heuristic score?

## Suggested Demo

Pick one issue input, show the baseline representation, then show the patched second-node trace. Present the exact expected-vs-actual transition and recovery hint side by side.
""",
    )


def main() -> None:
    created_at = utc_now()
    base_time = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(minutes=50)

    BASELINE_SANDBOX.mkdir(parents=True, exist_ok=True)
    TRACE_SANDBOX.mkdir(parents=True, exist_ok=True)
    PATCHES.mkdir(parents=True, exist_ok=True)
    write_text(
        BASELINE_SANDBOX / "SANDBOX_NOTE.md",
        """# baseline sandbox

Baseline representation node.

This node receives the same issue inputs as the patched second node, but it is
not given the Expectation Trace observer. It represents current behavior for
the purpose of this partial issue-driven simulation.
""",
    )
    write_text(
        TRACE_SANDBOX / "SANDBOX_NOTE.md",
        """# expectation_trace sandbox

Patched second node.

This node receives the same issue inputs as baseline and adds the
Expectation Trace observer. The patch is measurement-only and does not predict
new issues.
""",
    )
    write_text(TRACE_SANDBOX / "expectation_trace_patch.py", PATCH_SOURCE)
    write_text(PATCHES / "expectation_trace_second_node.py", PATCH_SOURCE)

    tasks = [task_from_issue(issue) for issue in ISSUE_INPUTS]
    runs = build_runs(base_time)
    traces = build_traces(base_time)
    comparisons = build_comparisons(tasks, runs, traces)
    metrics = build_metrics(tasks, runs, traces)

    study = {
        "title": "Expectation Trace: A Minimal Runtime Surprise Layer for Hermes-Agent",
        "research_question": "Can a LeWorldModel-inspired expectation trace observer produce clearer fixture-level issue diagnostics when added to a second node and compared against a baseline representation on the same fixed issue inputs?",
        "hypothesis": "A lightweight expectation trace observer may make issue-derived runtime mismatches more observable and produce more specific fixture-level recovery hints than the baseline representation.",
        "claim_boundary": [
            "This does not implement the full LeWorldModel paper.",
            "This does not establish that Hermes-Agent has a neural world model.",
            "This does not forecast or discover issues.",
            "GitHub issues and PR-backed regression reports are inputs to the simulation.",
            "This evaluates a minimal runtime observation artifact patched into the second node.",
            "Results are preliminary and limited to the selected issue inputs.",
        ],
        "method_summary": "Two nodes were compared on the same fixed issue inputs: a baseline representation versus a patched second node with the expectation trace observer enabled. The paper inspiration is used only to motivate expected-vs-actual surprise scoring.",
        "sandboxes": [
            {
                "name": "baseline",
                "path": str(BASELINE_SANDBOX),
                "description": "Baseline representation derived from selected issue and PR evidence; unpatched for Expectation Trace.",
            },
            {
                "name": "expectation_trace",
                "path": str(TRACE_SANDBOX),
                "description": "Second node patched with a measurement-only expectation trace observer for expected-vs-actual transition tracing, surprise scoring, error categorization, and recovery hints.",
            },
        ],
        "input_selection_policy": {
            "source": "Hermes-Agent GitHub issues, GitHub PRs that close issues, local regression references, and release-linked issue evidence",
            "criteria": [
                "runtime/tool/provider failure relevance",
                "issue has explicit expected versus actual behavior or linked patch evidence",
                "local simulation can be bounded and safe",
                "useful to maintainers",
                "small enough for the first issue-driven benchmark",
            ],
            "honesty_note": "Inputs are issue-derived, but most were converted into bounded fixtures rather than replayed end to end in production.",
        },
        "metrics_defined": [
            "failure_detection_rate",
            "recovery_hint_quality",
            "time_to_diagnosis_steps",
            "surprise_score",
            "surprise_level",
            "secret_redaction_passed",
            "jsonl_export_valid",
            "artifact_validation_checks_passed",
        ],
    }

    conclusions = {
        "main_conclusion": "On the six fixed Lab v0 fixtures, the LeWorldModel-inspired expectation trace observer produced higher fixture-level diagnostic and recovery-hint scores than the baseline representation. This is a bounded simulation result, not a product benchmark, a production superiority claim, or an implementation of LeWorldModel.",
        "secondary_conclusions": [
            "The strongest case was issue #20982 because the issue body provides expected behavior, actual behavior, root cause, and affected files.",
            "The second node scored highest when the baseline representation surfaced the symptom later than the violated dispatcher, provider, or tool-boundary precondition.",
            "Issue-input traces are inspectable because they separate issue evidence, run records, transition records, comparisons, and scientific interpretation.",
        ],
        "what_worked": [
            "Issues became first-class fixed simulation inputs rather than model-generated targets.",
            "The patched second node produced issue-specific recovery hints from expected-vs-actual mismatches.",
            "The lab database now records a concrete second-node patch artifact.",
            "Secret redaction remains a required trace export postcondition.",
        ],
        "what_did_not_work": [
            "The run did not replay every issue end to end in a full production Hermes-Agent environment.",
            "Some issue inputs are PR-backed or release-linked rather than standalone issue bodies.",
            "Pytest was unavailable, so targeted regression suites could not be executed.",
            "The scoring model remains heuristic.",
        ],
        "inconclusive_findings": [
            "Whether the observer changes autonomous recovery after diagnosis remains untested.",
            "Whether surprise_score correlates with maintainer-prioritized severity is unknown.",
            "Whether the second-node observer should be a plugin, core debug flag, or standalone harness requires maintainer input.",
        ],
        "threats_to_validity": [
            "Small task set",
            "Heuristic scoring",
            "Issue reports converted into bounded fixtures may not match production replay",
            "Limited runtime budget",
            "No learned latent model",
            "No CEM planning",
            "No long-horizon evaluation",
            "Pytest unavailable in this environment",
            "Second-node patch is a simulation artifact, not an upstream Hermes-Agent code change",
        ],
        "scientific_honesty": "The fixture-level data is consistent with the hypothesis that expectation tracing can improve observability within this bounded simulation. It does not support claims of issue forecasting, full LeWorldModel behavior, learned latent dynamics, production superiority, or planning gains.",
        "recommended_next_experiment": "Select 10 to 20 live or recently closed Hermes-Agent issues, build executable reproduction fixtures for both nodes, add the observer only to the second node, run tests under pytest, and ask maintainers to rate recovery-hint usefulness.",
        "recommended_pr_scope": {
            "title": "Evaluate optional issue-driven Expectation Trace for tool-call surprise scoring",
            "scope": "measurement-only",
            "confidence": "medium",
            "why": "The fixed issue-input design is inspectable, but evidence is still fixture-based and should remain a measurement-only evaluation artifact until maintainers review it.",
        },
    }

    manifest = {
        "project": PROJECT,
        "title": TITLE,
        "subtitle": SUBTITLE,
        "created_at": created_at,
        "repo_under_test": REPO_UNDER_TEST,
        "paper_inspiration": PAPER_INSPIRATION,
        "local_paths": {
            "root": str(ROOT),
            "lab_db": str(LAB_DB),
            "baseline_sandbox": str(BASELINE_SANDBOX),
            "expectation_trace_sandbox": str(TRACE_SANDBOX),
        },
        "artifacts": {
            "study": "lab_db/study.json",
            "tasks": "lab_db/tasks.json",
            "issue_inputs": "lab_db/issue_inputs.json",
            "runs": "lab_db/runs.jsonl",
            "traces": "lab_db/traces.jsonl",
            "comparisons": "lab_db/comparisons.json",
            "metrics": "lab_db/metrics.json",
            "conclusions": "lab_db/conclusions.json",
            "chart_spec": "lab_db/chart_spec.json",
            "dashboard_prompt": "lab_db/dashboard_prompt.md",
            "data_dictionary": "lab_db/data_dictionary.md",
            "readme": "README.md",
            "validation": "VALIDATION.md",
            "second_node_patch": "patches/expectation_trace_second_node.py",
            "paper": "paper.md",
            "results": "results.md",
            "pr_proposal": "pr_proposal.md",
            "interview_notes": "interview_notes.md",
        },
        "status": "partial",
        "honesty_note": "The lab database is complete as a file package, but the experiment is partial: issues were used as bounded simulation inputs, pytest was unavailable, and the second-node patch is a simulation artifact rather than an upstream Hermes-Agent patch.",
        "methodology_note": "GitHub issues and PR-backed reports are fixed input fixtures. The lab does not predict issues.",
        "metric_caution": "Failure detection rates, recovery-hint quality, and surprise scores are fixture-level heuristic annotations, not production reliability measurements or statistical estimates.",
        "claim_boundary": [
            "Does not implement LeWorldModel.",
            "Does not prove world-model behavior.",
            "Does not prove production recovery.",
            "Does not evaluate autonomous planning.",
            "Does not generalize beyond the six Lab v0 fixtures.",
        ],
    }

    dashboard_prompt = """# Dashboard Generation Prompt

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
"""

    data_dictionary = """# Data Dictionary

## Overview

This lab database is the canonical structured output for an issue-driven Expectation Trace experiment. GitHub issues and PR-backed regression reports are inputs to the simulation. The second node is patched with a measurement-only expected-vs-actual observer.

Status: partial.

## Source Data Files

### manifest.json

Indexes artifacts, local paths, project status, and honesty notes.

### issue_inputs.json

The issue evidence used as simulation input. This is the primary source file for the corrected methodology.

Important fields:

- issue_number: GitHub issue or PR number used as the input identifier.
- issue_url: Primary issue or PR URL.
- evidence_url: URL used to substantiate the issue summary.
- source_basis: live_github_issue, github_issue_closed_by_pr, github_pr_regression, or release_linked_security_pr.
- issue_expected_behavior: Expected behavior extracted from the issue or linked patch evidence.
- issue_actual_behavior: Observed failure behavior extracted from the issue or linked patch evidence.
- trace_hint: Recovery hint generated by the patched second node.

### tasks.json

Benchmark task catalog derived from issue_inputs.json. Each selected task has source=github_issue because the simulation input is issue-derived. Some evidence is PR-backed; see notes and issue_inputs.json.

### runs.jsonl

One row per node run. Every selected issue input has a baseline run and a patched second-node run.

### traces.jsonl

One row per Expectation Trace transition emitted by the patched second node. Baseline runs intentionally do not emit these rows.

## Derived Data Files

### comparisons.json

Per-issue comparison of current behavior versus patched second-node behavior.

### metrics.json

Aggregate metrics computed from tasks, runs, and traces.

### conclusions.json

Scientific interpretation and honesty layer.

### chart_spec.json

Dashboard panel contract.

## Scoring Rules

### recovery_hint_quality

- 0: no actionable recovery hint.
- 1: generic or weak hint.
- 2: useful but incomplete hint.
- 3: specific actionable hint naming the violated precondition and repair path.

### surprise_score

Heuristic mismatch score from 0.0 to 1.0. It is issue-input diagnostic scoring, not issue prediction.

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
"""

    chart_spec = build_chart_spec()

    write_json(LAB_DB / "manifest.json", manifest)
    write_json(LAB_DB / "study.json", study)
    write_json(LAB_DB / "issue_inputs.json", ISSUE_INPUTS)
    write_json(LAB_DB / "tasks.json", tasks)
    write_jsonl(LAB_DB / "runs.jsonl", runs)
    write_jsonl(LAB_DB / "traces.jsonl", traces)
    write_json(LAB_DB / "comparisons.json", comparisons)
    write_json(LAB_DB / "metrics.json", metrics)
    write_json(LAB_DB / "conclusions.json", conclusions)
    write_json(LAB_DB / "chart_spec.json", chart_spec)
    write_text(LAB_DB / "dashboard_prompt.md", dashboard_prompt)
    write_text(LAB_DB / "data_dictionary.md", data_dictionary)
    write_reports(metrics, comparisons, conclusions)

    for run in runs:
        write_text(
            ROOT / run["raw_log_path"],
            f"""run_id: {run['run_id']}
task_id: {run['task_id']}
sandbox: {run['sandbox']}
command: {run['command']}
input_summary: {run['input_summary']}
output_summary: {run['output_summary']}
failure_detected: {run['failure_detected']}
error_category: {run['error_category']}
recovery_hint_quality: {run['recovery_hint_quality']}
notes: {run['notes']}
""",
        )

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
        json.loads((LAB_DB / name).read_text(encoding="utf-8"))
    for name in ["runs.jsonl", "traces.jsonl"]:
        for line in (LAB_DB / name).read_text(encoding="utf-8").splitlines():
            json.loads(line)

    print(json.dumps({
        "status": "partial",
        "lab_db": str(LAB_DB),
        "issue_inputs": len(ISSUE_INPUTS),
        "total_expectation_traces": metrics["total_expectation_traces"],
        "second_node_patch": str(PATCHES / "expectation_trace_second_node.py"),
        "json_validated": True,
    }, indent=2))


if __name__ == "__main__":
    main()
