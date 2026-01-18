#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "ERROR: Python is not installed or not on PATH." >&2
  exit 127
fi

set +e
"${PYTHON_BIN}" scripts/quality/gates.py
EXIT_CODE=$?
set -e

REPORT_PATH="docs/audits/latest-quality-gates-report.md"
if [[ $EXIT_CODE -ne 0 && -f "$REPORT_PATH" ]]; then
  cat "$REPORT_PATH"
fi

exit $EXIT_CODE
