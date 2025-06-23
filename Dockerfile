# Use Python 3.11 as base image (UBI for better OpenShift compatibility)
FROM registry.access.redhat.com/ubi9/python-311:latest

# Set working directory
WORKDIR /app

# Switch to root for package installation and directory setup
USER 0

# Install system dependencies
RUN dnf update -y && dnf install -y \
    git \
    && dnf clean all

# Install Python dependencies first (as root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for model storage and set permissions
RUN mkdir -p /app/models && \
    chown -R 1001:0 /app && \
    chmod -R g+rwx /app

# Switch back to non-root user for OpenShift security
USER 1001

# Expose port for the service
EXPOSE 8000

# Command to run the application
CMD ["python", "run_llamastack.py"]