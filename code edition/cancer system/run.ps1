# Run Cancer Risk Prediction System
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Cancer Risk Prediction System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Starting Flask application..." -ForegroundColor Yellow
python app.py

Write-Host ""
Read-Host "Press Enter to exit"