#!/bin/bash
# Development environment setup script

echo "🛠️ Setting up development environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create necessary directories
mkdir -p docs/screenshots
mkdir -p tests/{unit,integration,e2e,fixtures}
mkdir -p customer-configs

# Create test files if they don't exist
touch tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py tests/e2e/__init__.py

echo "✅ Development environment ready!"
echo "To activate: source venv/bin/activate"