# 🌱 Eco-Shift

**AI-Powered Logistics Optimization for Sustainable Supply Chain Management**

Eco-Shift is an intelligent multi-agent platform that leverages IBM watsonx.ai, the IBM Bee AI framework, and real-time weather data to optimize logistics operations, reduce carbon emissions, and promote sustainable supply chain practices.

Deployment ready on IBM cloud.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-blue)](https://www.ibm.com/watsonx)
[![Bee AI Framework](https://img.shields.io/badge/Bee-AI%20Framework-orange)](https://github.com/i-am-bee/bee-agent-framework)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Agent System](#-agent-system)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

Eco-Shift addresses the critical challenge of reducing carbon emissions in logistics operations through an intelligent multi-agent system that:

1. **🌦️ Real-time Weather Monitoring**: Continuously tracks weather conditions across vendor locations using OpenWeather API
2. **🤖 Intelligent Route Optimization**: Optimizes delivery routes based on weather patterns and emissions data
3. **🚛 Fleet Prioritization**: Recommends the most efficient vehicles with special emphasis on hydrogen and electric fleets
4. **📊 Emissions Tracking**: Calculates and monitors carbon footprint in real-time with AI-powered insights
5. **🧠 AI-Powered Decision Making**: Uses IBM watsonx.ai and Bee AI framework for intelligent recommendations

### What Makes Eco-Shift Unique?

- **Multi-Agent Architecture**: Three coordinating AI agents (Monitor, Auditor, Orchestrator) work together seamlessly
- **IBM Bee AI Framework**: Modern tool-based agent architecture with enhanced AI capabilities
- **Hydrogen Fleet Priority**: 10x scoring multiplier for hydrogen fleets to promote zero-emission logistics
- **Real-time Adaptation**: Automatic route adjustments based on severe weather conditions
- **Backward Compatible**: Supports both BeeAI and legacy agent implementations

---

## ✨ Key Features

### 🤖 Multi-Agent System (Powered by IBM Bee AI Framework)

#### **Monitor Agent** (Weather Intelligence)
- Continuous weather monitoring across all vendor locations
- Severe weather detection and alerting
- Weather impact analysis on logistics operations
- Proactive route adjustment recommendations
- 5-minute weather data caching to optimize API usage

#### **Auditor Agent** (Emissions Analysis)
- Real-time emissions calculation for all fleet types
- AI-powered vendor recommendations using IBM watsonx.ai
- Fleet prioritization with hydrogen fleet emphasis (10x multiplier)
- Route optimization for minimal carbon footprint
- Cost-benefit analysis for sustainable choices

#### **Orchestrator Agent** (Workflow Coordination)
- Coordinates Monitor and Auditor agent workflows
- Manages agent lifecycle and communication
- Aggregates results for frontend dashboard
- Handles error recovery and retry logic
- Supports both BeeAI and legacy agent modes

### 🌦️ Weather Intelligence

- **Real-time Data**: OpenWeather API integration with 5-minute caching
- **Severe Weather Alerts**: Automatic detection of storms, heavy rain, snow, fog
- **Impact Analysis**: Weather condition impact on delivery schedules
- **Proactive Routing**: Automatic route adjustments for weather avoidance
- **Alert Cooldown**: 30-minute cooldown per location to prevent alert spam

### 📊 Emissions Management

- **Multi-Fuel Support**: Diesel, petrol, electric, hybrid, and hydrogen fleets
- **Real-time Calculation**: Instant emissions calculation for any route
- **Baseline Comparison**: All calculations against diesel baseline (2.68 kg CO2e/L)
- **Zero-Emission Priority**: Hydrogen and electric fleets prioritized
- **AI Recommendations**: watsonx.ai powered optimization suggestions

**Emission Factors:**
- Diesel: 2.68 kg CO2e/L
- Petrol: 2.31 kg CO2e/L
- Hybrid: 1.34 kg CO2e/L (50% reduction)
- Electric: 0.0 kg CO2e (direct emissions)
- Hydrogen: 0.0 kg CO2e (direct emissions)

### 🚛 Fleet Optimization

- **Intelligent Prioritization**: Multi-factor scoring system
- **Hydrogen Fleet Boost**: 10x score multiplier for hydrogen vehicles
- **Route Optimization**: Minimal emissions path calculation
- **Load Balancing**: Efficient distribution across fleet
- **Maintenance Integration**: Considers vehicle availability and condition

### 📈 Interactive Dashboard

- **Real-time Metrics**: Live KPIs and performance indicators
- **Weather Visualization**: Current conditions and forecasts
- **Emissions Tracking**: Historical and real-time carbon footprint
- **Fleet Status**: Vehicle availability and efficiency metrics
- **AI Insights**: watsonx.ai recommendations and analysis

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ECO-SHIFT PLATFORM                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │              Frontend (Next.js 14 + TypeScript)              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │  Dashboard   │  │   Analytics  │  │   Settings   │      │  │
│  │  │   + GSAP     │  │   + Charts   │  │   + Config   │      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              │ REST API (FastAPI)                   │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                   Backend (FastAPI)                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │  API Routes  │  │   Services   │  │    Models    │      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │            Orchestrator Agent (Coordinator)                  │  │
│  │                                                              │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │         Message Bus (Pub/Sub Pattern)                 │  │  │
│  │  │  - Priority Queuing  - Request/Response              │  │  │
│  │  │  - Message TTL       - History Tracking              │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  │                                                              │  │
│  │  ┌──────────────────┐              ┌──────────────────┐    │  │
│  │  │  Monitor Agent   │◄────────────►│  Auditor Agent   │    │  │
│  │  │  (BeeAI)         │              │  (BeeAI)         │    │  │
│  │  │                  │              │                  │    │  │
│  │  │ - WeatherCheck   │              │ - EmissionsCalc  │    │  │
│  │  │ - VendorRetrieval│              │ - watsonx.ai     │    │  │
│  │  └──────────────────┘              └──────────────────┘    │  │
│  │         │                                     │             │  │
│  └─────────┼─────────────────────────────────────┼─────────────┘  │
│            │                                     │                 │
│            ▼                                     ▼                 │
│  ┌──────────────────┐              ┌──────────────────┐          │
│  │  OpenWeather API │              │  IBM watsonx.ai  │          │
│  │  (Weather Data)  │              │  (Granite Model) │          │
│  └──────────────────┘              └──────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Weather Monitoring**: Monitor Agent fetches weather data every 5 minutes (configurable)
2. **Alert Generation**: Severe weather conditions trigger high-priority alerts
3. **Audit Trigger**: Orchestrator receives alerts and triggers Auditor Agent
4. **AI Analysis**: Auditor calculates emissions and gets recommendations from watsonx.ai
5. **Results Aggregation**: Orchestrator combines results for frontend API
6. **Dashboard Update**: Frontend displays real-time recommendations and metrics

### Message Bus Architecture

The agents communicate via a custom message bus supporting:
- **Publish-Subscribe**: Broadcast messages to all subscribers
- **Direct Messaging**: Targeted messages to specific agents
- **Request-Response**: Synchronous-style communication with correlation IDs
- **Priority Queuing**: Critical messages processed first (negative priority values)
- **Message TTL**: Automatic expiration (default 3600 seconds)
- **History Tracking**: Message history for debugging (last 100 messages)

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14.2.3 (App Router)
- **Language**: TypeScript 5.4.5
- **Styling**: Tailwind CSS 3.4.3 (Brutalist Design)
- **Animations**: GSAP 3.12.5 (GreenSock)
- **UI Components**: Custom brutalist components
- **State Management**: React 18.3.1 Hooks
- **HTTP Client**: Axios with 30-second timeout
- **Date Handling**: date-fns

### Backend
- **Framework**: FastAPI 0.109.0+
- **Language**: Python 3.11+
- **Async Runtime**: asyncio, aiohttp
- **Validation**: Pydantic 2.5.3+
- **Testing**: pytest with coverage
- **Code Quality**: Black, Flake8, isort, mypy
- **Logging**: Structured JSON logging

### AI & Agent Framework
- **AI Platform**: IBM watsonx.ai 0.2.6+
- **Agent Framework**: IBM Bee AI Framework (with legacy fallback)
- **AI Model**: IBM Granite 13B Chat v2 (default)
- **Weather API**: OpenWeather API
- **Message Bus**: Custom pub/sub implementation

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Development**: Hot reload for both frontend and backend
- **Monitoring**: Built-in health checks and logging
- **CORS**: Configurable cross-origin support

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Git**
- **IBM watsonx.ai** account and API key ([Get started](https://www.ibm.com/watsonx))
- **OpenWeather** API key ([Get free key](https://openweathermap.org/api))

### Quick Start (5 Minutes)

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/eco-shift.git
cd eco-shift
```

#### 2. Install Dependencies

```bash
# Install root dependencies
npm install

# Install backend dependencies
cd apps/backend
pip install -r requirements.txt
cd ../..

# Install frontend dependencies
cd apps/frontend
npm install
cd ../..
```

#### 3. Configure Environment Variables

Create `.env` file in the root directory:

```bash
# IBM watsonx.ai (Required)
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2

# OpenWeather API (Required)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# BeeAI Framework Configuration
USE_BEEAI=true
BEEAI_LOG_LEVEL=INFO
BEEAI_TIMEOUT=30

# Application Settings
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=true

# Server Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000

# CORS (Frontend URL)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

Copy the same configuration to backend:

```bash
cp .env apps/backend/.env
```

#### 4. Start Development Servers

**Option 1: Using npm scripts (Recommended)**
```bash
npm run dev
```

**Option 2: Manual start**
```bash
# Terminal 1 - Backend
cd apps/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd apps/frontend
npm run dev
```

**Option 3: Using Docker**
```bash
docker-compose up -d
```

#### 5. Access the Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

### Verify Installation

Test the agents are working:

```bash
cd apps/backend

# Test weather agent
python examples/beeai_weather_example.py

# Test auditor agent
python examples/beeai_auditor_example.py

# Test full orchestrator workflow
python -m src.agents.orchestrator.orchestrator_agent
```

---

## 📁 Project Structure

```
eco-shift/
├── apps/
│   ├── frontend/                    # Next.js 14 frontend application
│   │   ├── src/
│   │   │   ├── app/                # Next.js app directory (App Router)
│   │   │   │   ├── layout.tsx      # Root layout
│   │   │   │   └── page.tsx        # Homepage
│   │   │   ├── components/         # React components
│   │   │   │   ├── ui/            # Reusable UI components
│   │   │   │   └── CommandCenter.tsx  # Main dashboard
│   │   │   ├── lib/               # Utilities and API client
│   │   │   │   ├── api.ts         # Backend API client
│   │   │   │   └── animations.ts  # GSAP animations
│   │   │   ├── hooks/             # Custom React hooks
│   │   │   ├── styles/            # Global styles
│   │   │   │   └── globals.css    # Tailwind + custom styles
│   │   │   └── types/             # TypeScript type definitions
│   │   ├── public/                # Static assets
│   │   └── package.json
│   │
│   └── backend/                     # FastAPI backend application
│       ├── src/
│       │   ├── agents/             # Multi-agent system
│       │   │   ├── monitor/        # Weather monitoring agent (BeeAI)
│       │   │   │   ├── weather_monitor.py      # BeeAI implementation
│       │   │   │   ├── monitor_agent.py        # Legacy implementation
│       │   │   │   ├── vendors.py              # Vendor data
│       │   │   │   └── config.py               # Agent configuration
│       │   │   ├── auditor/        # Emissions auditing agent (BeeAI)
│       │   │   │   ├── beeai_auditor.py        # BeeAI implementation
│       │   │   │   ├── auditor_agent.py        # Legacy implementation
│       │   │   │   ├── emissions_calculator.py # Emissions logic
│       │   │   │   ├── fleet_prioritizer.py    # Fleet scoring
│       │   │   │   ├── route_optimizer.py      # Route optimization
│       │   │   │   └── config.py               # Agent configuration
│       │   │   └── orchestrator/   # Agent coordinator
│       │   │       ├── orchestrator_agent.py   # Main orchestrator
│       │   │       ├── message_bus.py          # Pub/sub messaging
│       │   │       └── config.py               # Orchestrator config
│       │   ├── api/                # FastAPI route handlers
│       │   │   ├── agents.py       # Agent management endpoints
│       │   │   ├── weather.py      # Weather data endpoints
│       │   │   ├── emissions.py    # Emissions tracking endpoints
│       │   │   ├── vendors.py      # Vendor endpoints
│       │   │   ├── chat.py         # AI chat endpoints
│       │   │   └── orchestrator.py # Orchestrator endpoints
│       │   ├── services/           # External service integrations
│       │   │   ├── watsonx_service.py  # IBM watsonx.ai client
│       │   │   └── weather_service.py  # OpenWeather API client
│       │   ├── models/             # Pydantic data models
│       │   │   └── schemas.py      # API request/response schemas
│       │   ├── config/             # Configuration management
│       │   │   └── settings.py     # Application settings
│       │   ├── utils/              # Utility functions
│       │   │   └── logger.py       # Logging configuration
│       │   └── main.py             # FastAPI application entry point
│       ├── examples/               # Example scripts
│       │   ├── beeai_weather_example.py   # Weather agent demo
│       │   └── beeai_auditor_example.py   # Auditor agent demo
│       ├── tests/                  # Test suite
│       ├── requirements.txt        # Python dependencies
│       ├── pyproject.toml         # Project configuration
│       ├── pytest.ini             # Pytest configuration
│       └── Dockerfile             # Docker configuration
│
├── packages/
│   └── types/                      # Shared TypeScript types
│       ├── index.ts
│       └── package.json
│
├── scripts/                        # Development scripts
│   ├── dev.ps1                    # Start dev servers (Windows)
│   ├── setup.ps1                  # Setup script (Windows)
│   └── test.ps1                   # Run tests (Windows)
│
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md            # Architecture details
│   └── QUICK_START.md             # Quick start guide
│
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Docker Compose configuration
├── package.json                   # Root package.json (monorepo)
├── AGENTS.md                      # Agent system documentation
├── BEEAI_MIGRATION_COMPLETE.md   # BeeAI migration summary
└── README.md                      # This file
```

---

## 🤖 Agent System

### BeeAI Framework Integration

Eco-Shift uses the **IBM Bee AI framework** for modern, tool-based agent architecture with enhanced AI capabilities.

#### Monitor Agent (BeeAI)

**Location**: `apps/backend/src/agents/monitor/weather_monitor.py`

**Purpose**: Real-time weather monitoring and vendor recommendations

**Tools**:
- `WeatherCheckTool` - Checks current weather conditions
- `VendorRetrievalTool` - Retrieves eco-friendly alternative vendors

**Usage**:
```python
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent

agent = BeeAIWeatherMonitorAgent(
    target_location="New York,US",
    api_key=os.getenv("OPENWEATHER_API_KEY")
)

result = await agent.check_weather()
# Returns: {status, reason, alternative_vendors}
```

**Response Format**:
```json
{
  "status": "reroute_required",
  "reason": "heavy thunderstorm",
  "alternative_vendors": [
    {
      "id": "vendor_001",
      "name": "EcoFleet Solutions",
      "location": "Boston,US",
      "fleet_type": "hydrogen",
      "distance_km": 350
    }
  ]
}
```

**Configuration**:
- Polling interval: 300 seconds (5 minutes)
- Weather cache: 300 seconds
- Alert cooldown: 1800 seconds (30 minutes)
- Severe weather conditions: thunderstorm, heavy rain, snow, fog

#### Auditor Agent (BeeAI)

**Location**: `apps/backend/src/agents/auditor/beeai_auditor.py`

**Purpose**: Emissions analysis and AI-powered vendor recommendations

**Tools**:
- `EmissionsCalculationTool` - Calculates emissions using watsonx.ai

**Usage**:
```python
from src.agents.auditor.beeai_auditor import BeeAIAuditorAgent

agent = BeeAIAuditorAgent()

result = await agent.analyze_vendors({
    "vendors": vendor_list,
    "location": "New York,US"
})
# Returns: {approved_vendor_id, emissions_saving, justification}
```

**Response Format**:
```json
{
  "status": "success",
  "approved_vendor_id": "vendor_001",
  "emissions_saving": "100% (zero direct emissions)",
  "justification": "Selected hydrogen fleet for zero direct emissions...",
  "vendors_analyzed": 4
}
```

**Fleet Prioritization**:
- Hydrogen fleets: 10x score multiplier (intentional business logic)
- Electric fleets: High priority
- Hybrid fleets: Medium priority
- Diesel/Petrol: Lower priority

#### Orchestrator Agent

**Location**: `apps/backend/src/agents/orchestrator/orchestrator_agent.py`

**Purpose**: Coordinates Monitor and Auditor agents, manages workflows

**Features**:
- Supports both BeeAI and legacy agents
- Automatic response format detection
- Feature flag controlled (`USE_BEEAI` environment variable)
- Manages agent lifecycle (start/stop)
- Aggregates results for frontend API

**Configuration**:
```python
# Enable BeeAI agents (default)
config = OrchestratorConfig(use_beeai=True)

# Or via environment variable
USE_BEEAI=true
```

**Workflow**:
1. Initialize agents (Monitor and Auditor)
2. Start background monitoring
3. Receive weather alerts from Monitor
4. Trigger Auditor for emissions analysis
5. Aggregate and return results

### Message Bus

**Location**: `apps/backend/src/agents/orchestrator/message_bus.py`

The message bus enables agent communication with:

**Patterns**:
- **Publish-Subscribe**: Broadcast to all subscribers
- **Direct Send**: Targeted messages to specific agents
- **Request-Response**: Synchronous-style communication

**Features**:
- Priority queuing (CRITICAL > HIGH > NORMAL > LOW)
- Message TTL (default 3600 seconds)
- Message history (last 100 messages)
- Queue size limit (1000 messages per agent)

**Usage**:
```python
from src.agents.orchestrator.message_bus import get_message_bus, Message, MessageType

# Get message bus instance
message_bus = get_message_bus()

# Publish message
message = Message(
    type=MessageType.WEATHER_ALERT,
    sender="monitor_agent",
    payload={"location": "New York", "severity": "high"},
    priority=MessagePriority.HIGH
)
await message_bus.publish(message)

# Subscribe to messages
def callback(message: Message):
    print(f"Received: {message.payload}")

message_bus.subscribe(MessageType.WEATHER_ALERT, callback)
```

### Legacy Agent Support

The system maintains backward compatibility with legacy agents:

**Legacy Monitor Agent**: `apps/backend/src/agents/monitor/monitor_agent.py`
**Legacy Auditor Agent**: `apps/backend/src/agents/auditor/auditor_agent.py`

To use legacy agents:
```bash
# In .env
USE_BEEAI=false
```

---

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Health Check
```bash
GET /health
# Returns: {"status": "healthy", "timestamp": "..."}
```

#### Agents
```bash
GET  /api/agents/status              # Get all agent statuses
POST /api/agents/start               # Start all agents
POST /api/agents/stop                # Stop all agents
GET  /api/agents/orchestrator/results # Get latest orchestrator results
POST /api/agents/orchestrator/run    # Run orchestrator workflow
```

#### Weather
```bash
GET  /api/weather/current?location=New York,US  # Get current weather
GET  /api/weather/alerts                        # Get active weather alerts
GET  /api/weather/forecast?location=New York,US # Get weather forecast
```

#### Vendors
```bash
GET  /api/vendors                    # List all vendors
GET  /api/vendors/{id}               # Get vendor details
GET  /api/vendors/{id}/weather       # Get vendor weather data
POST /api/vendors/search             # Search vendors by criteria
```

#### Emissions
```bash
POST /api/emissions/calculate        # Calculate emissions for route
GET  /api/emissions/stats            # Get emissions statistics
POST /api/emissions/optimize         # Get optimization recommendations
```

#### Chat (AI Assistant)
```bash
POST /api/chat                       # Chat with AI assistant
# Body: {"message": "How can I reduce emissions?"}
```

### Example API Calls

**Get Current Weather**:
```bash
curl http://localhost:8000/api/weather/current?location=New%20York,US
```

**Run Orchestrator Workflow**:
```bash
curl -X POST http://localhost:8000/api/agents/orchestrator/run \
  -H "Content-Type: application/json" \
  -d '{"location": "New York,US"}'
```

**Calculate Emissions**:
```bash
curl -X POST http://localhost:8000/api/emissions/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "distance_km": 500,
    "fuel_type": "hydrogen",
    "fuel_consumption_l": 0
  }'
```

---

## 💻 Development

### Running Tests

**All tests**:
```bash
npm run test
```

**Frontend only**:
```bash
cd apps/frontend
npm test
```

**Backend only**:
```bash
cd apps/backend
pytest
```

**With coverage**:
```bash
cd apps/backend
pytest --cov=src --cov-report=html
```

**Specific test file**:
```bash
pytest tests/unit/test_agents.py -v
```

### Code Quality

**Linting**:
```bash
# All
npm run lint

# Frontend only
npm run lint:frontend

# Backend only
npm run lint:backend
```

**Formatting**:
```bash
# All
npm run format

# Frontend only
npm run format:frontend

# Backend only
npm run format:backend
```

**Type checking**:
```bash
npm run type-check
```

### Development Commands

```bash
# Development
npm run dev                    # Start both frontend and backend
npm run dev:frontend           # Frontend only (port 3000)
npm run dev:backend            # Backend only (port 8000)

# Building
npm run build                  # Build both apps
npm run build:frontend         # Next.js production build
npm run build:backend          # Install Python dependencies

# Docker
npm run docker:build           # Build Docker images
npm run docker:up              # Start containers
npm run docker:down            # Stop containers
npm run docker:logs            # View logs
npm run docker:clean           # Remove containers and volumes

# Agent Management
npm run agents:status          # Check agent statuses
npm run agents:start           # Start all agents
npm run agents:stop            # Stop all agents

# Utilities
npm run health                 # Check health of both services
npm run logs                   # Tail backend logs
```

### Environment Variables

See `.env.example` for all available configuration options.

**Required**:
- `WATSONX_API_KEY` - IBM watsonx.ai API key
- `WATSONX_PROJECT_ID` - IBM watsonx.ai project ID
- `OPENWEATHER_API_KEY` - OpenWeather API key

**Optional**:
- `USE_BEEAI` - Enable BeeAI framework (default: true)
- `WATSONX_MODEL_ID` - AI model ID (default: ibm/granite-13b-chat-v2)
- `LOG_LEVEL` - Logging level (default: INFO)
- `BACKEND_PORT` - Backend server port (default: 8000)
- `CORS_ORIGINS` - Allowed CORS origins (default: http://localhost:3000)

### Adding New Features

**Add New API Endpoint**:
1. Create route in `apps/backend/src/api/`
2. Define Pydantic schemas in `apps/backend/src/models/schemas.py`
3. Add business logic in services or agents
4. Update frontend API client in `apps/frontend/src/lib/api.ts`
5. Add tests

**Add New Agent Tool**:
1. Create tool class extending `Tool` from Bee AI framework
2. Implement `execute()` method
3. Add tool to agent's tool list
4. Update agent documentation

**Add New Frontend Component**:
1. Create component in `apps/frontend/src/components/`
2. Use TypeScript interfaces for props
3. Import types from `apps/frontend/src/types/index.ts`
4. Use Tailwind CSS for styling
5. Add GSAP animations if needed

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Scale backend services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### Manual Deployment

**Frontend**:
```bash
cd apps/frontend
npm run build
npm start
```

**Backend**:
```bash
cd apps/backend
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment-Specific Configuration

- **Development**: `.env`
- **Staging**: `.env.staging`
- **Production**: `.env.production`

### Production Checklist

- [ ] Set `DEBUG=false`
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure production database (if using)
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (nginx/Apache)
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Enable rate limiting
- [ ] Configure API authentication

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow existing code style
   - Write tests for new features
   - Update documentation
4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Code Style Guidelines

**Python (Backend)**:
- Line length: 100 characters
- Use Black for formatting
- Use flake8 for linting
- Type hints required
- Google-style docstrings

**TypeScript (Frontend)**:
- Line length: 100 characters
- Use Prettier for formatting
- Use ESLint for linting
- Functional components with hooks
- TypeScript interfaces for props

### Commit Message Format

```
type(scope): subject

body

footer
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Example**:
```
feat(agents): add hydrogen fleet prioritization

Implement 10x score multiplier for hydrogen fleets to promote
zero-emission logistics operations.

Closes #123
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM watsonx.ai** - AI capabilities and Granite models
- **IBM Bee AI Framework** - Modern agent framework
- **OpenWeather** - Weather data API
- **Next.js** and **FastAPI** - Excellent frameworks
- **IBM Bob Hackathon** - Inspiration and support
- All contributors and supporters

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Agent System Guide**: [AGENTS.md](AGENTS.md)
- **BeeAI Migration**: [BEEAI_MIGRATION_COMPLETE.md](BEEAI_MIGRATION_COMPLETE.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/eco-shift/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/eco-shift/discussions)

---

## 🗺️ Roadmap

### Current Version (v1.0.0)
- ✅ Multi-agent system with BeeAI framework
- ✅ Real-time weather monitoring
- ✅ Emissions calculation and tracking
- ✅ Fleet prioritization with hydrogen emphasis
- ✅ Interactive dashboard with GSAP animations
- ✅ IBM watsonx.ai integration

### Upcoming Features
- [ ] Mobile application (React Native)
- [ ] Advanced analytics and ML models
- [ ] Integration with more weather providers
- [ ] Real-time vehicle tracking with GPS
- [ ] Multi-language support (i18n)
- [ ] Enhanced reporting and export capabilities
- [ ] API rate limiting and authentication
- [ ] Webhook support for external integrations
- [ ] Database persistence for agent states
- [ ] Multi-tenant support

---

## 🌟 Key Highlights

- **🤖 Intelligent Multi-Agent System**: Three coordinating AI agents powered by IBM Bee AI framework
- **🧠 IBM watsonx.ai Integration**: Advanced AI recommendations using Granite models
- **🌦️ Real-time Weather Intelligence**: Proactive route adjustments based on weather conditions
- **♻️ Zero-Emission Priority**: 10x multiplier for hydrogen fleets to promote sustainability
- **📊 Comprehensive Analytics**: Real-time emissions tracking and optimization insights
- **🎨 Modern UI**: Brutalist design with GSAP animations for engaging user experience
- **🔄 Backward Compatible**: Supports both BeeAI and legacy agent implementations
- **🚀 Production Ready**: Docker support, comprehensive testing, and monitoring

---

**Built with ❤️ for a sustainable future**

*Eco-Shift - Transforming logistics through AI-powered sustainability*
