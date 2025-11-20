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
    pip install fastapi "uvicorn[standard]" python-dotenv pydantic-settings
    pip freeze > requirements.txt
fi

# 5. Run the FastAPI server
echo "🚀 Starting FastAPI server on http://127.0.0.1:8000 ..."
uvicorn app.main:app --reload
