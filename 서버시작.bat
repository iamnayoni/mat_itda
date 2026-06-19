@echo off
chcp 65001 > nul
echo ========================================
echo   맛,잇다 서버 시작 중...
echo ========================================
cd /d "%~dp0"
call venv\Scripts\activate
echo.
echo 서버 주소: http://127.0.0.1:8000
echo 종료하려면 Ctrl+C 를 누르세요
echo ========================================
python manage.py runserver
pause
