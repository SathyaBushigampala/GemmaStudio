@echo off
title GemmaStudio - Powered by Gemma on Gemini API
echo ========================================================
echo   Starting GemmaStudio
echo   Powered by Google Gemma on Gemini API
echo ========================================================
python -m pip install -r requirements.txt --quiet
python app.py
pause
