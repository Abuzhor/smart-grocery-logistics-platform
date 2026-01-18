# Quality Gates Report

## Environment
- Timestamp (UTC): 2026-01-18T22:10:30.724287+00:00
- Commit: 812c6b2
- OS: Linux-6.11.0-1018-azure-x86_64-with-glibc2.39
- Python: 3.12.3

## Summary
- PASS: 1
- FAIL: 1
- WARN: 0
- SKIP: 0

## Gate Results

### Gate 1: Repo structure sanity
- Status: PASS
- Message: All required repository paths exist.
- Details:
  - README.md: OK
  - docs: OK
  - scripts: OK

### Gate 2: Planning scripts compile
- Status: FAIL
- Message: One or more planning scripts failed to compile.
- Details:
  - scripts/planning/bootstrap_github.py: FAIL
  - scripts/planning/generate_issues_json.py: OK

## Failures

### Gate 2: Planning scripts compile
- scripts/planning/bootstrap_github.py:853 — Sorry: IndentationError: expected an indented block after 'if' statement on line 851 (bootstrap_github.py, line 853)
