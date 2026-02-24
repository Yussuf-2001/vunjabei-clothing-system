param(
    [string]$BackendHost = "127.0.0.1",
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendRoot = Join-Path $projectRoot "frontend"
$pythonExe = Join-Path $projectRoot "env\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    throw "Backend virtual environment not found at '$pythonExe'."
}

if (-not (Test-Path $frontendRoot)) {
    throw "Frontend folder not found at '$frontendRoot'."
}

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$projectRoot'; & '$pythonExe' manage.py runserver $BackendHost`:$BackendPort"
)

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$frontendRoot'; npm run dev -- --host 127.0.0.1 --port $FrontendPort --strictPort"
)

Write-Host "Backend:  http://$BackendHost`:$BackendPort/"
Write-Host "Frontend: http://127.0.0.1`:$FrontendPort/login"
Write-Host "Both development servers started in new terminal windows."
