$ErrorActionPreference = "Stop"

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    & $python.Path "scripts/quality/gates.py"
    exit $LASTEXITCODE
}

$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pyLauncher) {
    & $pyLauncher.Path -3 "scripts/quality/gates.py"
    exit $LASTEXITCODE
}

Write-Error "Python is not installed or not on PATH."
exit 127
