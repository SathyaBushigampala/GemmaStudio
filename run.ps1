# GemmaStudio PowerShell Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting GemmaStudio" -ForegroundColor Green
Write-Host "  Powered by Google Gemma on Gemini API" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

python -m pip install -r requirements.txt --quiet
python app.py
