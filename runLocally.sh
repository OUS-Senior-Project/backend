#!/bin/bash

echo "🔄 Starting local backend setup..."

# Navigate to the script's directory (important!)
cd "$(dirname "$0")"

# 1. Remove old venv if it exists
if [ -d "venv" ]; then
    echo "🧹 Removing old virtual environment..."
    rm -rf venv
fi

# 2. Create a new venv
echo "🐍 Creating new virtual environment..."
python3 -m venv venv

# 3. Activate venv
echo "📦 Activating virtual environment..."
source venv/bin/activate

# 4. Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "📥 requirements.txt not found. Installing minimal dependencies..."
    pip install --upgrade pip
    pip install fastapi "uvicorn[standard]" python-dotenv pydantic-settings ruff mypy
    pip freeze > requirements.txt
fi

# 5. Run Ruff linting (optional but recommended)
if command -v ruff >/dev/null 2>&1; then
    echo "🔎 Running Ruff linting..."
    ruff check . --fix
else
    echo "⚠️ Ruff not installed. Skipping lint step."
fi

# 6. Run Ruff formatter
if command -v ruff >/dev/null 2>&1; then
    echo "🎨 Formatting code with Ruff..."
    ruff format .
fi

# 7. Run Mypy type checking (optional)
if command -v mypy >/dev/null 2>&1; then
    echo "🧠 Running Mypy type checking..."
    mypy app/ || echo "⚠️ Mypy found type issues (does not stop server)."
fi

# 8. Run the FastAPI server
echo "🚀 Starting FastAPI server on http://127.0.0.1:8000 ..."
uvicorn app.main:app --reload
