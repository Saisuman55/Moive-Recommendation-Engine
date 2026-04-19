# Starts API (port 8000) and Vite (port 5173) in two new windows.
# Requires: Node.js on PATH, Python 3.11+ from python.org (not the Microsoft Store stub).

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"

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

$py = Find-Python
if (-not $py) {
    Write-Host "Python 3.11+ not found. Install from https://www.python.org/downloads/ and check 'Add python.exe to PATH'." -ForegroundColor Yellow
    Write-Host "The Microsoft Store 'python' stub will not work." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path (Join-Path $backend "venv\Scripts\python.exe"))) {
    Write-Host "Creating venv and installing backend deps (first run only)..." -ForegroundColor Cyan
    & $py -m venv (Join-Path $backend "venv")
    & (Join-Path $backend "venv\Scripts\python.exe") -m pip install -U pip
    & (Join-Path $backend "venv\Scripts\pip.exe") install -r (Join-Path $backend "requirements.txt")
}

$apiCmd = @"
cd '$backend'
`$env:DATABASE_URL='sqlite:///./movie_rec.db'
`$env:MODEL_PATH='./data/svd_model.pkl'
Write-Host 'API: http://127.0.0.1:8000/docs' -ForegroundColor Green
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
"@

$webCmd = @"
cd '$frontend'
Write-Host 'Web: http://127.0.0.1:5173 (API via Vite proxy /api -> http://127.0.0.1:8000)' -ForegroundColor Green
npm run dev -- --host 127.0.0.1 --port 5173
"@

Start-Process powershell -WorkingDirectory $root -ArgumentList "-NoExit", "-Command", $apiCmd
Start-Sleep -Seconds 2
Start-Process powershell -WorkingDirectory $root -ArgumentList "-NoExit", "-Command", $webCmd

Write-Host "Opened two terminals: API (8000) and Web (5173). Close those windows to stop servers." -ForegroundColor Cyan
