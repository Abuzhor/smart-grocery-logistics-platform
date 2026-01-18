#!/usr/bin/env python3
"""Quality gates runner.

Outputs a concise summary to stdout and writes a full report to
docs/audits/latest-quality-gates-report.md.
"""
from __future__ import annotations

import datetime as _dt
import os
import platform
import py_compile
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Sequence


REPORT_PATH = Path("docs/audits/latest-quality-gates-report.md")


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


def _collect_gates() -> Sequence[Gate]:
    return [
        Gate(gate_id="1", name="Repo structure sanity", run=_gate_repo_structure),
        Gate(gate_id="2", name="Planning scripts compile", run=_gate_planning_compile),
    ]


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

    return 1 if summary["FAIL"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
