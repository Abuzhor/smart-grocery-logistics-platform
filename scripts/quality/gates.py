#!/usr/bin/env python3
"""Quality gates runner.

Outputs a concise summary to stdout and writes a full report to
docs/audits/latest-quality-gates-report.md.
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import json
import os
import platform
import py_compile
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence


CONFIG_PATH = Path("scripts/quality/gates_config.json")
REPORT_PATH = Path("docs/audits/latest-quality-gates-report.md")
ISSUES_PATH = Path("scripts/planning/issues.json")


def _load_canonical_module():
    try:
        from scripts.quality import canonical as module

        return module
    except Exception:
        canonical_path = Path(__file__).with_name("canonical.py")
        spec = importlib.util.spec_from_file_location("canonical", canonical_path)
        if spec is None or spec.loader is None:
            raise ImportError("Unable to load canonical definitions.")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


canonical = _load_canonical_module()


@dataclass
class GateFailure:
    file: str
    line: Optional[int]
    message: str


@dataclass
class GateResult:
    gate_id: str
    name: str
    status: str  # PASS | FAIL | WARN | SKIP
    message: str
    details: List[str] = field(default_factory=list)
    failures: List[GateFailure] = field(default_factory=list)


@dataclass
class Gate:
    gate_id: str
    name: str
    run: Callable[[], GateResult]


def _now_utc() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).isoformat()


def _git_sha() -> str:
    env_sha = os.environ.get("GITHUB_SHA")
    if env_sha:
        return env_sha[:7]
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _format_failure(failure: GateFailure) -> str:
    if failure.line is None:
        return f"- {failure.file}: {failure.message}"
    return f"- {failure.file}:{failure.line} — {failure.message}"


def _find_line_number(lines: List[str], needle: str) -> Optional[int]:
    if not needle:
        return None
    for idx, line in enumerate(lines, start=1):
        if needle in line:
            return idx
    return None


def _gate_repo_structure() -> GateResult:
    required_paths = [
        Path("README.md"),
        Path("docs"),
        Path("scripts"),
        Path("docs/audits"),
    ]
    details: List[str] = []
    failures: List[GateFailure] = []

    for path in required_paths:
        if path.exists():
            details.append(f"{path.as_posix()}: OK")
        else:
            details.append(f"{path.as_posix()}: MISSING")
            failures.append(
                GateFailure(
                    file=path.as_posix(),
                    line=None,
                    message="Required path is missing.",
                )
            )

    if failures:
        return GateResult(
            gate_id="1",
            name="Repo structure sanity",
            status="FAIL",
            message="Missing required repository paths.",
            details=details,
            failures=failures,
        )

    return GateResult(
        gate_id="1",
        name="Repo structure sanity",
        status="PASS",
        message="All required repository paths exist.",
        details=details,
    )


def _gate_planning_compile() -> GateResult:
    targets = [
        Path("scripts/planning/bootstrap_github.py"),
        Path("scripts/planning/generate_issues_json.py"),
    ]
    details: List[str] = []
    failures: List[GateFailure] = []

    for target in targets:
        if not target.exists():
            details.append(f"{target.as_posix()}: MISSING")
            failures.append(
                GateFailure(
                    file=target.as_posix(),
                    line=None,
                    message="Expected planning script is missing.",
                )
            )
            continue

        try:
            py_compile.compile(target.as_posix(), doraise=True)
            details.append(f"{target.as_posix()}: OK")
        except py_compile.PyCompileError as exc:
            line = getattr(exc.exc_value, "lineno", None)
            details.append(f"{target.as_posix()}: FAIL")
            failures.append(
                GateFailure(
                    file=exc.file or target.as_posix(),
                    line=line,
                    message=exc.msg or str(exc),
                )
            )
        except Exception as exc:
            details.append(f"{target.as_posix()}: FAIL")
            failures.append(
                GateFailure(
                    file=target.as_posix(),
                    line=None,
                    message=str(exc),
                )
            )

    if failures:
        return GateResult(
            gate_id="2",
            name="Planning scripts compile",
            status="FAIL",
            message="One or more planning scripts failed to compile.",
            details=details,
            failures=failures,
        )

    return GateResult(
        gate_id="2",
        name="Planning scripts compile",
        status="PASS",
        message="Planning scripts compile cleanly.",
        details=details,
    )


def _gate_canonical_self_check() -> GateResult:
    failures: List[GateFailure] = []
    details: List[str] = []

    checks = [
        ("phases", canonical.PHASES, canonical.normalize_phase),
        ("domains", canonical.DOMAINS, canonical.normalize_domain),
        ("priorities", canonical.PRIORITIES, canonical.normalize_priority),
    ]

    for label, values, normalize in checks:
        details.append(f"{label}: {len(values)}")
        if not values:
            failures.append(
                GateFailure(
                    file="scripts/quality/canonical.py",
                    line=None,
                    message=f"Canonical {label} list is empty.",
                )
            )
            continue
        if len(set(values)) != len(values):
            failures.append(
                GateFailure(
                    file="scripts/quality/canonical.py",
                    line=None,
                    message=f"Canonical {label} list contains duplicates.",
                )
            )
        for value in values:
            normalized = normalize(value)
            if normalized != value:
                failures.append(
                    GateFailure(
                        file="scripts/quality/canonical.py",
                        line=None,
                        message=(
                            f"Canonical {label} value '{value}' normalizes to "
                            f"'{normalized}'."
                        ),
                    )
                )

    if failures:
        return GateResult(
            gate_id="3",
            name="Canonical self-check",
            status="FAIL",
            message="Canonical lists failed validation.",
            details=details,
            failures=failures,
        )

    return GateResult(
        gate_id="3",
        name="Canonical self-check",
        status="PASS",
        message="Canonical lists validated.",
        details=details,
    )


def _format_allowed(values: Iterable[str]) -> str:
    return ", ".join(values)


def _gate_canonical_drift() -> GateResult:
    if not ISSUES_PATH.exists():
        return GateResult(
            gate_id="4",
            name="Canonical drift detection",
            status="FAIL",
            message="issues.json not found.",
            details=[f"path: {ISSUES_PATH.as_posix()}"],
            failures=[
                GateFailure(
                    file=ISSUES_PATH.as_posix(),
                    line=None,
                    message="Expected file is missing.",
                )
            ],
        )

    raw = ISSUES_PATH.read_text(encoding="utf-8")
    try:
        issues = json.loads(raw)
    except json.JSONDecodeError as exc:
        return GateResult(
            gate_id="4",
            name="Canonical drift detection",
            status="FAIL",
            message="issues.json is not valid JSON.",
            details=[f"path: {ISSUES_PATH.as_posix()}"],
            failures=[
                GateFailure(
                    file=ISSUES_PATH.as_posix(),
                    line=exc.lineno,
                    message=exc.msg,
                )
            ],
        )

    if not isinstance(issues, list):
        return GateResult(
            gate_id="4",
            name="Canonical drift detection",
            status="FAIL",
            message="issues.json must contain a list of issues.",
            details=[f"path: {ISSUES_PATH.as_posix()}"],
            failures=[
                GateFailure(
                    file=ISSUES_PATH.as_posix(),
                    line=None,
                    message="Top-level JSON is not a list.",
                )
            ],
        )

    lines = raw.splitlines()
    failures: List[GateFailure] = []
    warnings: List[GateFailure] = []

    for idx, issue in enumerate(issues, start=1):
        if not isinstance(issue, dict):
            failures.append(
                GateFailure(
                    file=ISSUES_PATH.as_posix(),
                    line=None,
                    message=f"Issue #{idx} is not an object.",
                )
            )
            continue

        title = issue.get("title")
        if not title:
            failures.append(
                GateFailure(
                    file=ISSUES_PATH.as_posix(),
                    line=None,
                    message=f"Issue #{idx} is missing a title.",
                )
            )
            continue

        line = _find_line_number(lines, f"\"title\": \"{title}\"")
        project_meta = issue.get("project_meta")
        if project_meta is None:
            project_meta = issue.get("project")

        if not isinstance(project_meta, dict):
            failures.append(
                GateFailure(
                    file=ISSUES_PATH.as_posix(),
                    line=line,
                    message=f"Issue '{title}' is missing project metadata.",
                )
            )
            continue

        for key in ["phase", "domain", "priority", "notion_reference"]:
            if key not in project_meta:
                failures.append(
                    GateFailure(
                        file=ISSUES_PATH.as_posix(),
                        line=line,
                        message=f"Issue '{title}' missing project_meta.{key}.",
                    )
                )

        phase = project_meta.get("phase")
        domain = project_meta.get("domain")
        priority = project_meta.get("priority")

        if phase is not None:
            normalized = canonical.normalize_phase(phase)
            if normalized is None:
                failures.append(
                    GateFailure(
                        file=ISSUES_PATH.as_posix(),
                        line=line,
                        message=(
                            f"Issue '{title}' has invalid phase '{phase}'. "
                            f"Allowed: {_format_allowed(canonical.PHASES)}."
                        ),
                    )
                )
            elif normalized != phase:
                warnings.append(
                    GateFailure(
                        file=ISSUES_PATH.as_posix(),
                        line=line,
                        message=(
                            f"Issue '{title}' phase '{phase}' normalizes to "
                            f"'{normalized}'."
                        ),
                    )
                )

        if domain is not None:
            normalized = canonical.normalize_domain(domain)
            if normalized is None:
                failures.append(
                    GateFailure(
                        file=ISSUES_PATH.as_posix(),
                        line=line,
                        message=(
                            f"Issue '{title}' has invalid domain '{domain}'. "
                            f"Allowed: {_format_allowed(canonical.DOMAINS)}."
                        ),
                    )
                )
            elif normalized != domain:
                warnings.append(
                    GateFailure(
                        file=ISSUES_PATH.as_posix(),
                        line=line,
                        message=(
                            f"Issue '{title}' domain '{domain}' normalizes to "
                            f"'{normalized}'."
                        ),
                    )
                )

        if priority is not None:
            normalized = canonical.normalize_priority(priority)
            if normalized is None:
                failures.append(
                    GateFailure(
                        file=ISSUES_PATH.as_posix(),
                        line=line,
                        message=(
                            f"Issue '{title}' has invalid priority '{priority}'. "
                            f"Allowed: {_format_allowed(canonical.PRIORITIES)}."
                        ),
                    )
                )
            elif normalized != priority:
                warnings.append(
                    GateFailure(
                        file=ISSUES_PATH.as_posix(),
                        line=line,
                        message=(
                            f"Issue '{title}' priority '{priority}' normalizes to "
                            f"'{normalized}'."
                        ),
                    )
                )

    details = [
        f"issues scanned: {len(issues)}",
        f"warnings: {len(warnings)}",
        f"failures: {len(failures)}",
    ]

    if failures:
        return GateResult(
            gate_id="4",
            name="Canonical drift detection",
            status="FAIL",
            message="Drift detected in issues.json.",
            details=details,
            failures=failures + warnings,
        )

    if warnings:
        return GateResult(
            gate_id="4",
            name="Canonical drift detection",
            status="WARN",
            message="Normalization drift detected in issues.json.",
            details=details,
            failures=warnings,
        )

    return GateResult(
        gate_id="4",
        name="Canonical drift detection",
        status="PASS",
        message="All canonical values are normalized.",
        details=details,
    )


def _load_config() -> dict:
    """Load quality gates configuration from gates_config.json."""
    if not CONFIG_PATH.exists():
        print(f"ERROR: Configuration file not found: {CONFIG_PATH.as_posix()}", file=sys.stderr)
        sys.exit(1)
    
    try:
        config_text = CONFIG_PATH.read_text(encoding="utf-8")
        config = json.loads(config_text)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON in {CONFIG_PATH.as_posix()}: {exc.msg}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: Failed to load config from {CONFIG_PATH.as_posix()}: {exc}", file=sys.stderr)
        sys.exit(1)
    
    return config


def _collect_gates() -> Sequence[Gate]:
    """Collect gates based on configuration."""
    config = _load_config()
    
    # Update global REPORT_PATH if specified in config
    global REPORT_PATH
    if "report_path" in config:
        REPORT_PATH = Path(config["report_path"])
    
    # Map gate IDs to their implementations
    gate_implementations = {
        "1": ("Repo structure sanity", _gate_repo_structure),
        "2": ("Planning scripts compile", _gate_planning_compile),
        "3": ("Canonical self-check", _gate_canonical_self_check),
        "4": ("Canonical drift detection", _gate_canonical_drift),
    }
    
    gates_config = config.get("gates", [])
    gates = []
    
    for gate_config in gates_config:
        gate_id = gate_config.get("gate_id")
        enabled = gate_config.get("enabled", True)
        
        if not enabled:
            continue
        
        if gate_id in gate_implementations:
            default_name, run_func = gate_implementations[gate_id]
            # Allow config to override the default name
            name = gate_config.get("name", default_name)
            gates.append(Gate(gate_id=gate_id, name=name, run=run_func))
    
    # If no gates configured, fall back to all gates
    if not gates:
        return [
            Gate(gate_id=gid, name=name, run=func)
            for gid, (name, func) in gate_implementations.items()
        ]
    
    return gates


def _write_report(results: List[GateResult]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "PASS": sum(1 for r in results if r.status == "PASS"),
        "FAIL": sum(1 for r in results if r.status == "FAIL"),
        "WARN": sum(1 for r in results if r.status == "WARN"),
        "SKIP": sum(1 for r in results if r.status == "SKIP"),
    }

    lines: List[str] = []
    lines.append("# Quality Gates Report")
    lines.append("")
    lines.append("## Environment")
    lines.append(f"- Timestamp (UTC): {_now_utc()}")
    lines.append(f"- Commit: {_git_sha()}")
    lines.append(f"- OS: {platform.platform()}")
    lines.append(f"- Python: {platform.python_version()}")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- PASS: {summary['PASS']}")
    lines.append(f"- FAIL: {summary['FAIL']}")
    lines.append(f"- WARN: {summary['WARN']}")
    lines.append(f"- SKIP: {summary['SKIP']}")
    lines.append("")
    lines.append("## Gate Results")
    lines.append("")
    for result in results:
        lines.append(f"### Gate {result.gate_id}: {result.name}")
        lines.append(f"- Status: {result.status}")
        lines.append(f"- Message: {result.message}")
        lines.append("- Details:")
        if result.details:
            for item in result.details:
                lines.append(f"  - {item}")
        else:
            lines.append("  - (none)")
        lines.append("")
    lines.append("## Failures")
    lines.append("")

    any_failures = False
    for result in results:
        if result.failures:
            any_failures = True
            lines.append(f"### Gate {result.gate_id}: {result.name}")
            for failure in result.failures:
                lines.append(_format_failure(failure))
            lines.append("")

    if not any_failures:
        lines.append("(none)")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def _print_gate_table(results: Sequence[GateResult]) -> None:
    print("\nGate Results Summary")
    print("NAME | STATUS | SHORT REASON")
    print("--- | --- | ---")
    for result in results:
        reason = result.message or "(no message)"
        print(f"{result.name} | {result.status} | {reason}")


def _print_failed_gates(results: Sequence[GateResult]) -> None:
    failing = [result for result in results if result.status == "FAIL"]
    if not failing:
        return

    print("\nFAILED GATES")
    for result in failing:
        reason = result.message
        if result.failures:
            reason = f"{reason} ({result.failures[0].message})"
        print(f"- {result.name}: {reason}")


def _print_report_content() -> None:
    print("\nREPORT CONTENT (latest-quality-gates-report.md):")
    try:
        report_text = REPORT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("(report missing)")
        return
    except Exception as exc:
        print(f"(report unreadable: {exc})")
        return
    print(report_text)


def main() -> int:
    results: List[GateResult] = []
    for gate in _collect_gates():
        try:
            results.append(gate.run())
        except Exception as exc:
            results.append(
                GateResult(
                    gate_id=gate.gate_id,
                    name=gate.name,
                    status="FAIL",
                    message="Unhandled exception.",
                    details=["Gate execution raised an unexpected error."],
                    failures=[GateFailure(file="(runner)", line=None, message=str(exc))],
                )
            )

    _write_report(results)

    summary = {
        "PASS": sum(1 for r in results if r.status == "PASS"),
        "FAIL": sum(1 for r in results if r.status == "FAIL"),
        "WARN": sum(1 for r in results if r.status == "WARN"),
        "SKIP": sum(1 for r in results if r.status == "SKIP"),
    }

    print(
        "Quality gates: "
        f"PASS={summary['PASS']} FAIL={summary['FAIL']} "
        f"WARN={summary['WARN']} SKIP={summary['SKIP']} | "
        f"Report: {REPORT_PATH.as_posix()}"
    )

    _print_gate_table(results)
    if summary["FAIL"] > 0:
        _print_failed_gates(results)
        _print_report_content()

    return 1 if summary["FAIL"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
