**User:**

<task>
Design the optimal monorepo directory structure for "Eco-Shift", a multi-agent supply chain orchestrator with the following requirements:

**Tech Stack:**
- Frontend: Next.js, Tailwind CSS, GSAP
- Backend: Python with BeeAI framework
- AI: IBM watsonx.ai Granite-3.0-8b

**Architecture Components:**
- Agent A (The Monitor): Python agent polling OpenWeather API, manages vendor lists
- Agent B (The Auditor): Python agent calculating Scope 3 emissions, prioritizes hydrogen-fueled fleets

**Requirements:**
1. Design a clean monorepo structure that separates frontend and backend
2. Include proper directories for:
   - Next.js frontend application
   - Python backend with BeeAI agents
   - Shared types/interfaces
   - Configuration files
   - Documentation
3. Consider scalability for adding more agents in the future
4. Include directories for tests, utilities, and shared resources
5. Plan for environment configuration management
6. Consider API integration points between frontend and backend

Please provide:
1. A detailed directory tree structure with explanations
2. Rationale for the chosen structure
3. How the agents will be organized
4. Where shared resources and configurations will live
5. Best practices for this specific tech stack combination

This is for a 48-hour hackathon, so prioritize clarity and rapid development while maintaining good architecture.

Use attempt_completion when done with your architectural plan.
</task>
<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.gitignore,README.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T06:42:31.400Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>


# Current Workspace Directory (c:/Users/super/OneDrive/Desktop/ibm bob hackathon) Files
.gitignore
AGENTS.md
README.md
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll design an optimal monorepo structure for your Eco-Shift supply chain orchestrator. Let me start by gathering some context about the current project state and then create a comprehensive architectural plan.

<read_file>
<args>
  <file>
    <path>README.md</path>
  </file>
  <file>
    <path>.gitignore</path>
  </file>
  <file>
    <path>AGENTS.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'README.md', '.gitignore', 'AGENTS.md'] Result:
<files>
<file><path>README.md</path>
<content lines="1-15">
 1 | # IBM Bob Hackathon
 2 | 
 3 | This project was created for the IBM Bob Hackathon.
 4 | 
 5 | ## Getting Started
 6 | 
 7 | Add your project description and setup instructions here.
 8 | 
 9 | ## Technologies Used
10 | 
11 | - List your technologies here
12 | 
13 | ## Contributors
14 | 
15 | - Your name here
</content>
</file>
<file><path>.gitignore</path>
<content lines="1-27">
 1 | # Dependencies
 2 | node_modules/
 3 | venv/
 4 | env/
 5 | __pycache__/
 6 | 
 7 | # IDE
 8 | .vscode/
 9 | .idea/
10 | 
11 | # OS
12 | .DS_Store
13 | Thumbs.db
14 | 
15 | # Build outputs
16 | dist/
17 | build/
18 | *.pyc
19 | 
20 | # Environment variables
21 | .env
22 | .env.local
23 | 
24 | # Logs
25 | *.log
26 | 
27 | # Made with Bob
</content>
</file>
<file><path>AGENTS.md</path>
<content lines="1-30">
 1 | # AGENTS.md
 2 | 
 3 | This file provides guidance to agents when working with code in this repository.
 4 | 
 5 | ## Project Overview
 6 | 
 7 | This is a new project for the IBM Bob Hackathon. As the codebase develops, this file will be updated with project-specific information to help agents work more effectively with the code.
 8 | 
 9 | ## Build, Test, and Lint Commands
10 | 
11 | *To be added as the project structure is established.*
12 | 
13 | ```bash
14 | # Build command: TBD
15 | # Test command: TBD
16 | # Lint command: TBD
17 | ```
18 | 
19 | ## Code Style Guidelines
20 | 
21 | *To be documented as coding conventions are established during development.*
22 | 
23 | ## Notes for Agents
24 | 
25 | - This is an early-stage project with minimal structure
26 | - This file should be updated as the project grows with:
27 |   - Non-obvious architectural decisions
28 |   - Project-specific conventions and patterns
29 |   - Important context that isn't evident from the code itself
30 |   - Common pitfalls or gotchas specific to this codebase
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.gitignore,README.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T06:42:35.665Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.03

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I'll create a comprehensive architectural plan for the Eco-Shift monorepo structure. Let me break this down into actionable steps.

<update_todo_list>
<todos>
[-] Analyze project requirements and tech stack constraints
[ ] Design the complete monorepo directory structure
[ ] Document the rationale for architectural decisions
[ ] Create detailed explanations for each major directory
[ ] Define agent organization strategy
[ ] Plan shared resources and configuration management
[ ] Document API integration points
[ ] Create visual architecture diagram
[ ] Provide implementation guidelines for hackathon context
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.gitignore,README.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T06:43:10.736Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.06

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze project requirements and tech stack constraints | In Progress |
| 2 | Design the complete monorepo directory structure | Pending |
| 3 | Document the rationale for architectural decisions | Pending |
| 4 | Create detailed explanations for each major directory | Pending |
| 5 | Define agent organization strategy | Pending |
| 6 | Plan shared resources and configuration management | Pending |
| 7 | Document API integration points | Pending |
| 8 | Create visual architecture diagram | Pending |
| 9 | Provide implementation guidelines for hackathon context | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<write_to_file>
<path>docs/ARCHITECTURE.md</path>
<content># Eco-Shift Monorepo Architecture

## 📋 Executive Summary

This document outlines the monorepo architecture for **Eco-Shift**, a multi-agent supply chain orchestrator designed for the IBM Bob Hackathon. The structure prioritizes rapid development while maintaining scalability and clean separation of concerns.

## 🏗️ Complete Directory Structure

```
eco-shift/
├── apps/
│   ├── frontend/                    # Next.js application
│   │   ├── src/
│   │   │   ├── app/                # Next.js 13+ app directory
│   │   │   │   ├── api/            # API routes (proxy to backend)
│   │   │   │   ├── dashboard/      # Dashboard pages
│   │   │   │   ├── layout.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── components/         # React components
│   │   │   │   ├── ui/             # Reusable UI components
│   │   │   │   ├── dashboard/      # Dashboard-specific components
│   │   │   │   ├── charts/         # Data visualization components
│   │   │   │   └── animations/     # GSAP animation components
│   │   │   ├── lib/                # Frontend utilities
│   │   │   │   ├── api-client.ts   # Backend API client
│   │   │   │   ├── animations.ts   # GSAP utilities
│   │   │   │   └── utils.ts
│   │   │   ├── hooks/              # Custom React hooks
│   │   │   ├── styles/             # Global styles
│   │   │   └── types/              # Frontend-specific types
│   │   ├── public/                 # Static assets
│   │   ├── tests/                  # Frontend tests
│   │   ├── next.config.js
│   │   ├── tailwind.config.js
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   └── backend/                     # Python backend application
│       ├── src/
│       │   ├── agents/             # BeeAI agent implementations
│       │   │   ├── __init__.py
│       │   │   ├── base_agent.py   # Base agent class
│       │   │   ├── monitor/        # Agent A: The Monitor
│       │   │   │   ├── __init__.py
│       │   │   │   ├── agent.py    # Monitor agent implementation
│       │   │   │   ├── weather_service.py
│       │   │   │   ├── vendor_manager.py
│       │   │   │   └── config.py
│       │   │   ├── auditor/        # Agent B: The Auditor
│       │   │   │   ├── __init__.py
│       │   │   │   ├── agent.py    # Auditor agent implementation
│       │   │   │   ├── emissions_calculator.py
│       │   │   │   ├── fleet_prioritizer.py
│       │   │   │   └── config.py
│       │   │   └── orchestrator/   # Agent coordination
│       │   │       ├── __init__.py
│       │   │       ├── coordinator.py
│       │   │       └── message_bus.py
│       │   ├── api/                # FastAPI/Flask REST API
│       │   │   ├── __init__.py
│       │   │   ├── main.py         # API entry point
│       │   │   ├── routes/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── agents.py   # Agent status/control endpoints
│       │   │   │   ├── emissions.py # Emissions data endpoints
│       │   │   │   ├── vendors.py  # Vendor management endpoints
│       │   │   │   └── weather.py  # Weather data endpoints
│       │   │   ├── middleware/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── cors.py
│       │   │   │   └── auth.py
│       │   │   └── schemas/        # Pydantic models
│       │   │       ├── __init__.py
│       │   │       ├── agent.py
│       │   │       ├── emissions.py
│       │   │       └── vendor.py
│       │   ├── services/           # Business logic layer
│       │   │   ├── __init__.py
│       │   │   ├── watsonx_service.py  # IBM watsonx.ai integration
│       │   │   ├── openweather_service.py
│       │   │   └── data_processor.py
│       │   ├── models/             # Data models
│       │   │   ├── __init__.py
│       │   │   ├── vendor.py
│       │   │   ├── emission.py
│       │   │   └── weather.py
│       │   ├── utils/              # Backend utilities
│       │   │   ├── __init__.py
│       │   │   ├── logger.py
│       │   │   ├── config.py
│       │   │   └── validators.py
│       │   └── db/                 # Database layer (if needed)
│       │       ├── __init__.py
│       │       └── connection.py
│       ├── tests/                  # Backend tests
│       │   ├── unit/
│       │   ├── integration/
│       │   └── conftest.py
│       ├── requirements.txt
│       ├── requirements-dev.txt
│       ├── pyproject.toml
│       └── README.md
│
├── packages/                        # Shared packages
│   ├── types/                      # Shared TypeScript types
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── agent.types.ts
│   │   │   ├── emissions.types.ts
│   │   │   ├── vendor.types.ts
│   │   │   └── api.types.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── config/                     # Shared configuration
│       ├── eslint-config/          # Shared ESLint config
│       │   ├── index.js
│       │   └── package.json
│       └── tsconfig/               # Shared TypeScript configs
│           ├── base.json
│           ├── nextjs.json
│           └── package.json
│
├── scripts/                         # Development and deployment scripts
│   ├── setup.sh                    # Initial setup script
│   ├── dev.sh                      # Start all services in dev mode
│   ├── build.sh                    # Build all applications
│   ├── test.sh                     # Run all tests
│   └── deploy.sh                   # Deployment script
│
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md             # This file
│   ├── API.md                      # API documentation
│   ├── AGENTS.md                   # Agent behavior documentation
│   ├── DEPLOYMENT.md               # Deployment guide
│   └── DEVELOPMENT.md              # Development guide
│
├── config/                         # Root-level configuration
│   ├── .env.example                # Environment variables template
│   ├── docker-compose.yml          # Docker composition (optional)
│   └── nginx.conf                  # Nginx config (if needed)
│
├── .github/                        # GitHub configuration
│   └── workflows/
│       ├── ci.yml                  # CI pipeline
│       └── deploy.yml              # Deployment pipeline
│
├── .gitignore
├── README.md
├── AGENTS.md                       # Agent guidance file
├── package.json                    # Root package.json (workspace config)
├── pnpm-workspace.yaml             # PNPM workspace config
└── turbo.json                      # Turborepo config (optional)
```

## 🎯 Architectural Rationale

### 1. **Monorepo Structure Choice**

**Decision:** Apps-based monorepo with shared packages

**Rationale:**
- **Clear Separation:** [`apps/`](apps/) directory clearly separates deployable applications
- **Code Reuse:** [`packages/`](packages/) enables sharing types and configs between frontend/backend
- **Independent Deployment:** Each app can be deployed independently
- **Scalability:** Easy to add new agents or services without restructuring
- **Hackathon-Friendly:** Simple mental model, easy for team members to navigate

### 2. **Frontend Structure ([`apps/frontend/`](apps/frontend/))**

**Technology:** Next.js 13+ with App Router

**Key Decisions:**
- **App Router:** Modern Next.js structure for better performance and DX
- **Component Organization:** Separated by function (ui, dashboard, charts, animations)
- **API Routes as Proxy:** Next.js API routes proxy to Python backend for security
- **GSAP Integration:** Dedicated [`animations/`](apps/frontend/src/components/animations/) directory for GSAP components
- **Type Safety:** Local types + shared types from [`packages/types/`](packages/types/)

**Benefits:**
- Fast development with Next.js hot reload
- Built-in API routes for backend communication
- Tailwind CSS for rapid styling
- GSAP for smooth, professional animations

### 3. **Backend Structure ([`apps/backend/`](apps/backend/))**

**Technology:** Python with BeeAI framework + FastAPI

**Key Decisions:**

#### **Agent Organization ([`src/agents/`](apps/backend/src/agents/))**
```
agents/
├── base_agent.py          # Abstract base class for all agents
├── monitor/               # Agent A: Weather monitoring & vendor management
├── auditor/               # Agent B: Emissions calculation & fleet prioritization
└── orchestrator/          # Coordinates agent communication
```

**Agent Design Principles:**
- **Modularity:** Each agent is self-contained with its own config
- **Extensibility:** Base agent class makes adding new agents trivial
- **Separation of Concerns:** Each agent has dedicated service modules
- **BeeAI Integration:** Agents use BeeAI framework for AI capabilities
- **Message Bus:** Orchestrator enables inter-agent communication

#### **API Layer ([`src/api/`](apps/backend/src/api/))**
- **FastAPI:** Modern, fast, with automatic OpenAPI docs
- **Route Organization:** Grouped by domain (agents, emissions, vendors, weather)
- **Pydantic Schemas:** Type-safe request/response validation
- **Middleware:** CORS, auth, logging centralized

#### **Services Layer ([`src/services/`](apps/backend/src/services/))**
- **watsonx_service.py:** IBM watsonx.ai Granite-3.0-8b integration
- **openweather_service.py:** OpenWeather API client
- **data_processor.py:** Business logic for data transformation

**Benefits:**
- Clean architecture with clear layers
- Easy to test each component independently
- Scalable for adding more agents
- Type-safe with Pydantic models

### 4. **Shared Packages ([`packages/`](packages/))**

#### **Types Package ([`packages/types/`](packages/types/))**
**Purpose:** Single source of truth for data structures

**Contents:**
- [`agent.types.ts`](packages/types/src/agent.types.ts): Agent status, configuration types
- [`emissions.types.ts`](packages/types/src/emissions.types.ts): Scope 3 emissions data structures
- [`vendor.types.ts`](packages/types/src/vendor.types.ts): Vendor and fleet information
- [`api.types.ts`](packages/types/src/api.types.ts): API request/response types

**Benefits:**
- Frontend and backend share same type definitions
- Reduces bugs from type mismatches
- Single place to update when data structures change

#### **Config Package ([`packages/config/`](packages/config/))**
**Purpose:** Shared linting and TypeScript configurations

**Benefits:**
- Consistent code style across all TypeScript code
- DRY principle for configuration
- Easy to update standards project-wide

### 5. **Configuration Management**

#### **Environment Variables Strategy**

```
config/
└── .env.example          # Template with all required variables

apps/frontend/
└── .env.local            # Frontend-specific variables

apps/backend/
└── .env                  # Backend-specific variables
```

**Key Variables:**
```bash
# Backend (.env)
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project
OPENWEATHER_API_KEY=your_key
DATABASE_URL=postgresql://...
CORS_ORIGINS=http://localhost:3000

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

**Benefits:**
- Clear separation of frontend/backend secrets
- Template file prevents missing variables
- NEXT_PUBLIC_ prefix for client-safe variables

### 6. **Agent Architecture Deep Dive**

#### **Agent A: The Monitor**

**Location:** [`apps/backend/src/agents/monitor/`](apps/backend/src/agents/monitor/)

**Responsibilities:**
1. Poll OpenWeather API for weather data
2. Manage vendor lists and availability
3. Trigger alerts based on weather conditions
4. Communicate with Auditor agent

**Key Files:**
- [`agent.py`](apps/backend/src/agents/monitor/agent.py): Main agent logic using BeeAI
- [`weather_service.py`](apps/backend/src/agents/monitor/weather_service.py): OpenWeather API integration
- [`vendor_manager.py`](apps/backend/src/agents/monitor/vendor_manager.py): Vendor CRUD operations
- [`config.py`](apps/backend/src/agents/monitor/config.py): Agent-specific configuration

**Data Flow:**
```
OpenWeather API → weather_service.py → agent.py → orchestrator → Frontend
                                      ↓
                                vendor_manager.py → Database
```

#### **Agent B: The Auditor**

**Location:** [`apps/backend/src/agents/auditor/`](apps/backend/src/agents/auditor/)

**Responsibilities:**
1. Calculate Scope 3 emissions for supply chain
2. Prioritize hydrogen-fueled fleets
3. Generate sustainability reports
4. Provide recommendations via watsonx.ai

**Key Files:**
- [`agent.py`](apps/backend/src/agents/auditor/agent.py): Main agent logic using BeeAI
- [`emissions_calculator.py`](apps/backend/src/agents/auditor/emissions_calculator.py): Scope 3 calculations
- [`fleet_prioritizer.py`](apps/backend/src/agents/auditor/fleet_prioritizer.py): Fleet ranking logic
- [`config.py`](apps/backend/src/agents/auditor/config.py): Agent-specific configuration

**Data Flow:**
```
Vendor Data → emissions_calculator.py → agent.py → watsonx.ai (Granite-3.0-8b)
                                       ↓
                              fleet_prioritizer.py → Recommendations → Frontend
```

#### **Agent Orchestrator**

**Location:** [`apps/backend/src/agents/orchestrator/`](apps/backend/src/agents/orchestrator/)

**Purpose:** Coordinate communication between agents

**Key Components:**
- [`coordinator.py`](apps/backend/src/agents/orchestrator/coordinator.py): Manages agent lifecycle
- [`message_bus.py`](apps/backend/src/agents/orchestrator/message_bus.py): Inter-agent messaging

**Communication Pattern:**
```
Monitor Agent → Message Bus → Auditor Agent
      ↓                            ↓
  Weather Data              Emissions Analysis
      ↓                            ↓
      └──────→ Orchestrator ←──────┘
                    ↓
              API Layer → Frontend
```

### 7. **API Integration Points**

#### **Frontend → Backend Communication**

**Architecture:** Next.js API Routes as Proxy

```typescript
// apps/frontend/src/app/api/agents/route.ts
export async function GET() {
  const response = await fetch(`${process.env.BACKEND_URL}/api/agents`);
  return Response.json(await response.json());
}
```

**Benefits:**
- Hides backend URL from client
- Enables server-side authentication
- CORS handled automatically
- Can add caching/rate limiting

#### **Backend API Endpoints**

**Base URL:** `http://localhost:8000/api`

**Key Endpoints:**

```python
# Agent Management
GET    /api/agents                    # List all agents and status
GET    /api/agents/{agent_id}         # Get specific agent details
POST   /api/agents/{agent_id}/start   # Start an agent
POST   /api/agents/{agent_id}/stop    # Stop an agent

# Weather Data (Monitor Agent)
GET    /api/weather/current           # Current weather data
GET    /api/weather/forecast          # Weather forecast
GET    /api/weather/alerts            # Weather alerts

# Vendor Management (Monitor Agent)
GET    /api/vendors                   # List all vendors
POST   /api/vendors                   # Add new vendor
PUT    /api/vendors/{vendor_id}       # Update vendor
DELETE /api/vendors/{vendor_id}       # Remove vendor

# Emissions Data (Auditor Agent)
GET    /api/emissions/scope3          # Scope 3 emissions data
GET    /api/emissions/analysis        # Emissions analysis
POST   /api/emissions/calculate       # Calculate emissions for route

# Fleet Management (Auditor Agent)
GET    /api/fleets                    # List all fleets
GET    /api/fleets/prioritized        # Hydrogen-prioritized fleets
GET    /api/fleets/{fleet_id}/score   # Get fleet sustainability score
```

#### **WebSocket Support (Optional for Real-time Updates)**

```python
# apps/backend/src/api/websocket.py
@app.websocket("/ws/agents")
async def agent_updates(websocket: WebSocket):
    # Stream agent status updates to frontend
    pass
```

### 8. **Testing Strategy**

#### **Frontend Tests ([`apps/frontend/tests/`](apps/frontend/tests/))**
```
tests/
├── unit/                  # Component unit tests
│   ├── components/
│   └── hooks/
├── integration/           # API integration tests
└── e2e/                   # End-to-end tests (Playwright)
```

**Tools:** Jest, React Testing Library, Playwright

#### **Backend Tests ([`apps/backend/tests/`](apps/backend/tests/))**
```
tests/
├── unit/                  # Unit tests for services/agents
│   ├── test_agents.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/           # API integration tests
│   ├── test_api_routes.py
│   └── test_agent_communication.py
└── conftest.py            # Pytest fixtures
```

**Tools:** pytest, pytest-asyncio, httpx (for API testing)

### 9. **Development Workflow**

#### **Quick Start Commands**

```bash
# Initial setup
./scripts/setup.sh

# Start all services in development mode
./scripts/dev.sh

# Run tests
./scripts/test.sh

# Build for production
./scripts/build.sh
```

#### **Individual Service Commands**

```bash
# Frontend only
cd apps/frontend
npm run dev              # Start dev server on :3000

# Backend only
cd apps/backend
python -m uvicorn src.api.main:app --reload  # Start API on :8000
```

### 10. **Scalability Considerations**

#### **Adding New Agents**

**Process:**
1. Create new directory in [`apps/backend/src/agents/`](apps/backend/src/agents/)
2. Extend [`base_agent.py`](apps/backend/src/agents/base_agent.py)
3. Register with orchestrator
4. Add API routes if needed
5. Update frontend to display agent status

**Example Structure:**
```python
# apps/backend/src/agents/optimizer/agent.py
from agents.base_agent import BaseAgent

class OptimizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="optimizer")
    
    async def execute(self):
        # Agent logic here
        pass
```

#### **Future Agent Ideas**
- **Route Optimizer:** Optimizes delivery routes based on emissions
- **Demand Forecaster:** Predicts supply chain demand using AI
- **Risk Assessor:** Evaluates supply chain risks
- **Cost Analyzer:** Analyzes cost vs. sustainability tradeoffs

### 11. **Technology Integration Details**

#### **IBM watsonx.ai Integration**

**Location:** [`apps/backend/src/services/watsonx_service.py`](apps/backend/src/services/watsonx_service.py)

```python
from ibm_watsonx_ai import Credentials, APIClient
from ibm_watsonx_ai.foundation_models import ModelInference

class WatsonXService:
    def __init__(self):
        self.credentials = Credentials(
            api_key=os.getenv("WATSONX_API_KEY"),
            url="https://us-south.ml.cloud.ibm.com"
        )
        self.client = APIClient(self.credentials)
        self.model = ModelInference(
            model_id="ibm/granite-3-8b-instruct",
            credentials=self.credentials,
            project_id=os.getenv("WATSONX_PROJECT_ID")
        )
    
    async def generate_recommendations(self, emissions_data):
        prompt = f"Analyze emissions data and provide recommendations: {emissions_data}"
        response = self.model.generate(prompt=prompt)
        return response
```

#### **BeeAI Framework Integration**

**Location:** [`apps/backend/src/agents/base_agent.py`](apps/backend/src/agents/base_agent.py)

```python
from bee_agent import BeeAgent, Tool

class BaseAgent(BeeAgent):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.tools = self._register_tools()
    
    def _register_tools(self) -> list[Tool]:
        # Register tools for the agent
        return []
    
    async def execute(self):
        # Override in subclasses
        raise NotImplementedError
```

#### **GSAP Animation Setup**

**Location:** [`apps/frontend/src/lib/animations.ts`](apps/frontend/src/lib/animations.ts)

```typescript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export const fadeInUp = (element: HTMLElement) => {
  gsap.from(element, {
    y: 50,
    opacity: 0,
    duration: 0.8,
    ease: 'power3.out'
  });
};

export const animateEmissionsChart = (data: number[]) => {
  // Custom GSAP animations for charts
};
```

### 12. **Hackathon-Specific Optimizations**

#### **Rapid Development Priorities**

1. **Use Mock Data Initially**
   - Create [`apps/backend/src/utils/mock_data.py`](apps/backend/src/utils/mock_data.py)
   - Allows frontend development without waiting for API integrations

2. **Parallel Development**
   - Frontend team: Work on UI with mock data
   - Backend team: Implement agents and API
   - Integration: Last 12 hours

3. **Pre-built Components**
   - Use shadcn/ui for rapid UI development
   - Tailwind CSS for quick styling
   - Chart.js or Recharts for data visualization

4. **Simplified Authentication**
   - Skip complex auth for hackathon
   - Use simple API key if needed

5. **Docker Compose for Easy Setup**
   ```yaml
   # config/docker-compose.yml
   services:
     frontend:
       build: ./apps/frontend
       ports:
         - "3000:3000"
     backend:
       build: ./apps/backend
       ports:
         - "8000:8000"
       environment:
         - WATSONX_API_KEY=${WATSONX_API_KEY}
   ```

### 13. **Documentation Strategy**

#### **Essential Documentation Files**

1. **[`docs/API.md`](docs/API.md)**: Complete API documentation with examples
2. **[`docs/AGENTS.md`](docs/AGENTS.md)**: Agent behavior and communication patterns
3. **[`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)**: Setup and development guide
4. **[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)**: Deployment instructions

#### **Code Documentation**

- **Python:** Docstrings for all classes and functions
- **TypeScript:** JSDoc comments for complex functions
- **README.md:** In each major directory explaining its purpose

## 🚀 Implementation Timeline (48 Hours)

### **Hour 0-4: Setup & Foundation**
- [ ] Initialize monorepo structure
- [ ] Set up Next.js frontend
- [ ] Set up Python backend with FastAPI
- [ ] Configure shared types package
- [ ] Set up development scripts

### **Hour 4-12: Core Agent Development**
- [ ] Implement Monitor Agent (Agent A)
- [ ] Implement Auditor Agent (Agent B)
- [ ] Set up agent orchestrator
- [ ] Integrate OpenWeather API
- [ ] Integrate IBM watsonx.ai

### **Hour 12-24: API & Integration**
- [ ] Build FastAPI endpoints
- [ ] Implement frontend API client
- [ ] Connect agents to API
- [ ] Test agent communication
- [ ] Set up WebSocket for real-time updates

### **Hour 24-36: Frontend Development**
- [ ] Build dashboard UI
- [ ] Implement data visualization
- [ ] Add GSAP animations
- [ ] Connect to backend API
- [ ] Responsive design with Tailwind

### **Hour 36-44: Testing & Polish**
- [ ] Integration testing
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] Documentation
- [ ] Demo preparation

### **Hour 44-48: Final Touches**
- [ ] Final testing
- [ ] Deployment
- [ ] Demo rehearsal
- [ ] Presentation materials

## 📊 Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend - Next.js"
        UI[User Interface]
        API_ROUTES[API Routes Proxy]
        COMPONENTS[React Components]
        GSAP[GSAP Animations]
    end

    subgraph "Backend - Python"
        FASTAPI[FastAPI Server]
        
        subgraph "Agents"
            MONITOR[Monitor Agent<br/>Weather & Vendors]
            AUDITOR[Auditor Agent<br/>Emissions & Fleets]
            ORCH[Orchestrator]
        end
        
        subgraph "Services"
            WATSONX[watsonx.ai Service<br/>Granite-3.0-8b]
            WEATHER_SVC[OpenWeather Service]
            DATA_PROC[Data Processor]
        end
    end

    subgraph "External APIs"
        OPENWEATHER[OpenWeather API]
        IBM_WATSONX[IBM watsonx.ai]
    end

    subgraph "Shared"
        TYPES[Shared Types Package]
    end

    UI --> API_ROUTES
    API_ROUTES --> FASTAPI
    COMPONENTS --> GSAP
    COMPONENTS --> TYPES
    
    FASTAPI --> MONITOR
    FASTAPI --> AUDITOR
    MONITOR --> ORCH
    AUDITOR --> ORCH
    
    MONITOR --> WEATHER_SVC
    AUDITOR --> WATSONX
    AUDITOR --> DATA_PROC
    
    WEATHER_SVC --> OPENWEATHER
    WATSONX --> IBM_WATSONX
    
    FASTAPI --> TYPES
```

## 🎯 Key Benefits of This Architecture

1. **Clear Separation of Concerns**
   - Frontend and backend are completely independent
   - Agents are modular and self-contained
   - Easy to understand and navigate

2. **Scalability**
   - Adding new agents is straightforward
   - Can scale frontend and backend independently
   - Shared types prevent integration issues

3. **Developer Experience**
   - Fast hot reload in development
   - Clear directory structure
   - Comprehensive documentation

4. **Hackathon-Optimized**
   - Parallel development possible
   - Mock data support for rapid iteration
   - Simple deployment with Docker

5. **Production-Ready Foundation**
   - Clean architecture for future expansion
   - Proper testing structure
   - Environment configuration management

## 📝 Next Steps

1. Review this architecture plan
2. Confirm tech stack choices
3. Set up initial monorepo structure
4. Begin parallel development on frontend and backend
5. Regular integration checkpoints

---

**Questions or Concerns?**
This architecture is designed to be flexible. If you need to adjust any part based on team expertise or time constraints, the modular structure makes it easy to adapt.
</content>
<line_count>717</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'docs/ARCHITECTURE.md'] Result:
<file_write_result>
<path>docs/ARCHITECTURE.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
docs\ARCHITECTURE.md

# VSCode Open Tabs
.gitignore,README.md,AGENTS.md,docs/ARCHITECTURE.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T06:44:49.812Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.11

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze project requirements and tech stack constraints | In Progress |
| 2 | Design the complete monorepo directory structure | Pending |
| 3 | Document the rationale for architectural decisions | Pending |
| 4 | Create detailed explanations for each major directory | Pending |
| 5 | Define agent organization strategy | Pending |
| 6 | Plan shared resources and configuration management | Pending |
| 7 | Document API integration points | Pending |
| 8 | Create visual architecture diagram | Pending |
| 9 | Provide implementation guidelines for hackathon context | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Analyze project requirements and tech stack constraints
[x] Design the complete monorepo directory structure
[x] Document the rationale for architectural decisions
[x] Create detailed explanations for each major directory
[x] Define agent organization strategy
[x] Plan shared resources and configuration management
[x] Document API integration points
[x] Create visual architecture diagram
[x] Provide implementation guidelines for hackathon context
[-] Create quick reference guide for team
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
docs\ARCHITECTURE.md

# VSCode Open Tabs
.gitignore,README.md,AGENTS.md,docs/ARCHITECTURE.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T06:44:54.137Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.17

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze project requirements and tech stack constraints | Completed |
| 2 | Design the complete monorepo directory structure | Completed |
| 3 | Document the rationale for architectural decisions | Completed |
| 4 | Create detailed explanations for each major directory | Completed |
| 5 | Define agent organization strategy | Completed |
| 6 | Plan shared resources and configuration management | Completed |
| 7 | Document API integration points | Completed |
| 8 | Create visual architecture diagram | Completed |
| 9 | Provide implementation guidelines for hackathon context | Completed |
| 10 | Create quick reference guide for team | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<write_to_file>
<path>docs/QUICK_START.md</path>
<content># Eco-Shift Quick Start Guide

## 🚀 30-Second Overview

**Eco-Shift** is a multi-agent supply chain orchestrator with:
- **Frontend:** Next.js + Tailwind CSS + GSAP (Port 3000)
- **Backend:** Python + BeeAI + FastAPI (Port 8000)
- **AI:** IBM watsonx.ai Granite-3.0-8b
- **Agents:** Monitor (weather/vendors) + Auditor (emissions/fleets)

## 📁 Key Directories

```
eco-shift/
├── apps/
│   ├── frontend/          # Next.js app → localhost:3000
│   └── backend/           # Python API → localhost:8000
│       └── src/agents/    # Agent A (monitor) & Agent B (auditor)
├── packages/
│   └── types/             # Shared TypeScript types
├── docs/                  # Full documentation
└── scripts/               # Development scripts
```

## ⚡ Quick Commands

```bash
# Setup (first time only)
./scripts/setup.sh

# Start everything
./scripts/dev.sh

# Frontend only
cd apps/frontend && npm run dev

# Backend only
cd apps/backend && python -m uvicorn src.api.main:app --reload

# Run tests
./scripts/test.sh
```

## 🤖 Agent Locations

### Agent A: The Monitor
**Path:** [`apps/backend/src/agents/monitor/`](../apps/backend/src/agents/monitor/)
- Polls OpenWeather API
- Manages vendor lists
- Files: `agent.py`, `weather_service.py`, `vendor_manager.py`

### Agent B: The Auditor
**Path:** [`apps/backend/src/agents/auditor/`](../apps/backend/src/agents/auditor/)
- Calculates Scope 3 emissions
- Prioritizes hydrogen fleets
- Files: `agent.py`, `emissions_calculator.py`, `fleet_prioritizer.py`

## 🔌 API Endpoints

**Base URL:** `http://localhost:8000/api`

```
GET  /api/agents              # List all agents
GET  /api/weather/current     # Current weather
GET  /api/vendors             # List vendors
GET  /api/emissions/scope3    # Emissions data
GET  /api/fleets/prioritized  # Hydrogen-prioritized fleets
```

## 🎨 Frontend Structure

```
apps/frontend/src/
├── app/                   # Next.js pages
│   ├── api/              # API proxy routes
│   └── dashboard/        # Dashboard pages
├── components/
│   ├── ui/               # Reusable components
│   ├── charts/           # Data visualizations
│   └── animations/       # GSAP animations
└── lib/
    └── api-client.ts     # Backend API client
```

## 🐍 Backend Structure

```
apps/backend/src/
├── agents/               # BeeAI agents
│   ├── monitor/         # Agent A
│   ├── auditor/         # Agent B
│   └── orchestrator/    # Agent coordinator
├── api/                 # FastAPI routes
│   └── routes/          # Endpoint definitions
├── services/            # Business logic
│   ├── watsonx_service.py
│   └── openweather_service.py
└── models/              # Data models
```

## 🔑 Environment Variables

Create these files:

**`apps/backend/.env`**
```bash
WATSONX_API_KEY=your_key_here
WATSONX_PROJECT_ID=your_project_id
OPENWEATHER_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:3000
```

**`apps/frontend/.env.local`**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📦 Adding a New Agent

1. Create directory: `apps/backend/src/agents/your_agent/`
2. Create files:
   ```python
   # agent.py
   from agents.base_agent import BaseAgent
   
   class YourAgent(BaseAgent):
       def __init__(self):
           super().__init__(name="your_agent")
       
       async def execute(self):
           # Your logic here
           pass
   ```
3. Register in orchestrator
4. Add API routes if needed
5. Update frontend

## 🧪 Testing

```bash
# All tests
./scripts/test.sh

# Frontend only
cd apps/frontend && npm test

# Backend only
cd apps/backend && pytest
```

## 📚 Full Documentation

- **Architecture:** [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) - Complete system design
- **API Docs:** [`docs/API.md`](API.md) - All endpoints (to be created)
- **Agents:** [`docs/AGENTS.md`](AGENTS.md) - Agent behavior details
- **Development:** [`docs/DEVELOPMENT.md`](DEVELOPMENT.md) - Setup guide (to be created)

## 🎯 Hackathon Workflow

### Hour 0-4: Setup
- [ ] Run `./scripts/setup.sh`
- [ ] Verify both servers start
- [ ] Test API connection

### Hour 4-12: Backend
- [ ] Implement Monitor agent
- [ ] Implement Auditor agent
- [ ] Connect to OpenWeather API
- [ ] Integrate watsonx.ai

### Hour 12-24: Integration
- [ ] Build API endpoints
- [ ] Test agent communication
- [ ] Create mock data

### Hour 24-36: Frontend
- [ ] Build dashboard UI
- [ ] Add data visualizations
- [ ] Implement GSAP animations
- [ ] Connect to backend

### Hour 36-48: Polish
- [ ] Integration testing
- [ ] Bug fixes
- [ ] Demo preparation

## 🆘 Common Issues

**Port already in use:**
```bash
# Kill process on port 3000
npx kill-port 3000

# Kill process on port 8000
npx kill-port 8000
```

**Python dependencies:**
```bash
cd apps/backend
pip install -r requirements.txt
```

**Node modules:**
```bash
cd apps/frontend
npm install
```

**CORS errors:**
- Check `CORS_ORIGINS` in backend `.env`
- Verify frontend URL matches

## 💡 Pro Tips

1. **Use Mock Data First:** Develop frontend with mock data while backend is being built
2. **Parallel Development:** Frontend and backend teams work independently
3. **Test Early:** Test agent communication as soon as both agents are implemented
4. **Keep It Simple:** Skip complex auth for hackathon, focus on core features
5. **Document As You Go:** Update docs when you make architectural decisions

## 🔗 Useful Links

- **Next.js Docs:** https://nextjs.org/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **BeeAI Framework:** [Add link when available]
- **IBM watsonx.ai:** https://www.ibm.com/watsonx
- **OpenWeather API:** https://openweathermap.org/api

## 📞 Need Help?

1. Check [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) for detailed explanations
2. Review code comments in base files
3. Ask team members familiar with specific components

---

**Ready to build?** Start with `./scripts/setup.sh` and follow the hackathon workflow above!
</content>
<line_count>247</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'docs/QUICK_START.md'] Result:
<file_write_result>
<path>docs/QUICK_START.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
docs\QUICK_START.md

# VSCode Open Tabs
.gitignore,README.md,AGENTS.md,docs/ARCHITECTURE.md,docs/QUICK_START.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T06:45:24.637Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.23

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze project requirements and tech stack constraints | Completed |
| 2 | Design the complete monorepo directory structure | Completed |
| 3 | Document the rationale for architectural decisions | Completed |
| 4 | Create detailed explanations for each major directory | Completed |
| 5 | Define agent organization strategy | Completed |
| 6 | Plan shared resources and configuration management | Completed |
| 7 | Document API integration points | Completed |
| 8 | Create visual architecture diagram | Completed |
| 9 | Provide implementation guidelines for hackathon context | Completed |
| 10 | Create quick reference guide for team | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Analyze project requirements and tech stack constraints
[x] Design the complete monorepo directory structure
[x] Document the rationale for architectural decisions
[x] Create detailed explanations for each major directory
[x] Define agent organization strategy
[x] Plan shared resources and configuration management
[x] Document API integration points
[x] Create visual architecture diagram
[x] Provide implementation guidelines for hackathon context
[x] Create quick reference guide for team
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
docs\QUICK_START.md

# VSCode Open Tabs
.gitignore,README.md,AGENTS.md,docs/ARCHITECTURE.md,docs/QUICK_START.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T06:45:28.701Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.29

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze project requirements and tech stack constraints | Completed |
| 2 | Design the complete monorepo directory structure | Completed |
| 3 | Document the rationale for architectural decisions | Completed |
| 4 | Create detailed explanations for each major directory | Completed |
| 5 | Define agent organization strategy | Completed |
| 6 | Plan shared resources and configuration management | Completed |
| 7 | Document API integration points | Completed |
| 8 | Create visual architecture diagram | Completed |
| 9 | Provide implementation guidelines for hackathon context | Completed |
| 10 | Create quick reference guide for team | Completed |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
I've designed a comprehensive monorepo architecture for **Eco-Shift**, your multi-agent supply chain orchestrator. Here's what I've created:

## 📋 Deliverables

### 1. **Complete Architecture Documentation** ([`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md))
A 717-line comprehensive guide covering:

**Directory Structure:**
- **Apps-based monorepo** with clear separation between [`apps/frontend/`](apps/frontend/) (Next.js) and [`apps/backend/`](apps/backend/) (Python)
- **Shared packages** in [`packages/types/`](packages/types/) for type safety across the stack
- **Agent organization** with dedicated directories for Monitor and Auditor agents
- **Scalable structure** ready for adding more agents in the future

**Key Architectural Decisions:**

**Agent Organization** ([`apps/backend/src/agents/`](apps/backend/src/agents/)):
- **Agent A (Monitor):** [`monitor/`](apps/backend/src/agents/monitor/) - Weather polling + vendor management
- **Agent B (Auditor):** [`auditor/`](apps/backend/src/agents/auditor/) - Emissions calculation + fleet prioritization
- **Orchestrator:** [`orchestrator/`](apps/backend/src/agents/orchestrator/) - Inter-agent communication via message bus
- **Base Agent Class:** Extensible foundation for adding new agents

**API Integration:**
- FastAPI backend with organized routes by domain
- Next.js API routes as proxy for security
- 15+ documented endpoints for agents, weather, vendors, emissions, and fleets
- Optional WebSocket support for real-time updates

**Configuration Management:**
- Environment-specific `.env` files
- Shared configuration packages
- Clear separation of frontend/backend secrets

**Tech Stack Integration:**
- IBM watsonx.ai Granite-3.0-8b service layer
- BeeAI framework for agent implementation
- OpenWeather API integration
- GSAP animation utilities

### 2. **Quick Start Guide** ([`docs/QUICK_START.md`](docs/QUICK_START.md))
A concise 247-line reference with:
- 30-second overview
- Key directory locations
- Quick commands for development
- Agent file locations
- API endpoint reference
- Environment variable setup
- 48-hour hackathon workflow
- Common troubleshooting tips

## 🎯 Key Benefits

1. **Hackathon-Optimized:**
   - Parallel development possible (frontend/backend teams work independently)
   - Mock data support for rapid iteration
   - Simple deployment with Docker Compose
   - Clear 48-hour implementation timeline

2. **Clean Architecture:**
   - Modular agent design (easy to add Agent C, D, E...)
   - Shared types prevent integration bugs
   - Clear separation of concerns
   - Production-ready foundation

3. **Developer Experience:**
   - Intuitive directory structure
   - Comprehensive documentation
   - Development scripts for common tasks
   - Type safety across the stack

4. **Scalability:**
   - Adding new agents takes ~30 minutes
   - Independent deployment of frontend/backend
   - Message bus enables complex agent interactions
   - Extensible base agent class

## 📊 Architecture Highlights

**Monorepo Structure:**
```
eco-shift/
├── apps/
│   ├── frontend/          # Next.js + Tailwind + GSAP
│   └── backend/           # Python + BeeAI + FastAPI
│       └── src/agents/    # Monitor, Auditor, Orchestrator
├── packages/
│   └── types/             # Shared TypeScript types
├── scripts/               # Dev/build/test scripts
└── docs/                  # Complete documentation
```

**Agent Communication Flow:**
```
Monitor Agent → Message Bus → Auditor Agent
      ↓                            ↓
  Weather Data              Emissions Analysis
      ↓                            ↓
      └──────→ Orchestrator ←──────┘
                    ↓
              API Layer → Frontend
```

## 🚀 Next Steps

1. **Review** the architecture plan in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
2. **Use** [`docs/QUICK_START.md`](docs/QUICK_START.md) as your team reference
3. **Switch to Code mode** to implement the structure
4. **Follow** the 48-hour timeline for optimal results

The architecture is designed for rapid development while maintaining clean code organization. All components are modular and can be developed in parallel, perfect for a hackathon environment.
</result>
</attempt_completion>

