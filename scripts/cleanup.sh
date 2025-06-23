#!/bin/bash
# Cleanup script for demo environment

echo "🧹 Cleaning up demo environment..."

# Delete OpenShift project
oc delete project retail-ai-demo 2>/dev/null || echo "Project already deleted"

# Clean up local files
rm -rf venv/
rm -rf htmlcov/
rm -rf .pytest_cache/
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Cleanup complete!"