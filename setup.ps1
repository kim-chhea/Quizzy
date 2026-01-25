<#
PowerShell setup script for Quizzy

Usage:
 - Open PowerShell (preferably as normal user)
 - If you get an execution policy error: run in an elevated PowerShell: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
 - Run: .\setup.ps1 -InstallOnly (to just create venv and install deps)
 - Run: .\setup.ps1 -Run (to install and launch Streamlit)

This script is safe and non-invasive: it only works in the project folder and creates a local .venv.
#>
param(
    [switch]$InstallOnly,
    [switch]$Run
)

$ErrorActionPreference = 'Stop'

Write-Host "Creating virtual environment in .venv..." -ForegroundColor Cyan
if (-Not (Test-Path .venv)) {
    python -m venv .venv
} else {
    Write-Host ".venv already exists" -ForegroundColor Yellow
}

Write-Host "Activating virtual environment and installing requirements..." -ForegroundColor Cyan
# Use the PowerShell activation script
# Use the PowerShell activation script
try {
    & "${PWD}\.venv\Scripts\Activate.ps1" 2>$null
} catch {
    # If direct invocation fails, try dot-sourcing the activation script
    . "${PWD}\.venv\Scripts\Activate.ps1"
}

python -m pip install --upgrade pip
pip install -r requirements.txt

if ($Run) {
    Write-Host "Launching Quizzy (Streamlit)..." -ForegroundColor Green
    streamlit run app.py
} else {
    Write-Host "Setup complete. To run the app use: streamlit run app.py, or re-run this script with -Run." -ForegroundColor Green
}
