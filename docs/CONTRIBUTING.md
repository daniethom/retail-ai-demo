# Contributing to Retail AI Assistant Demo

Thank you for your interest in improving this demo! This guide will help you get started with development and contributions.

## 🎯 Project Goals

This demo aims to showcase:
- **Model Context Protocol (MCP)** implementation patterns
- **Red Hat OpenShift AI** capabilities for enterprise AI
- **Real-world retail AI** use cases and business value
- **Production-ready architecture** patterns

## 🚀 Quick Start for Contributors

### Prerequisites
- **Python 3.11+** 
- **OpenShift Local (CRC)** or access to OpenShift cluster
- **Git** for version control
- **VS Code** (recommended) with Python extension

### Development Setup

1. **Fork and clone:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/retail-ai-demo.git
   cd retail-ai-demo
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run locally:**
   ```bash
   python run_llamastack.py
   # Access at http://localhost:8000
   ```

## 📋 Development Workflow

### Branch Strategy
- **main**: Production-ready demo code
- **develop**: Integration branch for new features
- **feature/**: Individual feature development
- **bugfix/**: Bug fixes
- **demo/**: Customer-specific customizations

### Making Changes

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test thoroughly:**
   ```bash
   # Run local tests
   python -m pytest tests/
   
   # Test deployment
   ./deploy-local.sh
   ```

4. **Commit with clear messages:**
   ```bash
   git commit -m "feat: add inventory search by category"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   # Create PR via GitHub interface
   ```

## 🎨 Coding Standards

### Python Style Guide
- **Follow PEP 8** for Python code formatting
- **Use type hints** for all function parameters and returns
- **Document functions** with docstrings
- **Keep functions focused** (single responsibility)

### Example Code Style
```python
async def check_inventory(
    self, 
    product_name: str, 
    size: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check inventory for a specific product.
    
    Args:
        product_name: Name or partial name of product to search
        size: Optional size filter
        
    Returns:
        Dictionary containing inventory information
        
    Raises:
        ValueError: If product_name is empty
    """
    if not product_name.strip():
        raise ValueError("Product name cannot be empty")
    
    # Implementation here...
    return result
```

### Frontend Standards
- **Semantic HTML5** elements
- **Responsive CSS** (mobile-first)
- **Progressive enhancement** JavaScript
- **Accessibility** considerations (ARIA labels, keyboard navigation)

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/           # Unit tests for individual functions
├── integration/    # Integration tests for MCP tools
├── e2e/           # End-to-end demo scenarios
└── fixtures/      # Test data and mocks
```

### Writing Tests
```python
import pytest
from retail_assistant import RetailMCPTools

def test_inventory_lookup_success():
    """Test successful inventory lookup."""
    tools = RetailMCPTools("test_data.json")
    result = tools.check_inventory("nike", "10")
    
    assert result["found"] is True
    assert len(result["products"]) > 0
    assert result["products"][0]["name"].lower().contains("nike")

def test_inventory_lookup_not_found():
    """Test inventory lookup with no results."""
    tools = RetailMCPTools("test_data.json")
    result = tools.check_inventory("nonexistent")
    
    assert result["found"] is False
    assert len(result["products"]) == 0
```

### Running Tests
```bash
# All tests
python -m pytest

# Specific test file
python -m pytest tests/unit/test_mcp_tools.py

# With coverage
python -m pytest --cov=retail_assistant

# Integration tests (requires OpenShift)
python -m pytest tests/integration/ --openshift
```

## 🎯 Contribution Areas

### High-Priority Improvements
1. **Additional MCP Tools**
   - Product recommendations
   - Pricing lookup
   - Promotional campaigns
   - Supplier information

2. **Enhanced UI/UX**
   - Voice input support
   - Rich media responses
   - Mobile optimization
   - Accessibility improvements

3. **Integration Examples**
   - Real database connections
   - External API integrations
   - Message queue patterns
   - Webhook implementations

4. **Production Features**
   - Authentication/authorization
   - Rate limiting
   - Comprehensive logging
   - Performance monitoring

### Documentation Improvements
- **More demo scenarios** for different retail verticals
- **Video tutorials** for setup and customization
- **Architecture decision records** (ADRs)
- **Troubleshooting guides** for common issues

### Demo Enhancements
- **Industry-specific versions** (fashion, electronics, grocery)
- **Multi-language support** for global demos
- **Advanced analytics** dashboard
- **Customer-specific branding** templates

## 🔧 Adding New MCP Tools

### Tool Development Pattern
1. **Define the interface** in `RetailMCPTools`
2. **Implement the logic** with proper error handling
3. **Add data access** patterns to `retail_data.json`
4. **Update AI orchestrator** to recognize new intents
5. **Add response formatting** in `SimulatedLLMClient`
6. **Write comprehensive tests**
7. **Update documentation**

### Example: Adding Promotions Tool
```python
def check_promotions(self, product_id: str = None, 
                    customer_tier: str = None) -> Dict[str, Any]:
    """
    Check active promotions for products or customer tiers.
    
    Args:
        product_id: Optional product to check promotions for
        customer_tier: Optional customer tier for targeted promotions
        
    Returns:
        Dictionary with promotion information
    """
    promotions = []
    
    for promo in self.data.get("promotions", []):
        if product_id and promo.get("applicable_products"):
            if product_id in promo["applicable_products"]:
                promotions.append(promo)
        elif customer_tier and promo.get("customer_tiers"):
            if customer_tier in promo["customer_tiers"]:
                promotions.append(promo)
        elif not product_id and not customer_tier:
            # Return all active promotions
            promotions.append(promo)
    
    return {
        "found": len(promotions) > 0,
        "promotions": promotions,
        "query_params": {
            "product_id": product_id,
            "customer_tier": customer_tier
        }
    }
```

## 📊 Demo Data Guidelines

### Data Quality Standards
- **Realistic data** that reflects actual retail scenarios
- **Consistent naming** conventions across entities
- **Proper relationships** between customers, orders, and products
- **Diverse examples** to showcase different use cases

### Adding Demo Data
```json
{
  "products": [
    {
      "product_id": "BRAND-###",
      "name": "Descriptive Product Name",
      "category": "Category",
      "sizes": {"size": stock_count},
      "price": 99.99,
      "colors": ["Color1", "Color2"],
      "location": "Warehouse X"
    }
  ],
  "customers": [
    {
      "customer_id": "CUST-###",
      "name": "First Last",
      "email": "email@domain.com",
      "tier": "Gold|Silver|Bronze",
      "total_orders": 0,
      "lifetime_value": 0.00,
      "recent_purchases": []
    }
  ]
}
```

## 🚀 Deployment Contributions

### OpenShift Improvements
- **Resource optimization** for different cluster sizes
- **Multi-environment** deployment configurations
- **Monitoring and alerting** setup
- **Security hardening** configurations

### CI/CD Enhancements
- **Automated testing** pipelines
- **Container scanning** integration
- **GitOps** deployment patterns
- **Release automation**

## 📝 Documentation Standards

### Code Documentation
- **Docstrings** for all public functions
- **Type hints** for parameters and returns
- **Inline comments** for complex logic
- **Architecture decision records** for significant changes

### Demo Documentation
- **Step-by-step** setup instructions
- **Troubleshooting** sections with common issues
- **Customization guides** for different scenarios
- **Video walkthroughs** for complex procedures

## 🐛 Bug Reports

### Issue Template
When reporting bugs, please include:
- **Environment details** (OpenShift version, Python version)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Logs and error messages**
- **Screenshots** if relevant

### Priority Levels
- **P0 (Critical)**: Demo completely broken
- **P1 (High)**: Major functionality not working
- **P2 (Medium)**: Minor issues affecting user experience
- **P3 (Low)**: Cosmetic issues or nice-to-have improvements

## 💡 Feature Requests

### Request Guidelines
- **Business justification** for the feature
- **Use case scenarios** where it would be valuable
- **Implementation suggestions** if you have technical ideas
- **Impact assessment** on existing functionality

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Wiki**: For detailed documentation and guides

### Code Review Process
- **All changes** require review before merging
- **Focus on**: correctness, readability, performance, security
- **Be constructive** in feedback and responsive to suggestions
- **Test thoroughly** before requesting review

## 🎉 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **Demo presentations** when appropriate

---

**Thank you for helping make this demo even better! Every contribution, no matter how small, helps showcase the power of Red Hat OpenShift AI to more customers.** 🚀