#!/bin/bash

# Retail AI Assistant Deployment Script for OpenShift AI
# This script helps deploy the MCP demo application

set -e

echo "🚀 Deploying Retail AI Assistant to OpenShift AI"
echo "================================================="

# Configuration
PROJECT_NAME="retail-ai-demo"
APP_NAME="retail-ai-assistant"

# Check if oc (OpenShift CLI) is installed
if ! command -v oc &> /dev/null; then
    echo "❌ OpenShift CLI (oc) is not installed. Please install it first."
    exit 1
fi

# Check if logged into OpenShift
if ! oc whoami &> /dev/null; then
    echo "❌ Not logged into OpenShift. Please run 'oc login' first."
    exit 1
fi

echo "✅ OpenShift CLI is ready"

# Create or switch to project
echo "📁 Setting up project: $PROJECT_NAME"
if oc get project $PROJECT_NAME &> /dev/null; then
    echo "Project $PROJECT_NAME already exists, switching to it..."
    oc project $PROJECT_NAME
else
    echo "Creating new project: $PROJECT_NAME"
    oc new-project $PROJECT_NAME --display-name="Retail AI Demo" --description="MCP Demo with LlamaStack"
fi

# Create templates directory if it doesn't exist
mkdir -p templates

# Build the application using Docker strategy (works better with OpenShift Local)
echo "🔨 Building application..."
oc new-build . --name=$APP_NAME --strategy=docker --to=$APP_NAME:latest || true

# Wait for build to complete
echo "⏳ Waiting for build to complete..."
oc logs -f bc/$APP_NAME

# Deploy the application
echo "🚀 Deploying application..."
oc apply -f deployment.yaml

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
oc rollout status deployment/$APP_NAME

# Get the route URL
ROUTE_URL=$(oc get route ${APP_NAME}-route -o jsonpath='{.spec.host}')

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo "Application URL: https://$ROUTE_URL"
echo ""
echo "You can now:"
echo "1. Open the URL in your browser to access the demo"
echo "2. Try the example queries in the interface"
echo "3. Monitor logs with: oc logs -f deployment/$APP_NAME"
echo ""
echo "Demo Examples to try:"
echo "• 'Do we have Nike Air Max size 10 in stock?'"
echo "• 'What did John Smith order recently?'"
echo "• 'What is the status of order ORD-1005?'"
echo ""
echo "Happy demoing! 🛍️"