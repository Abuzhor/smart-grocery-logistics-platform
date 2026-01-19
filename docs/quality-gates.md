# Quality Gates

This repository uses a single entry point for quality gates to keep PHASE 0 stable and auditable.

## Configuration

Quality gates are configured via `scripts/quality/gates_config.json`. This JSON file defines:

- `gates`: Array of gate configurations, each containing:
  - `gate_id`: Unique identifier for the gate (e.g., "1", "2", "3", "4")
  - `name`: Human-readable name of the gate
  - `enabled`: Boolean flag to enable/disable the gate (default: true)
- `report_path`: Path where the quality gates report will be written (default: "docs/audits/latest-quality-gates-report.md")

Example configuration:
```json
{
  "gates": [
    {
      "gate_id": "1",
      "name": "Repo structure sanity",
      "enabled": true
    }
  ],
  "report_path": "docs/audits/latest-quality-gates-report.md"
}
```

## Run Locally

### Bash (Linux/macOS)

```bash
scripts/quality/run_gates.sh
```

This script will:
- Detect the appropriate Python executable (python3 or python)
- Execute the quality gates via `gates.py`
- Return the exit code from gates.py (non-zero on failure)

### PowerShell (Windows)

```powershell
powershell -File scripts/quality/run_gates.ps1
```

This script will:
- Detect the appropriate Python executable (python or py launcher)
- Execute the quality gates via `gates.py`
- Return the exit code from gates.py (non-zero on failure)

**Note**: The PowerShell script does NOT modify the global execution policy.

## Output

- Concise summary is printed to stdout.
- Full report is written to docs/audits/latest-quality-gates-report.md.

The report includes timestamp (UTC), commit SHA (best effort), OS, Python version, each gate result, and failures with file+line.

## Gate Coverage

- Repo structure sanity (README.md, docs/, scripts/, docs/audits/).
- Planning script compilation (scripts/planning/bootstrap_github.py and generate_issues_json.py).
- Canonical self-check (validates canonical.py definitions).
- Canonical drift detection (validates issues.json against canonical values).

## Drift Prevention

Canonical Phase, Domain, and Priority values live in scripts/quality/canonical.py and are the single source of truth.

The drift gate:

- Normalizes phase/domain/priority values (case, spaces, hyphens/underscores, phase0 variants).
- Reports original → normalized values as WARN when normalization succeeds but differs.
- FAILs when a value cannot be normalized to a canonical set.
- Validates required project metadata fields but does not auto-edit issues.json.

## CI/CD Integration

The quality gates workflow (`.github/workflows/quality-gates.yml`) runs on:
- Pull requests
- Pushes to the `main` branch

The workflow:
- Runs on both `ubuntu-latest` and `windows-latest` via a matrix strategy
- Executes quality gates through the platform-specific scripts (`run_gates.sh` or `run_gates.ps1`)
- **Always uploads the quality gates report as an artifact**, even when gates fail (using `if: always()`)
- **Fails the job with a non-zero exit code** if any gate fails, blocking merge actions in CI/CD

Artifact name: `quality-gates-report-{os}` (e.g., `quality-gates-report-ubuntu-latest`)

