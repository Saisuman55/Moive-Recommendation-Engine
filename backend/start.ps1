# Start FastAPI on http://127.0.0.1:8000 (run from repo: .\backend\start.ps1)
# Requires Python 3.11+ from https://www.python.org/downloads/ (not the Microsoft Store stub).

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Find-Python {
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:ProgramFiles\Python313\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe"
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notmatch "WindowsApps") { return $cmd.Source }
    return $null
}

$venvPy = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
    $py = Find-Python
    if (-not $py) {
        Write-Host "Python not found. Install 3.11+ from python.org and enable 'Add to PATH', then run this script again." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "Creating venv..." -ForegroundColor Cyan
    & $py -m venv (Join-Path $PSScriptRoot "venv")
    & $venvPy -m pip install -U pip
    & (Join-Path $PSScriptRoot "venv\Scripts\pip.exe") install -r (Join-Path $PSScriptRoot "requirements.txt")
}

Write-Host "API: http://127.0.0.1:8000/docs" -ForegroundColor Green
& $venvPy -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
