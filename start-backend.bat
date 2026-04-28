@echo off
echo === Atamasta Backend Startup ===
echo.

cd backend

IF NOT EXIST ".env" (
  echo Creating .env from example...
  copy .env.example .env
)

IF NOT EXIST ".venv" (
  echo Creating virtual environment...
  python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting FastAPI backend on http://localhost:8000
echo API docs available at http://localhost:8000/docs
echo.
echo Default admin: admin@atamasta.com / Admin@12345
echo.
echo Press Ctrl+C to stop the server.
echo.

uvicorn app.main:app --reload --port 8000

pause
