Retail AI Assistant - MCP Demo
A comprehensive demonstration of Model Context Protocol (MCP) capabilities using Red Hat OpenShift AI. This demo showcases how AI can intelligently interact with retail systems for inventory management and customer service operations.
Show Image
🎯 Overview
This demo illustrates enterprise AI capabilities by simulating a retail assistant that can:

Check inventory in real-time with natural language queries
Retrieve customer information and purchase history
Process order status requests
Provide intelligent responses using MCP-style tool integration

🏗️ Architecture
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Interface │────│  FastAPI Server  │────│   MCP Tools     │
│   (React-style) │    │  (AI Orchestrator)│    │  (Retail Data)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌──────────────────┐
                       │ Simulated LLM    │
                       │ (Llama-3.2-3B)   │
                       └──────────────────┘
🚀 Quick Start
Prerequisites

OpenShift Local (CRC) or OpenShift AI cluster access
OpenShift CLI (oc) installed
Git for cloning the repository

1-Command Deploy
bashgit clone <your-repo-url>
cd retail-ai-demo
chmod +x deploy-local.sh
./deploy-local.sh
Manual Setup

Clone and setup:
bashgit clone <your-repo-url>
cd retail-ai-demo

Login to OpenShift:
bashoc login -u developer -p developer https://api.crc.testing:6443

Deploy:
bash./deploy-local.sh

Access the demo:

Route: http://retail-ai-assistant-retail-ai-demo.apps-crc.testing
Or port-forward: oc port-forward deployment/retail-ai-assistant 8000:8000



🛍️ Demo Script
Opening (2 minutes)

"Today I'll demonstrate how Red Hat OpenShift AI enables intelligent retail operations using Model Context Protocol (MCP) - a standard that allows AI systems to safely interact with business data and systems."

Core Demo Scenarios
1. Inventory Management
Try these queries:

"Do we have Nike Air Max size 10 in stock?"
"Show me all Adidas inventory"
"Are there any Levi jeans available in size 32?"

Key Points:

Natural language understanding
Real-time inventory lookup
Detailed stock information (sizes, colors, locations)
Actionable business intelligence

2. Customer Service
Try these queries:

"What did John Smith order recently?"
"Show me Sarah Johnson's purchase history"
"What is the status of order ORD-1005?"

Key Points:

Complete customer profiles
Purchase history analysis
Order tracking capabilities
Personalized service enablement

Technical Highlights

Secure Data Access: MCP controls exactly what data AI can access
Enterprise Scale: Runs on Kubernetes with auto-scaling
Real-time Processing: Sub-2-second response times
Extensible Architecture: Easy to add new capabilities

📊 Demo Data
The demo includes realistic retail data:
Products

Nike Air Max 270 - Multiple sizes and colors
Adidas Ultraboost 22 - Athletic footwear line
Levi's 501 Original Jeans - Classic apparel

Customers

John Smith - Gold tier customer with extensive history
Sarah Johnson - Silver tier customer with recent orders

Orders

ORD-1001 - Delivered Nike order
ORD-1005 - Shipped Adidas order with tracking

🔧 Customization
Adding New Products
Edit retail_data.json:
json{
  "product_id": "BRAND-###",
  "name": "Product Name",
  "category": "Category",
  "sizes": {"8": 10, "9": 15},
  "price": 99.99,
  "colors": ["Color1", "Color2"],
  "location": "Warehouse X"
}
Adding New MCP Tools
Extend the RetailMCPTools class in run_llamastack.py:
pythondef new_tool_function(self, param: str) -> Dict[str, Any]:
    # Tool implementation
    return {"result": "data"}
Branding Customization
Modify templates/index.html for:

Company colors and logos
Custom styling
Branded messaging

🏢 Business Value
For Retailers

Operational Efficiency: Reduce manual inventory lookups
Customer Experience: Instant, accurate information
Staff Productivity: AI-powered customer service tools
Data Insights: Natural language business intelligence

For IT Organizations

Enterprise Ready: Production-grade deployment on OpenShift
Secure Architecture: Controlled data access via MCP
Scalable Platform: Kubernetes-native scaling
Integration Friendly: API-first design for system integration

🔧 Technical Stack
ComponentTechnologyPurposeContainer PlatformRed Hat OpenShiftEnterprise KubernetesAI OrchestrationFastAPI + PythonRequest processingData IntegrationMCP ToolsSecure data accessFrontendHTML5 + JavaScriptDemo interfaceLanguage ModelSimulated Llama-3.2-3BNatural language processing
📈 Monitoring & Operations
Health Checks

Endpoint: /health
Expected Response: {"status":"healthy","service":"retail-ai-assistant"}

Logging
bash# View application logs
oc logs -f deployment/retail-ai-assistant

# Check pod status
oc get pods -l app=retail-ai-assistant

# Monitor resource usage
oc top pods
Scaling
bash# Scale up for higher load
oc scale deployment/retail-ai-assistant --replicas=3

# Adjust resource limits
oc set resources deployment/retail-ai-assistant --requests=cpu=200m,memory=512Mi
🐛 Troubleshooting
Common Issues
Build Failures:
bashoc logs -f bc/retail-ai-assistant
Pod Not Starting:
bashoc describe pod -l app=retail-ai-assistant
oc get events --sort-by=.metadata.creationTimestamp
Route Not Working:
bash# Use port-forward as alternative
oc port-forward deployment/retail-ai-assistant 8000:8000
# Access at http://localhost:8000
Resource Constraints (OpenShift Local):
bash# Reduce resource requirements
oc set resources deployment/retail-ai-assistant --requests=cpu=50m,memory=256Mi --limits=cpu=200m,memory=512Mi
Reset Everything
bashoc delete project retail-ai-demo
# Then run deploy-local.sh again
🚀 Production Considerations
Security

Implement proper authentication/authorization
Use secure secrets management for API keys
Enable TLS/SSL for external access
Regular security scanning of container images

Performance

Connect to real databases via connection pooling
Implement caching for frequently accessed data
Use production-grade LLM endpoints
Configure horizontal pod autoscaling

Integration

Replace mock data with real retail systems
Implement proper error handling and retry logic
Add comprehensive logging and monitoring
Set up CI/CD pipelines for updates

📝 Next Steps

Expand Demo: Add more retail scenarios (returns, promotions, analytics)
Real Integration: Connect to actual retail databases and APIs
Advanced AI: Implement RAG, multi-modal capabilities
Production Deploy: Move to production OpenShift cluster

📞 Support
Demo Support

Check troubleshooting section above
Review OpenShift Local documentation
Verify all required files are present

Red Hat Resources

OpenShift AI Documentation
OpenShift Local Setup
Container Platform Guide

📄 License
This demo is provided as-is for educational and demonstration purposes.

Ready to showcase the future of retail AI on Red Hat OpenShift! 🛍️✨