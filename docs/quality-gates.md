# Quality Gates

This repository uses a single entry point for quality gates to keep PHASE 0 stable and auditable.

## Run locally

### PowerShell (Windows)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/quality/run_gates.ps1
```

### Bash (Linux/macOS)

```bash
scripts/quality/run_gates.sh
```

## Output

- Concise summary is printed to stdout.
- Full report is written to docs/audits/latest-quality-gates-report.md.

The report includes timestamp (UTC), commit SHA (best effort), OS, Python version, each gate result, and failures with file+line.

## Gate Coverage

- Repo structure sanity (README.md, docs/, scripts/, docs/audits/).
- Planning script compilation (scripts/planning/bootstrap_github.py and generate_issues_json.py).

## CI

The workflow runs on pull requests and pushes to main for Windows and Linux. Reports are uploaded as artifacts even on failure.
