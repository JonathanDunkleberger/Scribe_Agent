param(
  # Skip dependency installation for faster runs
  [switch]$NoInstall
)

# Stop on errors
$ErrorActionPreference = 'Stop'

Write-Host "Starting Scribe Agent..." -ForegroundColor Cyan

# Ensure we run from the repo root (directory of this script)
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Create virtual environment if missing
if (-not (Test-Path .\.venv)) {
  Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
  python -m venv .venv
}

# Activate virtual environment
$activate = Join-Path .\.venv\Scripts Activate.ps1
. $activate

# Install Python dependencies unless suppressed
if (-not $NoInstall) {
  Write-Host "Installing requirements..." -ForegroundColor Yellow
  pip install -r requirements.txt | Out-Null
}

# Do not echo secrets; only confirm presence of .env
$envPath = Join-Path (Get-Location) '.env'
if (Test-Path $envPath) {
  Write-Host ".env found (keys not displayed)." -ForegroundColor Green
} else {
  Write-Host ".env not found. You can copy .env.example to .env." -ForegroundColor Yellow
}

# Launch the application
Write-Host "Launching app..." -ForegroundColor Cyan
python .\main.py
