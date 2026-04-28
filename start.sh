#!/usr/bin/env bash
# Quick start script — starts backend + opens frontend in browser

set -e

echo "=== Atamasta Web === Starting..."

# Check for .env file
if [ ! -f backend/.env ]; then
  echo "[info] Creating backend/.env from example..."
  cp backend/.env.example backend/.env
fi

# Option A: Docker Compose (recommended)
if command -v docker &>/dev/null && command -v docker-compose &>/dev/null; then
  echo "[docker] Starting with Docker Compose..."
  docker-compose up -d
  echo "[docker] Backend available at http://localhost:8000"
  echo "[docker] API docs at http://localhost:8000/docs"
else
  # Option B: Local Python
  echo "[local] Starting backend locally..."
  cd backend
  if [ ! -d ".venv" ]; then
    python -m venv .venv
    source .venv/bin/activate || source .venv/Scripts/activate
    pip install -r requirements.txt
  else
    source .venv/bin/activate || source .venv/Scripts/activate
  fi
  uvicorn app.main:app --reload --port 8000 &
  BACKEND_PID=$!
  cd ..
  echo "[local] Backend PID: $BACKEND_PID"
fi

echo ""
echo "✓ Open frontend: frontend/index.html in your browser"
echo "  (or use Live Server in VS Code)"
echo ""
echo "Default admin credentials:"
echo "  Email:    admin@atamasta.com"
echo "  Password: Admin@12345"
echo ""
echo "API docs: http://localhost:8000/docs"
