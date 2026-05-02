# 🌱 Eco-Shift

**AI-Powered Logistics Optimization for Sustainable Supply Chain Management**

Eco-Shift is an intelligent platform that leverages IBM watsonx.ai and real-time weather data to optimize logistics operations, reduce carbon emissions, and promote sustainable supply chain practices.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Agent System](#agent-system)
- [Development](#development)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Eco-Shift addresses the critical challenge of reducing carbon emissions in logistics operations by:

1. **Real-time Weather Monitoring**: Tracks weather conditions across vendor locations
2. **Intelligent Route Optimization**: Optimizes delivery routes based on weather and emissions
3. **Fleet Prioritization**: Recommends the most efficient vehicles for each route
4. **Emissions Tracking**: Calculates and monitors carbon footprint in real-time
5. **AI-Powered Insights**: Uses IBM watsonx.ai for intelligent decision-making

---

## ✨ Features

### 🤖 Multi-Agent System
- **Monitor Agent**: Continuously monitors weather conditions and vendor locations
- **Auditor Agent**: Analyzes emissions, optimizes routes, and prioritizes fleet
- **Orchestrator Agent**: Coordinates workflow between agents

### 🌦️ Weather Intelligence
- Real-time weather data from OpenWeather API
- Weather alerts for severe conditions
- Impact analysis on logistics operations
- Proactive route adjustments

### 📊 Emissions Management
- Real-time emissions calculation
- Fuel type comparison (diesel, petrol, electric, hybrid)
- Carbon footprint tracking
- Reduction recommendations

### 🚛 Fleet Optimization
- Vehicle prioritization based on efficiency
- Route optimization for minimal emissions
- Load balancing across fleet
- Maintenance scheduling integration

### 📈 Analytics Dashboard
- Real-time metrics and KPIs
- Interactive charts and visualizations
- Historical data analysis
- Export capabilities

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ECO-SHIFT PLATFORM                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Frontend (Next.js)                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │  Dashboard   │  │   Analytics  │  │   Settings   │      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              │ REST API                             │
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
│  │                  Orchestrator Agent                          │  │
│  │                                                              │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │              Message Bus (Pub/Sub)                    │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  │                                                              │  │
│  │  ┌──────────────┐                    ┌──────────────┐      │  │
│  │  │   Monitor    │◄──────────────────►│   Auditor    │      │  │
│  │  │    Agent     │                    │    Agent     │      │  │
│  │  └──────────────┘                    └──────────────┘      │  │
│  │         │                                     │             │  │
│  └─────────┼─────────────────────────────────────┼─────────────┘  │
│            │                                     │                 │
│            ▼                                     ▼                 │
│  ┌──────────────────┐              ┌──────────────────┐          │
│  │  OpenWeather API │              │  IBM watsonx.ai  │          │
│  └──────────────────┘              └──────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Weather Monitoring**: Monitor Agent fetches weather data from OpenWeather API
2. **Alert Generation**: Severe weather conditions trigger alerts
3. **Audit Trigger**: Orchestrator receives alerts and triggers Auditor Agent
4. **Analysis**: Auditor calculates emissions and optimizes routes using watsonx.ai
5. **Results**: Optimized recommendations sent to frontend dashboard
6. **Action**: Users review and implement recommendations

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: React Hooks
- **Charts**: Recharts
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Async**: asyncio, aiohttp
- **Validation**: Pydantic
- **Testing**: pytest
- **Code Quality**: Black, Flake8

### AI & Data
- **AI Platform**: IBM watsonx.ai
- **Weather API**: OpenWeather
- **Agent Framework**: Custom multi-agent system
- **Message Bus**: Custom pub/sub implementation

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL (optional)
- **Caching**: Redis (optional)
- **Monitoring**: Built-in logging and metrics

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Git**
- **IBM watsonx.ai** account and API key
- **OpenWeather** API key

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/eco-shift.git
cd eco-shift
```

#### 2. Run Setup Script

**Windows (PowerShell):**
```powershell
.\scripts\setup.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

#### 3. Configure Environment Variables

Edit `.env` file with your API keys:

```bash
# IBM watsonx.ai
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here

# OpenWeather
OPENWEATHER_API_KEY=your_api_key_here
```

#### 4. Start Development Servers

**Windows (PowerShell):**
```powershell
.\scripts\dev.ps1
```

**Linux/Mac:**
```bash
./scripts/dev.sh
```

**Or use npm:**
```bash
npm run dev
```

#### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Using Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📁 Project Structure

```
eco-shift/
├── apps/
│   ├── frontend/              # Next.js frontend application
│   │   ├── src/
│   │   │   ├── app/          # Next.js app directory
│   │   │   ├── components/   # React components
│   │   │   ├── lib/          # Utilities and API client
│   │   │   ├── styles/       # Global styles
│   │   │   └── types/        # TypeScript types
│   │   ├── public/           # Static assets
│   │   └── package.json
│   │
│   └── backend/              # FastAPI backend application
│       ├── src/
│       │   ├── agents/       # Agent system
│       │   │   ├── monitor/  # Weather monitoring agent
│       │   │   ├── auditor/  # Emissions auditing agent
│       │   │   └── orchestrator/ # Agent coordinator
│       │   ├── api/          # API routes
│       │   ├── config/       # Configuration
│       │   ├── models/       # Data models
│       │   ├── services/     # Business logic
│       │   └── utils/        # Utilities
│       ├── tests/            # Test suite
│       └── requirements.txt
│
├── packages/
│   └── types/                # Shared TypeScript types
│
├── scripts/                  # Development scripts
│   ├── dev.ps1              # Start dev servers (Windows)
│   ├── setup.ps1            # Setup script (Windows)
│   └── test.ps1             # Run tests (Windows)
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md      # Architecture details
│   └── QUICK_START.md       # Quick start guide
│
├── .env.example             # Environment variables template
├── docker-compose.yml       # Docker Compose configuration
├── package.json             # Root package.json
└── README.md               # This file
```

---

## 🤖 Agent System

### Monitor Agent

**Purpose**: Continuously monitors weather conditions across vendor locations

**Responsibilities**:
- Fetch real-time weather data from OpenWeather API
- Track weather conditions for all vendor locations
- Generate alerts for severe weather conditions
- Identify affected vendors
- Provide weather forecasts

**Configuration**: `apps/backend/src/agents/monitor/config.py`

### Auditor Agent

**Purpose**: Analyzes emissions and optimizes logistics operations

**Responsibilities**:
- Calculate emissions for routes and vehicles
- Optimize routes for minimal emissions
- Prioritize fleet based on efficiency
- Generate recommendations using watsonx.ai
- Provide cost-benefit analysis

**Configuration**: `apps/backend/src/agents/auditor/config.py`

### Orchestrator Agent

**Purpose**: Coordinates workflow between Monitor and Auditor agents

**Responsibilities**:
- Manage agent lifecycle
- Coordinate inter-agent communication
- Handle weather alerts and trigger audits
- Aggregate results for frontend
- Implement retry logic and error handling

**Configuration**: `apps/backend/src/agents/orchestrator/config.py`

### Message Bus

The agents communicate via a custom message bus that supports:
- Publish-subscribe pattern
- Priority-based message queuing
- Request-response patterns
- Message expiration (TTL)
- Message history for debugging

---

## 💻 Development

### Running Tests

**All tests:**
```bash
npm run test
```

**Frontend only:**
```bash
cd apps/frontend
npm test
```

**Backend only:**
```bash
cd apps/backend
pytest
```

**With coverage:**
```powershell
.\scripts\test.ps1 -Coverage
```

### Code Quality

**Linting:**
```bash
npm run lint
```

**Formatting:**
```bash
npm run format
```

**Type checking:**
```bash
npm run type-check
```

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `WATSONX_API_KEY`: IBM watsonx.ai API key
- `WATSONX_PROJECT_ID`: IBM watsonx.ai project ID
- `OPENWEATHER_API_KEY`: OpenWeather API key
- `BACKEND_PORT`: Backend server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: info)

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Manual Deployment

**Frontend:**
```bash
cd apps/frontend
npm run build
npm start
```

**Backend:**
```bash
cd apps/backend
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Environment-Specific Configuration

- **Development**: `.env`
- **Staging**: `.env.staging`
- **Production**: `.env.production`

---

## 📚 API Documentation

### Interactive API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Agents
- `GET /api/agents/status` - Get all agent statuses
- `POST /api/agents/orchestrator/run` - Run orchestrator workflow
- `GET /api/agents/orchestrator/results` - Get latest results

#### Weather
- `GET /api/weather/current` - Get current weather for all vendors
- `GET /api/weather/alerts` - Get active weather alerts
- `GET /api/weather/forecast` - Get weather forecast

#### Vendors
- `GET /api/vendors` - List all vendors
- `GET /api/vendors/{id}` - Get vendor details
- `GET /api/vendors/{id}/weather` - Get vendor weather data

#### Emissions
- `POST /api/emissions/calculate` - Calculate emissions
- `GET /api/emissions/stats` - Get emissions statistics
- `POST /api/emissions/optimize` - Get optimization recommendations

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style
- Write tests for new features
- Update documentation
- Keep commits atomic and well-described
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM watsonx.ai** for AI capabilities
- **OpenWeather** for weather data
- **Next.js** and **FastAPI** communities
- All contributors and supporters

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/eco-shift/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/eco-shift/discussions)

---

## 🗺️ Roadmap

- [ ] Mobile application
- [ ] Advanced analytics and ML models
- [ ] Integration with more weather providers
- [ ] Real-time vehicle tracking
- [ ] Multi-language support
- [ ] Enhanced reporting capabilities
- [ ] API rate limiting and authentication
- [ ] Webhook support for external integrations

---

**Built with ❤️ for a sustainable future**