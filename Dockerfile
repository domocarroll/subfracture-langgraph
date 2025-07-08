# SUBFRACTURE LangGraph Production Dockerfile
# Multi-stage build for optimized production deployment

# Stage 1: Builder
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION=1.0.0
ARG VCS_REF

# Set labels
LABEL maintainer="SUBFRACTURE Team"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="SUBFRACTURE LangGraph"
LABEL org.label-schema.description="Physics-Based Brand Intelligence System"
LABEL org.label-schema.version=$VERSION
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.schema-version="1.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Stage 2: Production
FROM python:3.11-slim as production

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r subfracture && useradd -r -g subfracture subfracture

# Set work directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app /app

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/checkpoints /app/workshop_sessions && \
    chown -R subfracture:subfracture /app

# Switch to non-root user
USER subfracture

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LANGCHAIN_TRACING_V2=true
ENV LANGCHAIN_PROJECT=subfracture-production

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Alternative commands (uncomment as needed)
# CMD ["python", "demo_workflow.py", "--sample"]  # For demo deployment
# CMD ["python", "workshop_manager.py"]  # For workshop deployment