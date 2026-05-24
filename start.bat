@echo off
title Sentiment Analysis System

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

set HF_ENDPOINT=https://hf-mirror.com

where conda >nul 2>&1
if %errorlevel%==0 (
    call conda activate sentiment_bert 2>nul
)

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please run: conda activate sentiment_bert
    pause
    exit /b 1
)

echo ============================================
echo   Sentiment Analysis System
echo ============================================
echo.

echo [1/3] Checking model cache...
if not exist "models\bert_tokenizer\vocab.txt" (
    echo [*] Tokenizer files not found, copying from cache...
    python download_tokenizer.py
    if errorlevel 1 (
        echo [ERROR] Tokenizer files missing.
        pause
        exit /b 1
    )
)
echo [OK] Tokenizer ready

echo.
echo [2/3] Checking model checkpoint...
if not exist "models\BEST_checkpoint_inference.tar" (
    if not exist "models\BEST_checkpoint.tar" (
        echo [ERROR] No model checkpoint found!
        pause
        exit /b 1
    )
    echo [*] Converting to lightweight checkpoint...
    python convert_checkpoint.py
)
echo [OK] Model checkpoint found

echo.
echo [3/3] Starting backend server...

start "" http://localhost:8000

echo.
echo ============================================
echo   Frontend : http://localhost:8000
echo   API Docs : http://localhost:8000/docs
echo   Login    : admin / admin
echo ============================================
echo   Model is loading below, wait a moment
echo   then refresh the browser page.
echo ============================================
echo.

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

pause
