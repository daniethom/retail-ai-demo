#!/bin/bash

# Retail AI Assistant Deployment Script for OpenShift Local (CRC)
# This script is optimized for local development

set -e

echo "🚀 Deploying Retail AI Assistant to OpenShift Local"
echo "===================================================="

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
    echo "For OpenShift Local, typically: oc login -u developer -p developer https://api.crc.testing:6443"
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

# Ensure templates directory exists
mkdir -p templates

# Check if required files exist
echo "📋 Checking required files..."
required_files=("Dockerfile" "requirements.txt" "run_llamastack.py" "retail_data.json" "templates/index.html")
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Missing required file: $file"
        echo "Please make sure all files from the artifacts are in the current directory."
        exit 1
    fi
done

echo "✅ All required files found"

# Build the application using Docker strategy
echo "🔨 Building application with Docker strategy..."
if oc get bc/$APP_NAME &> /dev/null; then
    echo "Build config exists, starting new build..."
    oc start-build $APP_NAME --from-dir=. --follow
else
    echo "Creating new build config..."
    oc new-build . --name=$APP_NAME --strategy=docker --to=$APP_NAME:latest
    
    # Wait a moment for build config to be created
    echo "⏳ Waiting for build config to be ready..."
    sleep 3
    
    # Start the actual build
    echo "🚀 Starting build from source directory..."
    oc start-build $APP_NAME --from-dir=. --follow
fi

# Check if build was successful
echo "🔍 Checking build status..."
echo "⏳ Waiting for build to complete..."

# Wait for build to finish
oc wait --for=condition=Complete build -l buildconfig=$APP_NAME --timeout=300s

BUILD_STATUS=$(oc get build -l buildconfig=$APP_NAME --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].status.phase}')
if [[ "$BUILD_STATUS" != "Complete" ]]; then
    echo "❌ Build failed with status: $BUILD_STATUS"
    echo "Check build logs with: oc logs -f bc/$APP_NAME"
    exit 1
fi

echo "✅ Build completed successfully"

# Create deployment if it doesn't exist
if ! oc get deployment/$APP_NAME &> /dev/null; then
    echo "📦 Creating deployment..."
    oc new-app $APP_NAME:latest --name=$APP_NAME
    
    # Set resource limits
    oc set resources deployment/$APP_NAME --requests=cpu=500m,memory=1Gi --limits=cpu=1000m,memory=2Gi
    
    # Add health checks
    oc set probe deployment/$APP_NAME --readiness --get-url=http://:8000/health --initial-delay-seconds=5 --period-seconds=5
    oc set probe deployment/$APP_NAME --liveness --get-url=http://:8000/health --initial-delay-seconds=30 --period-seconds=10
else
    echo "📦 Deployment exists, updating image..."
    oc rollout latest dc/$APP_NAME 2>/dev/null || oc set image deployment/$APP_NAME $APP_NAME=$APP_NAME:latest
fi

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
oc rollout status deployment/$APP_NAME --timeout=300s

# Expose the service if route doesn't exist
if ! oc get route/$APP_NAME &> /dev/null; then
    echo "🌐 Creating route..."
    oc expose service/$APP_NAME --hostname=$APP_NAME-$PROJECT_NAME.apps-crc.testing
fi

# Get the route URL
ROUTE_URL=$(oc get route/$APP_NAME -o jsonpath='{.spec.host}' 2>/dev/null || echo "Route not found")

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
if [[ "$ROUTE_URL" != "Route not found" ]]; then
    echo "Application URL: http://$ROUTE_URL"
    echo "(Note: OpenShift Local uses HTTP, not HTTPS)"
else
    echo "Getting service info..."
    oc get svc/$APP_NAME
    echo "You can access the app by port-forwarding:"
    echo "oc port-forward svc/$APP_NAME 8000:8000"
    echo "Then visit: http://localhost:8000"
fi

echo ""
echo "Useful commands:"
echo "• View logs: oc logs -f deployment/$APP_NAME"
echo "• Check status: oc get pods -l app=$APP_NAME"
echo "• Port forward: oc port-forward svc/$APP_NAME 8000:8000"
echo ""
echo "Demo Examples to try:"
echo "• 'Do we have Nike Air Max size 10 in stock?'"
echo "• 'What did John Smith order recently?'"
echo "• 'What is the status of order ORD-1005?'"
echo ""
echo "Happy demoing! 🛍️"