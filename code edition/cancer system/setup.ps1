# Cancer Risk Prediction System Setup Script
# Run this script to set up the complete environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cancer Risk Prediction System Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not found in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "This can happen if you installed Python from Microsoft Store." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "SOLUTION 1: Add Python to PATH" -ForegroundColor White
    Write-Host "1. Search for 'Environment Variables' in Windows search" -ForegroundColor White
    Write-Host "2. Click 'Environment Variables'" -ForegroundColor White
    Write-Host "3. Under 'System variables', find 'Path' and click 'Edit'" -ForegroundColor White
    Write-Host "4. Add this path: C:\Users\$env:USERNAME\AppData\Local\Microsoft\WindowsApps\" -ForegroundColor White
    Write-Host "5. Restart PowerShell and try again" -ForegroundColor White
    Write-Host ""
    Write-Host "SOLUTION 2: Download Python from python.org" -ForegroundColor White
    Write-Host "1. Go to: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. Download Python 3.8 or higher" -ForegroundColor White
    Write-Host "3. Install and check 'Add Python to PATH'" -ForegroundColor White
    Write-Host "4. Run this script again" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Create virtual environment
Write-Host ""
Write-Host "Step 2: Creating virtual environment..." -ForegroundColor Yellow
if (!(Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists." -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host ""
Write-Host "Step 3: Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Step 4: Install dependencies
Write-Host ""
Write-Host "Step 4: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Step 5: Verify installation
Write-Host ""
Write-Host "Step 5: Verifying installation..." -ForegroundColor Yellow
$flaskCheck = pip list | Select-String "Flask"
if ($flaskCheck) {
    Write-Host "✅ Flask installed successfully." -ForegroundColor Green
} else {
    Write-Host "❌ Flask installation failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application:" -ForegroundColor White
Write-Host "1. Run: .\run.ps1" -ForegroundColor White
Write-Host "2. Open: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Your cancer risk prediction system is ready!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to continue"