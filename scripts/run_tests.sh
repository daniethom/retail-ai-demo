#!/bin/bash

# Test runner script for Retail AI Assistant
# Runs different types of tests based on arguments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TEST_TYPE="unit"
VERBOSE=false
COVERAGE=false

# Help function
show_help() {
    echo "Test runner for Retail AI Assistant"
    echo ""
    echo "Usage: $0 [OPTIONS] [TEST_TYPE]"
    echo ""
    echo "TEST_TYPE:"
    echo "  unit          Run unit tests only (default)"
    echo "  integration   Run integration tests"
    echo "  e2e           Run end-to-end tests"
    echo "  performance   Run performance tests"
    echo "  all           Run all tests"
    echo ""
    echo "OPTIONS:"
    echo "  -v, --verbose     Verbose output"
    echo "  -c, --coverage    Generate coverage report"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 unit           # Run unit tests"
    echo "  $0 -c all         # Run all tests with coverage"
    echo "  $0 -v integration # Run integration tests verbosely"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        unit|integration|e2e|performance|all)
            TEST_TYPE="$1"
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Check if we're in the right directory
if [[ ! -f "run_llamastack.py" ]]; then
    echo -e "${RED}Error: Must be run from the project root directory${NC}"
    exit 1
fi

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}Warning: No virtual environment detected${NC}"
    echo "Consider running: source venv/bin/activate"
fi

# Install test dependencies if needed
if [[ ! -f "requirements-dev.txt" ]] || ! pip show pytest > /dev/null 2>&1; then
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    if [[ -f "requirements-dev.txt" ]]; then
        pip install -r requirements-dev.txt
    else
        pip install pytest pytest-asyncio pytest-cov httpx
    fi
fi

# Build pytest command
PYTEST_CMD="python -m pytest"

if [[ "$VERBOSE" == true ]]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

if [[ "$COVERAGE" == true ]]; then
    PYTEST_CMD="$PYTEST_CMD --cov=run_llamastack --cov-report=html --cov-report=term"
fi

# Run tests based on type
echo -e "${GREEN}Running $TEST_TYPE tests...${NC}"

case $TEST_TYPE in
    unit)
        $PYTEST_CMD tests/unit/
        ;;
    integration)
        echo -e "${YELLOW}Note: Integration tests may require OpenShift Local running${NC}"
        $PYTEST_CMD tests/integration/ -m integration
        ;;
    e2e)
        echo -e "${YELLOW}Note: E2E tests require the application to be running${NC}"
        $PYTEST_CMD tests/e2e/ -m e2e
        ;;
    performance)
        echo -e "${YELLOW}Note: Performance tests require the application to be running${NC}"
        $PYTEST_CMD tests/ -m performance
        ;;
    all)
        echo -e "${YELLOW}Running all tests (some may be skipped if requirements not met)${NC}"
        $PYTEST_CMD tests/
        ;;
    *)
        echo -e "${RED}Unknown test type: $TEST_TYPE${NC}"
        show_help
        exit 1
        ;;
esac

# Show coverage report location if generated
if [[ "$COVERAGE" == true ]]; then
    echo -e "${GREEN}Coverage report generated at: htmlcov/index.html${NC}"
fi

echo -e "${GREEN}Tests completed!${NC}"