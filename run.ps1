param(
  [switch]$NoInstall
)

$ErrorActionPreference = 'Stop'

Write-Host "Starting Scribe Agent..." -ForegroundColor Cyan

# Ensure we are in the repo root where this script resides
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Create venv if missing
if (-not (Test-Path .\.venv)) {
  Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
  python -m venv .venv
}

# Activate venv
$activate = Join-Path .\.venv\Scripts Activate.ps1
. $activate

# Install requirements unless suppressed
if (-not $NoInstall) {
  Write-Host "Installing requirements..." -ForegroundColor Yellow
  pip install -r requirements.txt | Out-Null
}

# Do not echo secrets; just confirm .env presence
$envPath = Join-Path (Get-Location) '.env'
if (Test-Path $envPath) {
  Write-Host ".env found (keys not displayed)." -ForegroundColor Green
} else {
  Write-Host ".env not found. You can copy .env.example to .env." -ForegroundColor Yellow
}

# Launch
Write-Host "Launching app..." -ForegroundColor Cyan
python .\main.py
