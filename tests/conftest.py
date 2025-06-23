"""
Pytest configuration for Retail AI Assistant tests
"""

import pytest
import json
import tempfile
from pathlib import Path
from typing import Dict, Any

# Test data
SAMPLE_RETAIL_DATA = {
    "inventory": [
        {
            "product_id": "TEST-001",
            "name": "Test Nike Shoes",
            "category": "Footwear",
            "sizes": {"8": 5, "9": 10, "10": 0},
            "price": 100.00,
            "colors": ["Black", "White"],
            "location": "Test Warehouse"
        }
    ],
    "customers": [
        {
            "customer_id": "TEST-CUST-001",
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "555-0123",
            "tier": "Gold",
            "total_orders": 5,
            "lifetime_value": 500.00,
            "recent_purchases": []
        }
    ],
    "orders": [
        {
            "order_id": "TEST-ORD-001",
            "customer_id": "TEST-CUST-001",
            "date": "2024-06-01",
            "status": "Delivered",
            "items": [
                {
                    "product_id": "TEST-001",
                    "name": "Test Nike Shoes",
                    "quantity": 1,
                    "size": "9",
                    "price": 100.00
                }
            ],
            "total": 100.00,
            "shipping_address": "123 Test St, Test City, TC 12345"
        }
    ]
}

@pytest.fixture
def sample_retail_data():
    """Provide sample retail data for testing"""
    return SAMPLE_RETAIL_DATA.copy()

@pytest.fixture
def temp_data_file(sample_retail_data):
    """Create temporary retail data file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_retail_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    Path(temp_file).unlink(missing_ok=True)

@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing"""
    return "This is a test response from the simulated LLM."

# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "openshift: mark test as requiring OpenShift"
    )