# Customization Guide

This guide shows how to adapt the Retail AI Assistant demo for different customers, industries, and use cases.

## 🎯 Quick Customizations (5-15 minutes)

### Brand Customization

#### 1. Update Visual Branding
Edit `templates/index.html`:

```html
<!-- Change header colors and title -->
<div class="header">
    <h1>🏪 [CUSTOMER NAME] AI Assistant</h1>
    <p>Powered by Red Hat OpenShift AI</p>
</div>

<!-- Update CSS colors -->
<style>
    .header {
        background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
    }
    
    .user-message {
        background: #YOUR_BRAND_COLOR;
    }
</style>
```

#### 2. Add Customer Logo
```html
<!-- In the header section -->
<div class="header">
    <img src="data:image/svg+xml;base64,[BASE64_LOGO]" alt="Customer Logo" style="height: 40px; margin-bottom: 10px;">
    <h1>AI-Powered Operations</h1>
</div>
```

### Data Customization

#### 1. Industry-Specific Products
Edit `retail_data.json` with customer's actual product categories:

**Fashion Retailer:**
```json
{
  "product_id": "ZARA-001",
  "name": "Summer Floral Dress",
  "category": "Women's Fashion",
  "sizes": {"XS": 5, "S": 12, "M": 8, "L": 3, "XL": 0},
  "price": 49.99,
  "colors": ["Floral Print", "Solid Black"],
  "season": "Summer 2024",
  "location": "Store A"
}
```

**Electronics Retailer:**
```json
{
  "product_id": "APPL-001", 
  "name": "iPhone 15 Pro",
  "category": "Smartphones",
  "variants": {"128GB": 5, "256GB": 12, "512GB": 3, "1TB": 1},
  "price": 999.99,
  "colors": ["Space Black", "Silver", "Gold"],
  "warranty": "1 year",
  "location": "Warehouse Central"
}
```

#### 2. Customer-Specific Names
```json
{
  "customer_id": "CUST-001",
  "name": "[USE_CUSTOMER_EMPLOYEE_NAMES]",
  "email": "realistic@customerdomain.com",
  "tier": "VIP",
  "company": "[CUSTOMER_COMPANY_IF_B2B]"
}
```

## 🏭 Industry-Specific Versions

### Fashion & Apparel

#### Enhanced Product Model
```python
# Add to RetailMCPTools
def check_style_recommendations(self, customer_id: str, season: str = "current") -> Dict[str, Any]:
    """Recommend styles based on customer history and current season"""
    customer = self.get_customer_info_by_id(customer_id)
    
    # Logic for style recommendations
    recommendations = []
    for item in self.data["inventory"]:
        if item.get("season") == season:
            recommendations.append({
                "name": item["name"],
                "reason": "Matches your style preferences",
                "price": item["price"]
            })
    
    return {
        "customer": customer["name"],
        "season": season,
        "recommendations": recommendations
    }

def check_size_availability(self, product_name: str, preferred_sizes: List[str]) -> Dict[str, Any]:
    """Check availability across multiple size preferences"""
    # Enhanced size checking logic
    pass
```

#### Fashion-Specific Queries
```python
# Add to AI orchestrator intent recognition
fashion_keywords = ["style", "trend", "season", "outfit", "collection"]
if any(word in user_message_lower for word in fashion_keywords):
    return await self._handle_fashion_query(user_message)
```

### Electronics & Technology

#### Technical Specifications Tool
```python
def get_product_specs(self, product_name: str) -> Dict[str, Any]:
    """Get detailed technical specifications"""
    for item in self.data["inventory"]:
        if product_name.lower() in item["name"].lower():
            return {
                "found": True,
                "product": item["name"],
                "specifications": item.get("specs", {}),
                "compatibility": item.get("compatibility", []),
                "warranty": item.get("warranty", "Standard"),
                "support_options": ["Phone", "Chat", "Email", "In-store"]
            }
    
    return {"found": False}

def check_compatibility(self, product1: str, product2: str) -> Dict[str, Any]:
    """Check if two products are compatible"""
    # Compatibility checking logic
    pass
```

### Grocery & Food Service

#### Expiration & Freshness Tracking
```python
def check_expiration_dates(self, category: str = None) -> Dict[str, Any]:
    """Check products nearing expiration"""
    from datetime import datetime, timedelta
    
    expiring_soon = []
    for item in self.data["inventory"]:
        if item.get("expiration_date"):
            exp_date = datetime.strptime(item["expiration_date"], "%Y-%m-%d")
            days_until_exp = (exp_date - datetime.now()).days
            
            if days_until_exp <= 3:  # Expiring in 3 days
                expiring_soon.append({
                    "name": item["name"],
                    "expiration_date": item["expiration_date"],
                    "days_remaining": days_until_exp,
                    "location": item["location"],
                    "action": "Mark down price" if days_until_exp <= 1 else "Monitor closely"
                })
    
    return {
        "items_expiring": expiring_soon,
        "total_count": len(expiring_soon)
    }
```

### B2B/Wholesale

#### Volume Pricing & Contracts
```python
def get_volume_pricing(self, product_id: str, quantity: int, customer_tier: str) -> Dict[str, Any]:
    """Calculate volume-based pricing"""
    base_price = self.get_product_price(product_id)
    
    # Volume discounts
    if quantity >= 1000:
        discount = 0.15  # 15% for large orders
    elif quantity >= 500:
        discount = 0.10  # 10% for medium orders
    elif quantity >= 100:
        discount = 0.05  # 5% for small bulk orders
    else:
        discount = 0.0
    
    # Customer tier bonus
    tier_discounts = {"Platinum": 0.05, "Gold": 0.03, "Silver": 0.01}
    tier_discount = tier_discounts.get(customer_tier, 0.0)
    
    final_discount = min(discount + tier_discount, 0.25)  # Max 25% discount
    final_price = base_price * (1 - final_discount)
    
    return {
        "base_price": base_price,
        "quantity": quantity,
        "volume_discount": discount,
        "tier_discount": tier_discount,
        "final_price": final_price,
        "total_cost": final_price * quantity,
        "savings": (base_price - final_price) * quantity
    }
```

## 🎨 Advanced UI Customizations

### Custom CSS Themes

#### Corporate Theme
```css
/* Add to templates/index.html */
:root {
    --primary-color: #003366;      /* Corporate blue */
    --secondary-color: #0066cc;    /* Lighter blue */
    --accent-color: #ff6600;       /* Orange accent */
    --text-color: #333333;
    --background-gradient: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
}

.header {
    background: var(--background-gradient);
}

.user-message {
    background: var(--accent-color);
}

#sendButton {
    background: var(--background-gradient);
}
```

#### Industry-Specific Icons
```html
<!-- Fashion -->
<li onclick="sendExample('Show me new arrivals')">
    👗 "Show me new arrivals"
</li>

<!-- Electronics -->
<li onclick="sendExample('Check iPhone 15 specifications')">
    📱 "Check iPhone 15 specifications"
</li>

<!-- Grocery -->
<li onclick="sendExample('What items expire today?')">
    🥛 "What items expire today?"
</li>
```

### Multi-Language Support

#### Basic Translation Framework
```javascript
// Add to templates/index.html
const translations = {
    'en': {
        'title': 'Retail AI Assistant',
        'subtitle': 'MCP Demo with LlamaStack on OpenShift AI',
        'placeholder': 'Ask about inventory, customers, or orders...',
        'send': 'Send'
    },
    'es': {
        'title': 'Asistente AI de Retail',
        'subtitle': 'Demo MCP con LlamaStack en OpenShift AI',
        'placeholder': 'Pregunta sobre inventario, clientes o pedidos...',
        'send': 'Enviar'
    }
};

function setLanguage(lang) {
    const t = translations[lang];
    document.querySelector('h1').textContent = `🛍️ ${t.title}`;
    document.querySelector('.header p').textContent = t.subtitle;
    document.getElementById('messageInput').placeholder = t.placeholder;
    document.getElementById('sendButton').textContent = t.send;
}
```

## 🔧 Technical Customizations

### Custom MCP Tools

#### Example: Loyalty Points Tool
```python
def check_loyalty_points(self, customer_id: str) -> Dict[str, Any]:
    """Check customer loyalty points and redemption options"""
    customer = self.get_customer_by_id(customer_id)
    
    # Calculate points based on purchase history
    total_spent = customer.get("lifetime_value", 0)
    points = int(total_spent * 10)  # 10 points per dollar
    
    # Redemption options
    redemptions = []
    if points >= 1000:
        redemptions.append({"reward": "$10 off next purchase", "cost": 1000})
    if points >= 2500:
        redemptions.append({"reward": "Free shipping", "cost": 2500})
    if points >= 5000:
        redemptions.append({"reward": "$50 gift card", "cost": 5000})
    
    return {
        "customer": customer["name"],
        "points_balance": points,
        "points_earned_today": 0,  # Could be calculated
        "available_rewards": redemptions,
        "next_reward_threshold": min([r["cost"] for r in redemptions if r["cost"] > points], default=None)
    }
```

### Integration Hooks

#### Webhook Support
```python
import requests

async def notify_external_system(self, event_type: str, data: Dict[str, Any]):
    """Send notifications to external systems"""
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        payload = {
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=5)
            logger.info(f"Webhook sent: {response.status_code}")
        except Exception as e:
            logger.error(f"Webhook failed: {e}")
```

## 📋 Customer-Specific Demo Scripts

### Fashion Retailer Script
```markdown
**Opening:** "Fashion moves fast, and so do customer expectations. Let me show you how AI can help your team provide instant, accurate information about your latest collections."

**Queries to demonstrate:**
- "Do we have the summer floral dress in size medium?"
- "What's trending in our women's section?"
- "Show me Sarah's style preferences"
- "Which items need to be marked down this week?"
```

### Technology Retailer Script
```markdown
**Opening:** "Tech customers ask detailed questions about specifications, compatibility, and availability. Here's how AI can make your sales team technical experts instantly."

**Queries to demonstrate:**
- "Is the iPhone 15 Pro compatible with wireless charging?"
- "What laptops do we have under $1000?"
- "Check warranty status for order ORD-1001"
- "Show me John's tech upgrade recommendations"
```

## 🚀 Deployment Variations

### Multi-Environment Setup
```bash
# Development
export ENVIRONMENT=dev
export RESOURCE_LIMITS="cpu=100m,memory=256Mi"

# Customer Demo
export ENVIRONMENT=demo
export RESOURCE_LIMITS="cpu=200m,memory=512Mi"

# Production Simulation
export ENVIRONMENT=prod
export RESOURCE_LIMITS="cpu=500m,memory=1Gi"
```

### Customer-Specific Configurations
```yaml
# customer-configs/fashion-retailer.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: demo-config
data:
  INDUSTRY: "fashion"
  BRAND_COLOR: "#ff69b4"
  DEMO_PRODUCTS: "dresses,shoes,accessories"
  CUSTOMER_NAME: "Fashion Forward Inc"
```

## 📊 Analytics & Tracking

### Demo Engagement Metrics
```python
# Add to FastAPI app
@app.middleware("http")
async def track_demo_usage(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Log demo interactions
    if request.url.path == "/chat":
        logger.info(f"Demo query processed in {process_time:.2f}s")
    
    return response
```

## 📞 Support for Customizations

### Testing Customizations
```bash
# Test locally first
python run_llamastack.py

# Test with custom data
cp retail_data.json retail_data.json.backup
cp customer-data/fashion-retailer.json retail_data.json
python run_llamastack.py

# Deploy and test
./deploy-local.sh
curl http://localhost:8000/health
```

### Version Control for Customer Versions
```bash
# Create customer-specific branch
git checkout -b customer/fashion-retailer
# Make customizations
git add -A
git commit -m "Customize for Fashion Retailer demo"
git push origin customer/fashion-retailer
```

---

**Remember: Start with simple branding changes, then add industry-specific features based on customer feedback during the demo!** 🎯