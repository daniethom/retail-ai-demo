"""
Unit tests for MCP Tools functionality
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to sys.path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from run_llamastack import RetailMCPTools


class TestRetailMCPTools:
    """Test RetailMCPTools functionality"""
    
    def test_load_data_success(self, temp_data_file):
        """Test successful data loading"""
        tools = RetailMCPTools(temp_data_file)
        
        assert len(tools.data["inventory"]) > 0
        assert len(tools.data["customers"]) > 0
        assert len(tools.data["orders"]) > 0
    
    def test_load_data_file_not_found(self):
        """Test handling of missing data file"""
        tools = RetailMCPTools("nonexistent_file.json")
        
        assert tools.data["inventory"] == []
        assert tools.data["customers"] == []
        assert tools.data["orders"] == []
    
    def test_check_inventory_found(self, temp_data_file):
        """Test inventory lookup with results"""
        tools = RetailMCPTools(temp_data_file)
        
        result = tools.check_inventory("nike")
        
        assert result["found"] is True
        assert len(result["products"]) == 1
        assert "Nike" in result["products"][0]["name"]
    
    def test_check_inventory_not_found(self, temp_data_file):
        """Test inventory lookup with no results"""
        tools = RetailMCPTools(temp_data_file)
        
        result = tools.check_inventory("nonexistent")
        
        assert result["found"] is False
        assert len(result["products"]) == 0
    
    def test_check_inventory_with_size(self, temp_data_file):
        """Test inventory lookup with specific size"""
        tools = RetailMCPTools(temp_data_file)
        
        # Size in stock
        result = tools.check_inventory("nike", "9")
        assert result["found"] is True
        assert result["products"][0]["available"] is True
        assert result["products"][0]["stock"] == 10
        
        # Size out of stock
        result = tools.check_inventory("nike", "10")
        assert result["found"] is True
        assert result["products"][0]["available"] is False
        assert result["products"][0]["stock"] == 0
    
    def test_get_customer_info_found(self, temp_data_file):
        """Test customer lookup with results"""
        tools = RetailMCPTools(temp_data_file)
        
        result = tools.get_customer_info("Test Customer")
        
        assert result["found"] is True
        assert result["customer"]["name"] == "Test Customer"
        assert result["customer"]["tier"] == "Gold"
    
    def test_get_customer_info_not_found(self, temp_data_file):
        """Test customer lookup with no results"""
        tools = RetailMCPTools(temp_data_file)
        
        result = tools.get_customer_info("Nonexistent Customer")
        
        assert result["found"] is False
        assert "not found" in result["message"]
    
    def test_get_order_status_by_id(self, temp_data_file):
        """Test order lookup by order ID"""
        tools = RetailMCPTools(temp_data_file)
        
        result = tools.get_order_status(order_id="TEST-ORD-001")
        
        assert result["found"] is True
        assert result["order"]["order_id"] == "TEST-ORD-001"
        assert result["order"]["status"] == "Delivered"
    
    def test_get_order_status_by_customer(self, temp_data_file):
        """Test order lookup by customer name"""
        tools = RetailMCPTools(temp_data_file)
        
        result = tools.get_order_status(customer_name="Test Customer")
        
        assert result["found"] is True
        assert len(result["orders"]) == 1
        assert result["orders"][0]["order_id"] == "TEST-ORD-001"
    
    def test_get_order_status_not_found(self, temp_data_file):
        """Test order lookup with no results"""
        tools = RetailMCPTools(temp_data_file)
        
        result = tools.get_order_status(order_id="NONEXISTENT-ORDER")
        
        assert result["found"] is False
        assert "not found" in result["message"]


if __name__ == "__main__":
    pytest.main([__file__])