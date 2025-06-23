"""
Main application to run LlamaStack with MCP retail tools on OpenShift AI
This script sets up the LLM, MCP server, and web interface
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

"""
Main application to run Retail AI Assistant with MCP-style tools on OpenShift AI
This demo simulates LlamaStack functionality for retail operations
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulatedLLMClient:
    """
    Simulated LLM client for demo purposes
    In production, this would be replaced with actual LlamaStack integration
    """
    
    def __init__(self):
        self.model_name = "Llama-3.2-3B (Simulated)"
        logger.info(f"Initialized simulated LLM: {self.model_name}")
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Simulate AI response generation
        In production, this would call actual LLM
        """
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        # For demo, we'll return contextual responses based on the tools used
        if context and "tool_result" in context:
            return self._format_ai_response(context["tool_result"], context.get("intent", "general"))
        
        return "I'm ready to help with your retail operations! Ask me about inventory or customer service."
    
    def _format_ai_response(self, tool_result: Dict[str, Any], intent: str) -> str:
        """Format tool results into natural AI responses"""
        
        if intent == "inventory":
            if not tool_result.get("found", False):
                return f"I couldn't find any products matching your search. Could you try a different product name or brand?"
            
            response = f"Here's what I found in our inventory:\n\n"
            
            for product in tool_result.get("products", []):
                response += f"**{product['name']}** - ${product['price']}\n"
                response += f"📍 Location: {product['location']}\n"
                response += f"🎨 Available colors: {', '.join(product['colors'])}\n"
                
                if "size" in product:
                    # Specific size query
                    if product.get("available", False):
                        response += f"✅ Size {product['size']}: **{product['stock']} units** in stock\n"
                    else:
                        response += f"❌ Size {product['size']}: **Out of stock**\n"
                        # Suggest alternatives
                        if "sizes" in product:
                            available_sizes = [sz for sz, stock in product["sizes"].items() if stock > 0]
                            if available_sizes:
                                response += f"💡 Alternative sizes available: {', '.join(available_sizes)}\n"
                else:
                    # All sizes query
                    response += "📦 **Stock levels by size:**\n"
                    for size, stock in product.get("sizes", {}).items():
                        status = "✅" if stock > 0 else "❌"
                        response += f"   {status} Size {size}: {stock} units\n"
                
                response += "\n"
            
            return response.strip()
        
        elif intent == "customer":
            if not tool_result.get("found", False):
                return f"I couldn't find that customer or order. Could you double-check the name or order number?"
            
            if "customer" in tool_result:
                # Customer info response
                customer = tool_result["customer"]
                response = f"**Customer Profile: {customer['name']}**\n\n"
                response += f"🏆 Tier: {customer['tier']} Customer\n"
                response += f"📧 Email: {customer['email']}\n"
                response += f"📞 Phone: {customer['phone']}\n"
                response += f"🛒 Total Orders: {customer['total_orders']}\n"
                response += f"💰 Lifetime Value: ${customer['lifetime_value']:,.2f}\n\n"
                
                response += "**Recent Purchase History:**\n"
                for purchase in customer.get("recent_purchases", []):
                    response += f"• **Order {purchase['order_id']}** ({purchase['date']})\n"
                    response += f"  Status: {purchase['status']} | Total: ${purchase['total']}\n"
                
                return response
            
            elif "order" in tool_result:
                # Single order response
                order = tool_result["order"]
                response = f"**Order Details: {order['order_id']}**\n\n"
                response += f"📅 Date: {order['date']}\n"
                response += f"📦 Status: **{order['status']}**\n"
                response += f"💵 Total: ${order['total']}\n"
                
                if "tracking" in order:
                    response += f"🚚 Tracking: {order['tracking']}\n"
                
                response += f"📍 Shipping: {order['shipping_address']}\n\n"
                
                response += "**Items:**\n"
                for item in order.get("items", []):
                    response += f"• {item['name']} (Size {item['size']}) - ${item['price']}\n"
                
                return response
            
            elif "orders" in tool_result:
                # Multiple orders response
                orders = tool_result["orders"]
                customer_name = tool_result.get("customer_name", "Customer")
                response = f"**Recent Orders for {customer_name}:**\n\n"
                
                for order in orders:
                    response += f"• **{order['order_id']}** ({order['date']}) - ${order['total']} - {order['status']}\n"
                
                return response
        
        return "I've processed your request. Is there anything specific you'd like me to explain further?"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetailMCPTools:
    """
    MCP (Model Context Protocol) tools for retail operations
    These tools allow the AI to interact with our mock retail data
    """
    
    def __init__(self, data_file: str = "retail_data.json"):
        """Initialize with retail data"""
        self.data_file = data_file
        self.load_data()
    
    def load_data(self):
        """Load mock retail data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
                logger.info("Loaded retail data successfully")
        except FileNotFoundError:
            logger.error(f"Could not find {self.data_file}")
            self.data = {"inventory": [], "customers": [], "orders": []}
    
    def check_inventory(self, product_name: str, size: str = None) -> Dict[str, Any]:
        """
        Check inventory for a product
        Args:
            product_name: Name or partial name of product
            size: Optional size to check
        Returns:
            Dictionary with inventory information
        """
        results = []
        
        for item in self.data["inventory"]:
            # Simple search - check if product_name is in the item name (case insensitive)
            if product_name.lower() in item["name"].lower():
                result = {
                    "product_id": item["product_id"],
                    "name": item["name"],
                    "price": item["price"],
                    "colors": item["colors"],
                    "location": item["location"]
                }
                
                if size:
                    # Check specific size
                    stock = item["sizes"].get(size, 0)
                    result["size"] = size
                    result["stock"] = stock
                    result["available"] = stock > 0
                else:
                    # Show all sizes
                    result["sizes"] = item["sizes"]
                    result["total_stock"] = sum(item["sizes"].values())
                
                results.append(result)
        
        return {
            "query": f"{product_name}" + (f" size {size}" if size else ""),
            "found": len(results) > 0,
            "products": results
        }
    
    def get_customer_info(self, customer_name: str) -> Dict[str, Any]:
        """
        Get customer information and recent purchases
        Args:
            customer_name: Customer name to search for
        Returns:
            Dictionary with customer information
        """
        for customer in self.data["customers"]:
            if customer_name.lower() in customer["name"].lower():
                return {
                    "found": True,
                    "customer": customer
                }
        
        return {
            "found": False,
            "message": f"Customer '{customer_name}' not found"
        }
    
    def get_order_status(self, order_id: str = None, customer_name: str = None) -> Dict[str, Any]:
        """
        Get order status by order ID or customer name
        Args:
            order_id: Specific order ID to look up
            customer_name: Customer name to find recent orders
        Returns:
            Dictionary with order information
        """
        if order_id:
            # Search by order ID
            for order in self.data["orders"]:
                if order["order_id"].lower() == order_id.lower():
                    return {
                        "found": True,
                        "order": order
                    }
            return {
                "found": False,
                "message": f"Order '{order_id}' not found"
            }
        
        elif customer_name:
            # Find customer first, then their orders
            customer_info = self.get_customer_info(customer_name)
            if customer_info["found"]:
                customer_id = customer_info["customer"]["customer_id"]
                customer_orders = [order for order in self.data["orders"] 
                                 if order["customer_id"] == customer_id]
                return {
                    "found": True,
                    "customer_name": customer_name,
                    "orders": customer_orders
                }
            else:
                return customer_info
        
        return {
            "found": False,
            "message": "Please provide either order_id or customer_name"
        }

class RetailAssistant:
    """
    Main retail assistant that combines simulated LLM with MCP-style tools
    """
    
    def __init__(self):
        self.tools = RetailMCPTools()
        self.llm_client = SimulatedLLMClient()
        logger.info("Retail Assistant initialized successfully")
    
    async def process_query(self, user_message: str) -> str:
        """
        Process user query using simulated LLM + MCP tools
        Args:
            user_message: User's question/request
        Returns:
            AI response string
        """
        user_message_lower = user_message.lower()
        
        try:
            # Intent recognition and tool calling
            if any(word in user_message_lower for word in ["stock", "inventory", "available", "have"]):
                return await self._handle_inventory_query(user_message)
            
            elif any(word in user_message_lower for word in ["customer", "order", "purchase", "bought", "ord-"]):
                return await self._handle_customer_query(user_message)
            
            else:
                # Default helpful response
                return await self.llm_client.generate_response(
                    user_message,
                    context={"intent": "general"}
                )
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."
    
    async def _handle_inventory_query(self, message: str) -> str:
        """Handle inventory-related queries using MCP tools"""
        # Extract product and size info
        words = message.lower().split()
        
        product_name = ""
        if "nike" in words:
            product_name = "nike"
        elif "adidas" in words:
            product_name = "adidas"
        elif "levi" in words:
            product_name = "levi"
        
        size = None
        for word in words:
            if word.isdigit() and len(word) <= 2:
                size = word
                break
        
        if not product_name:
            return await self.llm_client.generate_response(
                message,
                context={
                    "tool_result": {"found": False, "message": "Could not identify product"},
                    "intent": "inventory"
                }
            )
        
        # Call MCP tool
        tool_result = self.tools.check_inventory(product_name, size)
        
        # Generate AI response
        return await self.llm_client.generate_response(
            message,
            context={
                "tool_result": tool_result,
                "intent": "inventory"
            }
        )
    
    async def _handle_customer_query(self, message: str) -> str:
        """Handle customer service queries using MCP tools"""
        words = message.split()
        
        # Extract names and order IDs
        potential_names = []
        for i, word in enumerate(words):
            if word.istitle() and len(word) > 2:
                if i + 1 < len(words) and words[i + 1].istitle():
                    potential_names.append(f"{word} {words[i + 1]}")
                else:
                    potential_names.append(word)
        
        order_id = None
        for word in words:
            if word.upper().startswith("ORD-"):
                order_id = word.upper()
                break
        
        tool_result = None
        
        if order_id:
            tool_result = self.tools.get_order_status(order_id=order_id)
        elif potential_names:
            for name in potential_names:
                result = self.tools.get_customer_info(name)
                if result["found"]:
                    tool_result = result
                    break
            
            if not tool_result:
                # Try order lookup by customer name
                for name in potential_names:
                    result = self.tools.get_order_status(customer_name=name)
                    if result["found"]:
                        tool_result = result
                        break
        
        if not tool_result:
            tool_result = {"found": False, "message": "Could not identify customer or order"}
        
        # Generate AI response
        return await self.llm_client.generate_response(
            message,
            context={
                "tool_result": tool_result,
                "intent": "customer"
            }
        )

# FastAPI web application
app = FastAPI(title="Retail AI Assistant", version="1.0.0")

# Initialize the assistant
assistant = RetailAssistant()

# Templates for web interface
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main demo interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    """Handle chat requests"""
    try:
        data = await request.json()
        user_message = data.get("message", "")
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Process the message
        response = await assistant.process_query(user_message)
        
        return JSONResponse({
            "response": response,
            "status": "success"
        })
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return JSONResponse({
            "response": "I'm sorry, I encountered an error. Please try again.",
            "status": "error"
        }, status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint for OpenShift"""
    return {"status": "healthy", "service": "retail-ai-assistant"}

if __name__ == "__main__":
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)