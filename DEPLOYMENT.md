# SUBFRACTURE LangGraph Deployment Guide

Complete deployment guide for production SUBFRACTURE brand intelligence system.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- LangGraph, LangSmith, LangChain
- Anthropic API key (Claude)
- Optional: OpenAI API key, Cognee for advanced memory

### 1. Environment Setup

```bash
# Clone and setup
git clone <repository>
cd subfracture-langgraph

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_key_here
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=subfracture-brand-intelligence

# Optional
OPENAI_API_KEY=your_openai_key_here
COGNEE_VECTOR_DB_URL=your_vector_db_url
COGNEE_GRAPH_DB_URL=your_graph_db_url
```

### 3. Quick Test

```bash
# Run demo workflow
python demo_workflow.py --sample

# Run interactive workshop
python workshop_manager.py --team-mode

# Run comprehensive tests
python run_tests.py --all
```

## 🏗️ Production Deployment

### Docker Deployment

1. **Build Container**
```bash
docker build -t subfracture-langgraph .
```

2. **Run Container**
```bash
docker run -d \
  --name subfracture-app \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e LANGSMITH_API_KEY=$LANGSMITH_API_KEY \
  -v $(pwd)/data:/app/data \
  subfracture-langgraph
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subfracture-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: subfracture
  template:
    metadata:
      labels:
        app: subfracture
    spec:
      containers:
      - name: subfracture
        image: subfracture-langgraph:latest
        ports:
        - containerPort: 8000
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: subfracture-secrets
              key: anthropic-api-key
        - name: LANGSMITH_API_KEY
          valueFrom:
            secretKeyRef:
              name: subfracture-secrets
              key: langsmith-api-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### Cloud Platform Deployment

#### Vercel (Recommended for Demo)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### Railway

```bash
# Connect repository to Railway
railway login
railway link
railway up
```

#### AWS ECS/Fargate

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag subfracture-langgraph:latest <account>.dkr.ecr.us-east-1.amazonaws.com/subfracture:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/subfracture:latest

# Deploy with ECS task definition
aws ecs run-task --cluster subfracture-cluster --task-definition subfracture-task
```

## 🔧 Configuration Guide

### Core Configuration

Create `config/production.toml`:

```toml
[llm]
primary_model = "claude-3-5-sonnet-20241022"
max_tokens = 8192
temperature = 0.7

[langsmith]
project = "subfracture-production"
tracing_enabled = true

[memory]
max_memory_mb = 4096
checkpoint_retention_hours = 72
cognee_enabled = true

[performance]
max_concurrent_tasks = 12
optimization_enabled = true
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API access |
| `LANGSMITH_API_KEY` | Yes | LangSmith tracing |
| `LANGSMITH_PROJECT` | Yes | Project name |
| `OPENAI_API_KEY` | No | Optional for evaluation |
| `COGNEE_VECTOR_DB_URL` | No | Advanced memory |
| `COGNEE_GRAPH_DB_URL` | No | Knowledge graphs |
| `MAX_MEMORY_MB` | No | Memory limit (default: 2048) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

### Security Configuration

```bash
# Production secrets
kubectl create secret generic subfracture-secrets \
  --from-literal=anthropic-api-key=$ANTHROPIC_API_KEY \
  --from-literal=langsmith-api-key=$LANGSMITH_API_KEY \
  --from-literal=openai-api-key=$OPENAI_API_KEY
```

## 📊 Monitoring & Observability

### Health Checks

The system provides health check endpoints:

```bash
# System health
curl http://localhost:8000/health

# Memory status
curl http://localhost:8000/memory/status

# Performance metrics
curl http://localhost:8000/metrics
```

### LangSmith Monitoring

All workflows are automatically traced in LangSmith:

- **Premium Value Metrics**: ROI validation and quality assessment
- **Gravity Performance**: Real-time optimization tracking
- **Error Tracking**: Comprehensive error analysis
- **Performance Monitoring**: Execution time and efficiency

### Logging Configuration

```python
# Configure structured logging
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

## 🔄 Scaling & Performance

### Horizontal Scaling

```yaml
# Auto-scaling configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: subfracture-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: subfracture-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Performance Optimization

1. **Memory Management**
   - Automatic memory cleanup
   - State checkpointing
   - Cognee integration for advanced memory

2. **Async Optimization**
   - Intelligent task parallelization
   - Dependency-aware execution
   - Adaptive concurrency limiting

3. **Error Handling**
   - Circuit breaker patterns
   - Exponential backoff retries
   - Graceful degradation

### Database Integration

For production scale, integrate with:

```python
# Vector database for semantic search
COGNEE_VECTOR_DB_URL = "postgresql://user:pass@host:5432/vectors"

# Graph database for knowledge relationships
COGNEE_GRAPH_DB_URL = "neo4j://host:7687"

# Redis for caching and session management
REDIS_URL = "redis://host:6379/0"
```

## 🧪 Testing & Validation

### Pre-deployment Testing

```bash
# Run full test suite
python run_tests.py --all --coverage

# Performance testing
python run_tests.py --performance

# Load testing
python load_test.py --concurrent-users 50

# Integration testing
python integration_test.py --production-like
```

### Production Validation

```bash
# Health check
curl -f http://your-domain.com/health || exit 1

# Basic workflow test
python production_test.py --endpoint http://your-domain.com

# Memory management test
python memory_test.py --duration 3600  # 1 hour test
```

## 🔐 Security Considerations

### API Security

1. **Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

2. **Authentication**
```python
# JWT-based authentication
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

jwt_authentication = JWTAuthentication(
    secret=SECRET_KEY,
    lifetime_seconds=3600,
    tokenUrl="auth/jwt/login",
)
```

3. **Input Validation**
```python
# Strict input validation
from pydantic import validator

class BrandBriefInput(BaseModel):
    brand_brief: str
    
    @validator('brand_brief')
    def validate_brand_brief(cls, v):
        if len(v) < 10:
            raise ValueError('Brand brief too short')
        if len(v) > 10000:
            raise ValueError('Brand brief too long')
        return v
```

### Data Protection

- All API keys stored in secure secrets management
- Brand data encrypted at rest and in transit
- GDPR compliance for European operations
- SOC 2 compliance for enterprise customers

## 📈 Business Metrics & ROI

### Key Performance Indicators

1. **Brand Development Metrics**
   - Gravity index improvements: Target 20-40% within 12 months
   - Breakthrough discovery rate: 80%+ success rate
   - Validation checkpoint pass rate: 90%+

2. **Business Impact Metrics**
   - Client satisfaction scores: Target 4.5/5.0+
   - ROI delivery: 200-450% projected returns
   - Premium value justification: $50k+ validated investment

3. **Operational Metrics**
   - Workflow completion time: Target <2 hours
   - Error rate: <1% critical errors
   - System uptime: 99.9%+

### Revenue Tracking

```python
# Integrate with business metrics
revenue_attribution = {
    "brand_development_revenue": "$200k-450k per client",
    "methodology_licensing": "$50k-100k per partner",
    "training_certification": "$10k-25k per cohort",
    "strategic_consulting": "$150k-300k per engagement"
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Memory Issues**
```bash
# Check memory usage
python -c "from src.core.memory_manager import memory_manager; print(memory_manager.get_memory_summary())"

# Force cleanup
python -c "from src.core.memory_manager import memory_manager; await memory_manager._cleanup_memory()"
```

2. **API Rate Limits**
```bash
# Check rate limit status
python -c "from src.core.error_handler import error_handler; print(error_handler.get_error_summary())"
```

3. **Performance Issues**
```bash
# Check async optimization
python -c "from src.core.async_optimizer import async_optimizer; print(async_optimizer.get_performance_summary())"
```

### Support Contacts

- **Technical Issues**: Create GitHub issue
- **Business Support**: Contact enterprise team
- **Emergency**: Use incident response process

## 📚 Additional Resources

- **API Documentation**: `/docs` endpoint when running
- **LangSmith Dashboard**: Monitor all executions
- **Performance Metrics**: Built-in monitoring dashboards
- **Knowledge Base**: Cognee-powered semantic search

---

*This deployment guide ensures production-ready SUBFRACTURE brand intelligence with enterprise-grade reliability, security, and performance.*