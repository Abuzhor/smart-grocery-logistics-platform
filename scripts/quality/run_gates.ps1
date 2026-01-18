$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $repoRoot

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    & $python.Path "scripts/quality/gates.py"
    $exitCode = $LASTEXITCODE
} else {
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        & $pyLauncher.Path -3 "scripts/quality/gates.py"
        $exitCode = $LASTEXITCODE
    } else {
        Write-Error "Python is not installed or not on PATH."
        exit 127
    }
}

$reportPath = "docs/audits/latest-quality-gates-report.md"
if (Test-Path $reportPath) {
    Get-Content -Raw $reportPath
}

exit $exitCode
