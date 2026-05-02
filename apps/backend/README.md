# Eco-Shift Backend

AI-powered carbon emissions monitoring and optimization system backend built with FastAPI and IBM watsonx.ai.

## 🏗️ Architecture

The backend follows a modular architecture with:

- **FastAPI** - Modern, fast web framework with automatic API documentation
- **IBM watsonx.ai** - AI-powered analysis and recommendations
- **BeeAI Framework** - Agentic AI framework for autonomous agents
- **OpenWeather API** - Weather data integration
- **Async/Await** - Asynchronous operations for better performance

## 📁 Project Structure

```
apps/backend/
├── src/
│   ├── agents/              # AI agent implementations
│   │   ├── monitor/         # Agent A: Real-time monitoring
│   │   ├── auditor/         # Agent B: Analysis & recommendations
│   │   └── orchestrator/    # Agent coordination
│   ├── api/                 # FastAPI route handlers
│   │   ├── agents.py        # Agent management endpoints
│   │   ├── weather.py       # Weather data endpoints
│   │   ├── emissions.py     # Emissions tracking endpoints
│   │   └── vendors.py       # Vendor recommendation endpoints
│   ├── services/            # External service integrations
│   │   ├── watsonx_service.py   # IBM watsonx.ai integration
│   │   └── weather_service.py   # OpenWeather API integration
│   ├── models/              # Pydantic data models
│   │   └── schemas.py       # API request/response schemas
│   ├── config/              # Configuration management
│   │   └── settings.py      # Application settings
│   ├── utils/               # Utility functions
│   │   └── logger.py        # Logging configuration
│   └── main.py              # FastAPI application entry point
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
├── pytest.ini              # Pytest configuration
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip or poetry for package management
- IBM watsonx.ai account and API key
- OpenWeather API key (optional)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd apps/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   # Required:
   # - WATSONX_API_KEY
   # - WATSONX_PROJECT_ID
   # Optional:
   # - OPENWEATHER_API_KEY
   ```

5. **Run the application**:
   ```bash
   # Development mode with auto-reload
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   
   # Or using Python directly
   python -m src.main
   ```

6. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 🔧 Configuration

Configuration is managed through environment variables. See `.env.example` for all available options.

### Key Configuration Options

```bash
# Application
APP_NAME=Eco-Shift Backend
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# IBM watsonx.ai
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2

# OpenWeather API
OPENWEATHER_API_KEY=your_api_key_here

# Agents
AGENT_MONITOR_ENABLED=true
AGENT_AUDITOR_ENABLED=true
AGENT_ORCHESTRATOR_ENABLED=true
```

## 📚 API Documentation

### Health Check
```bash
GET /health
```

### Agents
```bash
GET  /api/agents              # List all agents
GET  /api/agents/{agent_id}   # Get agent details
POST /api/agents/action       # Perform agent action (start/stop/restart)
POST /api/agents/orchestrate  # Trigger orchestration
GET  /api/agents/workflows/history  # Get workflow history
```

### Emissions
```bash
POST   /api/emissions         # Log emission data
GET    /api/emissions         # Get emission records
GET    /api/emissions/summary # Get emissions summary
POST   /api/emissions/analyze # Analyze emissions with AI
GET    /api/emissions/suggestions  # Get optimization suggestions
DELETE /api/emissions         # Clear all emissions (testing)
```

### Weather
```bash
GET  /api/weather/current     # Get current weather
POST /api/weather/current     # Get current weather (POST)
GET  /api/weather/forecast    # Get weather forecast
GET  /api/weather/air-quality # Get air quality data
```

### Vendors
```bash
GET  /api/vendors             # List vendors
GET  /api/vendors/{vendor_id} # Get vendor details
POST /api/vendors/search      # Search vendors
GET  /api/vendors/recommendations  # Get AI recommendations
GET  /api/vendors/categories  # List vendor categories
```

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v
```

## 🐳 Docker

Build and run with Docker:

```bash
# Build image
docker build -t eco-shift-backend .

# Run container
docker run -p 8000:8000 --env-file .env eco-shift-backend

# Using docker-compose (if available)
docker-compose up
```

## 🔍 Code Quality

### Linting
```bash
# Run flake8
flake8 src/

# Run black (formatter)
black src/

# Run isort (import sorting)
isort src/

# Run mypy (type checking)
mypy src/
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🤖 Agents

### Monitor Agent (Agent A)
- Real-time emissions monitoring
- Anomaly detection
- Alert generation
- Weather data integration

### Auditor Agent (Agent B)
- Historical data analysis
- Vendor recommendations
- Optimization suggestions
- ROI calculations

### Orchestrator Agent
- Coordinates Monitor and Auditor agents
- Manages workflow execution
- Aggregates results
- Handles scheduling

## 🔐 Security

- API key authentication (to be implemented)
- CORS configuration for frontend
- Input validation with Pydantic
- Rate limiting (configurable)
- Secure environment variable handling

## 📊 Monitoring

- Structured JSON logging in production
- Health check endpoint
- Metrics collection (optional)
- Error tracking with Sentry (optional)

## 🚧 Development

### Adding New Endpoints

1. Create route handler in `src/api/`
2. Define Pydantic models in `src/models/schemas.py`
3. Add business logic in services or agents
4. Update API router in `src/api/__init__.py`
5. Add tests in `tests/`

### Adding New Agents

1. Create agent class inheriting from `BaseAgent`
2. Implement required methods: `initialize()`, `execute()`, `cleanup()`
3. Register agent in orchestrator
4. Add agent-specific endpoints if needed

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Ensure virtual environment is activated
2. **API key errors**: Check `.env` file configuration
3. **Port already in use**: Change PORT in `.env` or kill existing process
4. **CORS errors**: Add frontend URL to CORS_ORIGINS

### Debug Mode

Enable debug logging:
```bash
LOG_LEVEL=DEBUG uvicorn src.main:app --reload
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📧 Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Documentation: See `docs/` directory
- Architecture: See `docs/ARCHITECTURE.md`

## 🔄 Version History

- **0.1.0** - Initial release
  - FastAPI backend setup
  - Agent framework implementation
  - IBM watsonx.ai integration
  - OpenWeather API integration
  - Basic CRUD operations

---

Built with ❤️ for the IBM Bob Hackathon