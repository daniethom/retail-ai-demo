# Troubleshooting Guide

This guide helps resolve common issues when setting up and running the Retail AI Assistant demo.

## 🚨 Common Issues & Solutions

### OpenShift Local (CRC) Issues

#### 1. CRC Won't Start
```bash
# Check CRC status
crc status

# Common fixes
crc stop
crc delete
crc setup
crc start

# Check system resources
crc config get memory
crc config get cpus
```

**Minimum Requirements:**
- 8GB RAM available for CRC
- 4 CPU cores
- 35GB free disk space

#### 2. Disk Pressure Issues
```
Error: node(s) had untolerated taint {node.kubernetes.io/disk-pressure}
```

**Solution:**
```bash
# Clean up CRC
crc stop
crc cleanup
crc start

# Or increase disk allocation
crc config set disk-size 50
crc delete
crc start
```

#### 3. Memory Issues
```
Error: Insufficient memory
```

**Solution:**
```bash
# Increase CRC memory
crc config set memory 16384  # 16GB
crc delete
crc start

# Or reduce app resources
oc set resources deployment/retail-ai-assistant \
  --requests=cpu=50m,memory=256Mi \
  --limits=cpu=200m,memory=512Mi
```

### Build Issues

#### 1. Build Fails - Missing Dependencies
```
ERROR: Could not find a version that satisfies the requirement
```

**Solution:**
```bash
# Check requirements.txt format
cat requirements.txt

# Manually test pip install
pip install -r requirements.txt

# Update to known working versions
pip freeze > requirements.txt
```

#### 2. Permission Denied in Build
```
mkdir: cannot create directory '/app/models': Permission denied
```

**Solution:** Already fixed in current Dockerfile, but if you see this:
```dockerfile
# Switch to root, create dirs, set permissions, then switch back
USER 0
RUN mkdir -p /app/models && \
    chown -R 1001:0 /app && \
    chmod -R g+rwx /app
USER 1001
```

#### 3. Build Timeout
```bash
# Increase timeout
oc start-build retail-ai-assistant --from-dir=. --follow --timeout=600s
```

### Deployment Issues

#### 1. Pod Stuck in Pending
```bash
# Check what's wrong
oc describe pod -l app=retail-ai-assistant

# Common fixes
oc get nodes  # Check node capacity
oc get events --sort-by=.metadata.creationTimestamp

# Reduce resources if needed
oc set resources deployment/retail-ai-assistant \
  --requests=cpu=50m,memory=256Mi \
  --limits=cpu=200m,memory=512Mi
```

#### 2. Pod CrashLoopBackOff
```bash
# Check logs
oc logs -f deployment/retail-ai-assistant

# Common causes:
# - Missing files (check templates/index.html exists)
# - Port conflicts
# - Python import errors
```

#### 3. ImagePullBackOff
```
Failed to pull image "retail-ai-assistant:latest"
```

**Solution:**
```bash
# Use full image path
oc set image deployment/retail-ai-assistant \
  retail-ai-assistant=image-registry.openshift-image-registry.svc:5000/retail-ai-demo/retail-ai-assistant:latest

# Or check image exists
oc get imagestreams
```

### Network/Route Issues

#### 1. Route Not Working
```
Application is not available
```

**Solutions:**
```bash
# Check route exists
oc get routes

# Recreate route
oc delete route/retail-ai-assistant
oc expose service/retail-ai-assistant

# Use port-forward as backup
oc port-forward deployment/retail-ai-assistant 8000:8000
```

#### 2. Service Not Found
```bash
# Check service
oc get svc/retail-ai-assistant
oc describe svc/retail-ai-assistant

# Recreate if needed
oc delete svc/retail-ai-assistant
oc expose deployment/retail-ai-assistant --port=8000
```

#### 3. DNS Issues with CRC
```bash
# Check if you can access via IP
oc get svc/retail-ai-assistant -o jsonpath='{.spec.clusterIP}'

# Try port-forward instead
oc port-forward svc/retail-ai-assistant 8000:8000
```

### Application Issues

#### 1. 500 Internal Server Error
```bash
# Check application logs
oc logs -f deployment/retail-ai-assistant

# Common causes:
# - Missing retail_data.json
# - Template file issues
# - Python import errors
```

#### 2. Demo Queries Not Working
**Check:** `retail_data.json` is present and valid
```bash
# Validate JSON
python -m json.tool retail_data.json

# Check file exists in container
oc exec deployment/retail-ai-assistant -- ls -la
```

#### 3. Slow Response Times
```bash
# Check resource usage
oc top pods

# Increase resources
oc set resources deployment/retail-ai-assistant \
  --requests=cpu=200m,memory=512Mi \
  --limits=cpu=500m,memory=1Gi
```

## 🔧 Development Issues

### Local Development

#### 1. Python Environment Issues
```bash
# Create clean environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Import Errors
```python
# Common fix - add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python run_llamastack.py
```

#### 3. Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill process or use different port
python run_llamastack.py --port 8001
```

### File Structure Issues

#### 1. Missing Templates
```
jinja2.exceptions.TemplateNotFound: index.html
```

**Solution:**
```bash
# Ensure correct structure
mkdir -p templates
# Copy index.html to templates/index.html
```

#### 2. Missing Data File
```
FileNotFoundError: retail_data.json
```

**Solution:**
```bash
# Check file exists
ls -la retail_data.json

# Check JSON is valid
python -c "import json; json.load(open('retail_data.json'))"
```

## 🚨 Emergency Fixes

### Complete Reset
```bash
# Nuclear option - start fresh
oc delete project retail-ai-demo
crc stop
crc cleanup
crc start
oc login -u developer -p developer
# Then run deploy-local.sh again
```

### Quick Demo Backup
If everything fails during a customer demo:

1. **Use port-forward:**
   ```bash
   oc port-forward deployment/retail-ai-assistant 8000:8000
   ```

2. **Run locally:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python run_llamastack.py
   ```

3. **Use screenshots:** Keep screenshots of working demo in `docs/`

## 📊 Diagnostic Commands

### System Health Check
```bash
# OpenShift status
oc status
oc get nodes
oc get events --sort-by=.metadata.creationTimestamp

# Application status
oc get pods -l app=retail-ai-assistant
oc describe deployment/retail-ai-assistant
oc logs -f deployment/retail-ai-assistant

# Resource usage
oc top nodes
oc top pods

# Network connectivity
oc get routes
oc get svc
curl http://retail-ai-assistant-retail-ai-demo.apps-crc.testing/health
```

### Build Diagnostics
```bash
# Build status
oc get builds
oc describe build/retail-ai-assistant-1
oc logs -f bc/retail-ai-assistant

# Image status
oc get imagestreams
oc describe is/retail-ai-assistant
```

## 🆘 Getting Help

### Log Collection
When asking for help, collect these logs:

```bash
# System info
crc version
oc version

# Application logs
oc logs deployment/retail-ai-assistant > app.log
oc describe pod -l app=retail-ai-assistant > pod.log
oc get events --sort-by=.metadata.creationTimestamp > events.log

# Build logs (if build failed)
oc logs bc/retail-ai-assistant > build.log
```

### Support Channels
- **GitHub Issues:** For bugs and questions
- **Red Hat Support:** For OpenShift Local issues
- **Internal Slack:** #openshift-ai-demos (if available)

## 📚 Additional Resources

- [OpenShift Local Troubleshooting](https://crc.dev/crc/troubleshooting/)
- [OpenShift Container Platform Documentation](https://docs.openshift.com/)
- [FastAPI Troubleshooting](https://fastapi.tiangolo.com/tutorial/debugging/)

---

**Remember: Most issues are resolved by clean restart of CRC and checking resource allocation!** 🚀