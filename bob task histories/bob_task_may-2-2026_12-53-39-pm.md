**User:**

<task>
Update the AGENTS.md file with comprehensive project-specific information for the Eco-Shift project.

**Task: Update AGENTS.md with non-obvious, project-specific details**

Read the current [`AGENTS.md`](AGENTS.md:1) file and replace it with detailed, non-obvious information that AI assistants need to know about this codebase.

**Include the following sections:**

1. **Project Overview**
   - Brief description of Eco-Shift
   - Multi-agent architecture explanation
   - Key technologies and their specific versions

2. **Build, Test, and Lint Commands**
   - Frontend commands (from [`apps/frontend/package.json`](apps/frontend/package.json:1))
   - Backend commands (from [`apps/backend/pyproject.toml`](apps/backend/pyproject.toml:1))
   - Root-level commands (from [`package.json`](package.json:1))
   - Docker commands
   - Agent-specific commands

3. **Code Style Guidelines**
   - TypeScript/React conventions for frontend
   - Python conventions for backend
   - Import ordering rules
   - Naming conventions
   - File organization patterns

4. **Architecture-Specific Rules** (NON-OBVIOUS ONLY)
   - Agent communication patterns via message bus
   - How Monitor and Auditor agents interact
   - Orchestrator workflow patterns
   - API integration between frontend and backend
   - Environment variable requirements
   - Critical configuration dependencies

5. **Agent System Details** (NON-OBVIOUS)
   - Agent lifecycle management
   - Message bus usage patterns
   - How to add new agents
   - Agent configuration patterns
   - Error handling in agent workflows

6. **Development Workflow**
   - How to start the full stack
   - How to test individual agents
   - How to debug agent communication
   - Common development tasks

7. **Critical Gotchas** (NON-OBVIOUS)
   - Hydrogen fleet prioritization (10x multiplier in scoring)
   - Emissions calculation specifics
   - Weather polling intervals and caching
   - API rate limiting considerations
   - watsonx.ai integration requirements

**Important Guidelines:**
- Follow the "non-obvious only" principle from the init command
- Remove any obvious information that could be guessed
- Focus on project-specific patterns discovered by reading the code
- Include file paths for custom utilities
- Document counterintuitive design decisions
- Keep it concise but comprehensive

After updating AGENTS.md, use attempt_completion to summarize the changes.
</task>
<environment_details>
# VSCode Visible Files
README.md

# VSCode Open Tabs
.gitignore,AGENTS.md,docs/ARCHITECTURE.md,docs/QUICK_START.md,apps/frontend/package.json,apps/frontend/tsconfig.json,apps/frontend/tailwind.config.ts,apps/frontend/next.config.js,apps/frontend/.eslintrc.json,apps/frontend/postcss.config.js,apps/frontend/src/styles/globals.css,apps/frontend/src/app/layout.tsx,apps/frontend/src/app/page.tsx,apps/frontend/src/lib/api.ts,apps/frontend/.env.example,apps/frontend/README.md,apps/frontend/src/lib/utils.ts,apps/frontend/src/lib/animations.ts,apps/frontend/.gitignore,apps/frontend/.prettierrc

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T07:21:43.991Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (c:/Users/super/OneDrive/Desktop/ibm bob hackathon) Files
.dockerignore
.env.example
.gitignore
AGENTS.md
docker-compose.yml
package.json
README.md
apps/
apps/backend/
apps/backend/.env.example
apps/backend/.flake8
apps/backend/.gitignore
apps/backend/Dockerfile
apps/backend/pyproject.toml
apps/backend/pytest.ini
apps/backend/README.md
apps/backend/requirements.txt
apps/backend/src/
apps/backend/src/__init__.py
apps/backend/src/main.py
apps/backend/src/agents/
apps/backend/src/agents/__init__.py
apps/backend/src/agents/base_agent.py
apps/backend/src/agents/auditor/
apps/backend/src/agents/auditor/__init__.py
apps/backend/src/agents/auditor/auditor_agent.py
apps/backend/src/agents/auditor/config.py
apps/backend/src/agents/auditor/emissions_calculator.py
apps/backend/src/agents/auditor/fleet_prioritizer.py
apps/backend/src/agents/auditor/README.md
apps/backend/src/agents/auditor/route_optimizer.py
apps/backend/src/agents/monitor/
apps/backend/src/agents/monitor/__init__.py
apps/backend/src/agents/monitor/config.py
apps/backend/src/agents/monitor/monitor_agent.py
apps/backend/src/agents/monitor/README.md
apps/backend/src/agents/monitor/vendors.py
apps/backend/src/agents/monitor/weather_monitor.py
apps/backend/src/agents/orchestrator/
apps/backend/src/agents/orchestrator/__init__.py
apps/backend/src/agents/orchestrator/config.py
apps/backend/src/agents/orchestrator/message_bus.py
apps/backend/src/agents/orchestrator/orchestrator_agent.py
apps/backend/src/agents/orchestrator/README.md
apps/backend/src/api/
apps/backend/src/api/__init__.py
apps/backend/src/api/agents.py
apps/backend/src/api/emissions.py
apps/backend/src/api/vendors.py
apps/backend/src/api/weather.py
apps/backend/src/config/
apps/backend/src/config/__init__.py
apps/backend/src/config/settings.py
apps/backend/src/models/
apps/backend/src/models/__init__.py
apps/backend/src/models/schemas.py
apps/backend/src/services/
apps/backend/src/services/__init__.py
apps/backend/src/services/watsonx_service.py
apps/backend/src/services/weather_service.py
apps/backend/src/utils/
apps/backend/src/utils/__init__.py
apps/backend/src/utils/logger.py
apps/backend/tests/
apps/backend/tests/__init__.py
apps/frontend/
apps/frontend/.env.example
apps/frontend/.eslintrc.json
apps/frontend/.gitignore
apps/frontend/.prettierrc
apps/frontend/next.config.js
apps/frontend/package.json
apps/frontend/postcss.config.js
apps/frontend/README.md
apps/frontend/tailwind.config.ts
apps/frontend/tsconfig.json
apps/frontend/public/
apps/frontend/src/
apps/frontend/src/app/
apps/frontend/src/app/layout.tsx
apps/frontend/src/app/page.tsx
apps/frontend/src/components/
apps/frontend/src/components/animations/
apps/frontend/src/components/charts/
apps/frontend/src/components/dashboard/
apps/frontend/src/components/ui/
apps/frontend/src/components/ui/README.md
apps/frontend/src/hooks/
apps/frontend/src/hooks/useAgents.ts
apps/frontend/src/lib/
apps/frontend/src/lib/animations.ts
apps/frontend/src/lib/api.ts
apps/frontend/src/lib/utils.ts
apps/frontend/src/styles/
apps/frontend/src/styles/globals.css
apps/frontend/src/types/
apps/frontend/src/types/index.ts
apps/frontend/tests/
docs/
docs/ARCHITECTURE.md
docs/QUICK_START.md
packages/
packages/types/
packages/types/index.ts
packages/types/package.json
scripts/
scripts/dev.ps1
scripts/setup.ps1
scripts/test.ps1
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll read the necessary files to gather comprehensive information about the Eco-Shift project, then update the AGENTS.md file with non-obvious, project-specific details.

<read_file>
<args>
<file>
<path>AGENTS.md</path>
</file>
<file>
<path>README.md</path>
</file>
<file>
<path>docs/ARCHITECTURE.md</path>
</file>
<file>
<path>package.json</path>
</file>
<file>
<path>apps/frontend/package.json</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
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
<file><path>README.md</path>
<content lines="1-531">
  1 | # 🌱 Eco-Shift
  2 | 
  3 | **AI-Powered Logistics Optimization for Sustainable Supply Chain Management**
  4 | 
  5 | Eco-Shift is an intelligent platform that leverages IBM watsonx.ai and real-time weather data to optimize logistics operations, reduce carbon emissions, and promote sustainable supply chain practices.
  6 | 
  7 | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  8 | [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  9 | [![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
 10 | 
 11 | ---
 12 | 
 13 | ## 📋 Table of Contents
 14 | 
 15 | - [Overview](#overview)
 16 | - [Features](#features)
 17 | - [Architecture](#architecture)
 18 | - [Tech Stack](#tech-stack)
 19 | - [Getting Started](#getting-started)
 20 | - [Project Structure](#project-structure)
 21 | - [Agent System](#agent-system)
 22 | - [Development](#development)
 23 | - [Deployment](#deployment)
 24 | - [API Documentation](#api-documentation)
 25 | - [Contributing](#contributing)
 26 | - [License](#license)
 27 | 
 28 | ---
 29 | 
 30 | ## 🎯 Overview
 31 | 
 32 | Eco-Shift addresses the critical challenge of reducing carbon emissions in logistics operations by:
 33 | 
 34 | 1. **Real-time Weather Monitoring**: Tracks weather conditions across vendor locations
 35 | 2. **Intelligent Route Optimization**: Optimizes delivery routes based on weather and emissions
 36 | 3. **Fleet Prioritization**: Recommends the most efficient vehicles for each route
 37 | 4. **Emissions Tracking**: Calculates and monitors carbon footprint in real-time
 38 | 5. **AI-Powered Insights**: Uses IBM watsonx.ai for intelligent decision-making
 39 | 
 40 | ---
 41 | 
 42 | ## ✨ Features
 43 | 
 44 | ### 🤖 Multi-Agent System
 45 | - **Monitor Agent**: Continuously monitors weather conditions and vendor locations
 46 | - **Auditor Agent**: Analyzes emissions, optimizes routes, and prioritizes fleet
 47 | - **Orchestrator Agent**: Coordinates workflow between agents
 48 | 
 49 | ### 🌦️ Weather Intelligence
 50 | - Real-time weather data from OpenWeather API
 51 | - Weather alerts for severe conditions
 52 | - Impact analysis on logistics operations
 53 | - Proactive route adjustments
 54 | 
 55 | ### 📊 Emissions Management
 56 | - Real-time emissions calculation
 57 | - Fuel type comparison (diesel, petrol, electric, hybrid)
 58 | - Carbon footprint tracking
 59 | - Reduction recommendations
 60 | 
 61 | ### 🚛 Fleet Optimization
 62 | - Vehicle prioritization based on efficiency
 63 | - Route optimization for minimal emissions
 64 | - Load balancing across fleet
 65 | - Maintenance scheduling integration
 66 | 
 67 | ### 📈 Analytics Dashboard
 68 | - Real-time metrics and KPIs
 69 | - Interactive charts and visualizations
 70 | - Historical data analysis
 71 | - Export capabilities
 72 | 
 73 | ---
 74 | 
 75 | ## 🏗️ Architecture
 76 | 
 77 | ```
 78 | ┌─────────────────────────────────────────────────────────────────────┐
 79 | │                         ECO-SHIFT PLATFORM                          │
 80 | ├─────────────────────────────────────────────────────────────────────┤
 81 | │                                                                     │
 82 | │  ┌─────────────────────────────────────────────────────────────┐  │
 83 | │  │                    Frontend (Next.js)                        │  │
 84 | │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
 85 | │  │  │  Dashboard   │  │   Analytics  │  │   Settings   │      │  │
 86 | │  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
 87 | │  └─────────────────────────────────────────────────────────────┘  │
 88 | │                              │                                      │
 89 | │                              │ REST API                             │
 90 | │                              ▼                                      │
 91 | │  ┌─────────────────────────────────────────────────────────────┐  │
 92 | │  │                   Backend (FastAPI)                          │  │
 93 | │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
 94 | │  │  │  API Routes  │  │   Services   │  │    Models    │      │  │
 95 | │  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
 96 | │  └─────────────────────────────────────────────────────────────┘  │
 97 | │                              │                                      │
 98 | │                              │                                      │
 99 | │  ┌─────────────────────────────────────────────────────────────┐  │
100 | │  │                  Orchestrator Agent                          │  │
101 | │  │                                                              │  │
102 | │  │  ┌──────────────────────────────────────────────────────┐  │  │
103 | │  │  │              Message Bus (Pub/Sub)                    │  │  │
104 | │  │  └──────────────────────────────────────────────────────┘  │  │
105 | │  │                                                              │  │
106 | │  │  ┌──────────────┐                    ┌──────────────┐      │  │
107 | │  │  │   Monitor    │◄──────────────────►│   Auditor    │      │  │
108 | │  │  │    Agent     │                    │    Agent     │      │  │
109 | │  │  └──────────────┘                    └──────────────┘      │  │
110 | │  │         │                                     │             │  │
111 | │  └─────────┼─────────────────────────────────────┼─────────────┘  │
112 | │            │                                     │                 │
113 | │            ▼                                     ▼                 │
114 | │  ┌──────────────────┐              ┌──────────────────┐          │
115 | │  │  OpenWeather API │              │  IBM watsonx.ai  │          │
116 | │  └──────────────────┘              └──────────────────┘          │
117 | │                                                                     │
118 | └─────────────────────────────────────────────────────────────────────┘
119 | ```
120 | 
121 | ### Data Flow
122 | 
123 | 1. **Weather Monitoring**: Monitor Agent fetches weather data from OpenWeather API
124 | 2. **Alert Generation**: Severe weather conditions trigger alerts
125 | 3. **Audit Trigger**: Orchestrator receives alerts and triggers Auditor Agent
126 | 4. **Analysis**: Auditor calculates emissions and optimizes routes using watsonx.ai
127 | 5. **Results**: Optimized recommendations sent to frontend dashboard
128 | 6. **Action**: Users review and implement recommendations
129 | 
130 | ---
131 | 
132 | ## 🛠️ Tech Stack
133 | 
134 | ### Frontend
135 | - **Framework**: Next.js 14 (React 18)
136 | - **Language**: TypeScript
137 | - **Styling**: Tailwind CSS
138 | - **UI Components**: shadcn/ui
139 | - **State Management**: React Hooks
140 | - **Charts**: Recharts
141 | - **HTTP Client**: Axios
142 | 
143 | ### Backend
144 | - **Framework**: FastAPI
145 | - **Language**: Python 3.11+
146 | - **Async**: asyncio, aiohttp
147 | - **Validation**: Pydantic
148 | - **Testing**: pytest
149 | - **Code Quality**: Black, Flake8
150 | 
151 | ### AI & Data
152 | - **AI Platform**: IBM watsonx.ai
153 | - **Weather API**: OpenWeather
154 | - **Agent Framework**: Custom multi-agent system
155 | - **Message Bus**: Custom pub/sub implementation
156 | 
157 | ### Infrastructure
158 | - **Containerization**: Docker, Docker Compose
159 | - **Database**: PostgreSQL (optional)
160 | - **Caching**: Redis (optional)
161 | - **Monitoring**: Built-in logging and metrics
162 | 
163 | ---
164 | 
165 | ## 🚀 Getting Started
166 | 
167 | ### Prerequisites
168 | 
169 | - **Node.js** 18+ and npm
170 | - **Python** 3.11+
171 | - **Git**
172 | - **IBM watsonx.ai** account and API key
173 | - **OpenWeather** API key
174 | 
175 | ### Quick Start
176 | 
177 | #### 1. Clone the Repository
178 | 
179 | ```bash
180 | git clone https://github.com/yourusername/eco-shift.git
181 | cd eco-shift
182 | ```
183 | 
184 | #### 2. Run Setup Script
185 | 
186 | **Windows (PowerShell):**
187 | ```powershell
188 | .\scripts\setup.ps1
189 | ```
190 | 
191 | **Linux/Mac:**
192 | ```bash
193 | chmod +x scripts/setup.sh
194 | ./scripts/setup.sh
195 | ```
196 | 
197 | #### 3. Configure Environment Variables
198 | 
199 | Edit `.env` file with your API keys:
200 | 
201 | ```bash
202 | # IBM watsonx.ai
203 | WATSONX_API_KEY=your_api_key_here
204 | WATSONX_PROJECT_ID=your_project_id_here
205 | 
206 | # OpenWeather
207 | OPENWEATHER_API_KEY=your_api_key_here
208 | ```
209 | 
210 | #### 4. Start Development Servers
211 | 
212 | **Windows (PowerShell):**
213 | ```powershell
214 | .\scripts\dev.ps1
215 | ```
216 | 
217 | **Linux/Mac:**
218 | ```bash
219 | ./scripts/dev.sh
220 | ```
221 | 
222 | **Or use npm:**
223 | ```bash
224 | npm run dev
225 | ```
226 | 
227 | #### 5. Access the Application
228 | 
229 | - **Frontend**: http://localhost:3000
230 | - **Backend API**: http://localhost:8000
231 | - **API Documentation**: http://localhost:8000/docs
232 | 
233 | ### Using Docker
234 | 
235 | ```bash
236 | # Build and start all services
237 | docker-compose up -d
238 | 
239 | # View logs
240 | docker-compose logs -f
241 | 
242 | # Stop services
243 | docker-compose down
244 | ```
245 | 
246 | ---
247 | 
248 | ## 📁 Project Structure
249 | 
250 | ```
251 | eco-shift/
252 | ├── apps/
253 | │   ├── frontend/              # Next.js frontend application
254 | │   │   ├── src/
255 | │   │   │   ├── app/          # Next.js app directory
256 | │   │   │   ├── components/   # React components
257 | │   │   │   ├── lib/          # Utilities and API client
258 | │   │   │   ├── styles/       # Global styles
259 | │   │   │   └── types/        # TypeScript types
260 | │   │   ├── public/           # Static assets
261 | │   │   └── package.json
262 | │   │
263 | │   └── backend/              # FastAPI backend application
264 | │       ├── src/
265 | │       │   ├── agents/       # Agent system
266 | │       │   │   ├── monitor/  # Weather monitoring agent
267 | │       │   │   ├── auditor/  # Emissions auditing agent
268 | │       │   │   └── orchestrator/ # Agent coordinator
269 | │       │   ├── api/          # API routes
270 | │       │   ├── config/       # Configuration
271 | │       │   ├── models/       # Data models
272 | │       │   ├── services/     # Business logic
273 | │       │   └── utils/        # Utilities
274 | │       ├── tests/            # Test suite
275 | │       └── requirements.txt
276 | │
277 | ├── packages/
278 | │   └── types/                # Shared TypeScript types
279 | │
280 | ├── scripts/                  # Development scripts
281 | │   ├── dev.ps1              # Start dev servers (Windows)
282 | │   ├── setup.ps1            # Setup script (Windows)
283 | │   └── test.ps1             # Run tests (Windows)
284 | │
285 | ├── docs/                     # Documentation
286 | │   ├── ARCHITECTURE.md      # Architecture details
287 | │   └── QUICK_START.md       # Quick start guide
288 | │
289 | ├── .env.example             # Environment variables template
290 | ├── docker-compose.yml       # Docker Compose configuration
291 | ├── package.json             # Root package.json
292 | └── README.md               # This file
293 | ```
294 | 
295 | ---
296 | 
297 | ## 🤖 Agent System
298 | 
299 | ### Monitor Agent
300 | 
301 | **Purpose**: Continuously monitors weather conditions across vendor locations
302 | 
303 | **Responsibilities**:
304 | - Fetch real-time weather data from OpenWeather API
305 | - Track weather conditions for all vendor locations
306 | - Generate alerts for severe weather conditions
307 | - Identify affected vendors
308 | - Provide weather forecasts
309 | 
310 | **Configuration**: `apps/backend/src/agents/monitor/config.py`
311 | 
312 | ### Auditor Agent
313 | 
314 | **Purpose**: Analyzes emissions and optimizes logistics operations
315 | 
316 | **Responsibilities**:
317 | - Calculate emissions for routes and vehicles
318 | - Optimize routes for minimal emissions
319 | - Prioritize fleet based on efficiency
320 | - Generate recommendations using watsonx.ai
321 | - Provide cost-benefit analysis
322 | 
323 | **Configuration**: `apps/backend/src/agents/auditor/config.py`
324 | 
325 | ### Orchestrator Agent
326 | 
327 | **Purpose**: Coordinates workflow between Monitor and Auditor agents
328 | 
329 | **Responsibilities**:
330 | - Manage agent lifecycle
331 | - Coordinate inter-agent communication
332 | - Handle weather alerts and trigger audits
333 | - Aggregate results for frontend
334 | - Implement retry logic and error handling
335 | 
336 | **Configuration**: `apps/backend/src/agents/orchestrator/config.py`
337 | 
338 | ### Message Bus
339 | 
340 | The agents communicate via a custom message bus that supports:
341 | - Publish-subscribe pattern
342 | - Priority-based message queuing
343 | - Request-response patterns
344 | - Message expiration (TTL)
345 | - Message history for debugging
346 | 
347 | ---
348 | 
349 | ## 💻 Development
350 | 
351 | ### Running Tests
352 | 
353 | **All tests:**
354 | ```bash
355 | npm run test
356 | ```
357 | 
358 | **Frontend only:**
359 | ```bash
360 | cd apps/frontend
361 | npm test
362 | ```
363 | 
364 | **Backend only:**
365 | ```bash
366 | cd apps/backend
367 | pytest
368 | ```
369 | 
370 | **With coverage:**
371 | ```powershell
372 | .\scripts\test.ps1 -Coverage
373 | ```
374 | 
375 | ### Code Quality
376 | 
377 | **Linting:**
378 | ```bash
379 | npm run lint
380 | ```
381 | 
382 | **Formatting:**
383 | ```bash
384 | npm run format
385 | ```
386 | 
387 | **Type checking:**
388 | ```bash
389 | npm run type-check
390 | ```
391 | 
392 | ### Environment Variables
393 | 
394 | See `.env.example` for all available configuration options.
395 | 
396 | Key variables:
397 | - `WATSONX_API_KEY`: IBM watsonx.ai API key
398 | - `WATSONX_PROJECT_ID`: IBM watsonx.ai project ID
399 | - `OPENWEATHER_API_KEY`: OpenWeather API key
400 | - `BACKEND_PORT`: Backend server port (default: 8000)
401 | - `LOG_LEVEL`: Logging level (default: info)
402 | 
403 | ---
404 | 
405 | ## 🚢 Deployment
406 | 
407 | ### Docker Deployment
408 | 
409 | ```bash
410 | # Build production images
411 | docker-compose -f docker-compose.prod.yml build
412 | 
413 | # Start services
414 | docker-compose -f docker-compose.prod.yml up -d
415 | 
416 | # Scale services
417 | docker-compose -f docker-compose.prod.yml up -d --scale backend=3
418 | ```
419 | 
420 | ### Manual Deployment
421 | 
422 | **Frontend:**
423 | ```bash
424 | cd apps/frontend
425 | npm run build
426 | npm start
427 | ```
428 | 
429 | **Backend:**
430 | ```bash
431 | cd apps/backend
432 | pip install -r requirements.txt
433 | uvicorn src.main:app --host 0.0.0.0 --port 8000
434 | ```
435 | 
436 | ### Environment-Specific Configuration
437 | 
438 | - **Development**: `.env`
439 | - **Staging**: `.env.staging`
440 | - **Production**: `.env.production`
441 | 
442 | ---
443 | 
444 | ## 📚 API Documentation
445 | 
446 | ### Interactive API Docs
447 | 
448 | - **Swagger UI**: http://localhost:8000/docs
449 | - **ReDoc**: http://localhost:8000/redoc
450 | 
451 | ### Key Endpoints
452 | 
453 | #### Agents
454 | - `GET /api/agents/status` - Get all agent statuses
455 | - `POST /api/agents/orchestrator/run` - Run orchestrator workflow
456 | - `GET /api/agents/orchestrator/results` - Get latest results
457 | 
458 | #### Weather
459 | - `GET /api/weather/current` - Get current weather for all vendors
460 | - `GET /api/weather/alerts` - Get active weather alerts
461 | - `GET /api/weather/forecast` - Get weather forecast
462 | 
463 | #### Vendors
464 | - `GET /api/vendors` - List all vendors
465 | - `GET /api/vendors/{id}` - Get vendor details
466 | - `GET /api/vendors/{id}/weather` - Get vendor weather data
467 | 
468 | #### Emissions
469 | - `POST /api/emissions/calculate` - Calculate emissions
470 | - `GET /api/emissions/stats` - Get emissions statistics
471 | - `POST /api/emissions/optimize` - Get optimization recommendations
472 | 
473 | ---
474 | 
475 | ## 🤝 Contributing
476 | 
477 | We welcome contributions! Please see our contributing guidelines:
478 | 
479 | 1. Fork the repository
480 | 2. Create a feature branch (`git checkout -b feature/amazing-feature`)
481 | 3. Commit your changes (`git commit -m 'Add amazing feature'`)
482 | 4. Push to the branch (`git push origin feature/amazing-feature`)
483 | 5. Open a Pull Request
484 | 
485 | ### Development Guidelines
486 | 
487 | - Follow existing code style
488 | - Write tests for new features
489 | - Update documentation
490 | - Keep commits atomic and well-described
491 | - Ensure all tests pass before submitting PR
492 | 
493 | ---
494 | 
495 | ## 📄 License
496 | 
497 | This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
498 | 
499 | ---
500 | 
501 | ## 🙏 Acknowledgments
502 | 
503 | - **IBM watsonx.ai** for AI capabilities
504 | - **OpenWeather** for weather data
505 | - **Next.js** and **FastAPI** communities
506 | - All contributors and supporters
507 | 
508 | ---
509 | 
510 | ## 📞 Support
511 | 
512 | - **Documentation**: [docs/](docs/)
513 | - **Issues**: [GitHub Issues](https://github.com/yourusername/eco-shift/issues)
514 | - **Discussions**: [GitHub Discussions](https://github.com/yourusername/eco-shift/discussions)
515 | 
516 | ---
517 | 
518 | ## 🗺️ Roadmap
519 | 
520 | - [ ] Mobile application
521 | - [ ] Advanced analytics and ML models
522 | - [ ] Integration with more weather providers
523 | - [ ] Real-time vehicle tracking
524 | - [ ] Multi-language support
525 | - [ ] Enhanced reporting capabilities
526 | - [ ] API rate limiting and authentication
527 | - [ ] Webhook support for external integrations
528 | 
529 | ---
530 | 
531 | **Built with ❤️ for a sustainable future**
</content>
</file>
<file><path>docs/ARCHITECTURE.md</path>
<content lines="1-771">
  1 | # Eco-Shift Monorepo Architecture
  2 | 
  3 | ## 📋 Executive Summary
  4 | 
  5 | This document outlines the monorepo architecture for **Eco-Shift**, a multi-agent supply chain orchestrator designed for the IBM Bob Hackathon. The structure prioritizes rapid development while maintaining scalability and clean separation of concerns.
  6 | 
  7 | ## 🏗️ Complete Directory Structure
  8 | 
  9 | ```
 10 | eco-shift/
 11 | ├── apps/
 12 | │   ├── frontend/                    # Next.js application
 13 | │   │   ├── src/
 14 | │   │   │   ├── app/                # Next.js 13+ app directory
 15 | │   │   │   │   ├── api/            # API routes (proxy to backend)
 16 | │   │   │   │   ├── dashboard/      # Dashboard pages
 17 | │   │   │   │   ├── layout.tsx
 18 | │   │   │   │   └── page.tsx
 19 | │   │   │   ├── components/         # React components
 20 | │   │   │   │   ├── ui/             # Reusable UI components
 21 | │   │   │   │   ├── dashboard/      # Dashboard-specific components
 22 | │   │   │   │   ├── charts/         # Data visualization components
 23 | │   │   │   │   └── animations/     # GSAP animation components
 24 | │   │   │   ├── lib/                # Frontend utilities
 25 | │   │   │   │   ├── api-client.ts   # Backend API client
 26 | │   │   │   │   ├── animations.ts   # GSAP utilities
 27 | │   │   │   │   └── utils.ts
 28 | │   │   │   ├── hooks/              # Custom React hooks
 29 | │   │   │   ├── styles/             # Global styles
 30 | │   │   │   └── types/              # Frontend-specific types
 31 | │   │   ├── public/                 # Static assets
 32 | │   │   ├── tests/                  # Frontend tests
 33 | │   │   ├── next.config.js
 34 | │   │   ├── tailwind.config.js
 35 | │   │   ├── tsconfig.json
 36 | │   │   └── package.json
 37 | │   │
 38 | │   └── backend/                     # Python backend application
 39 | │       ├── src/
 40 | │       │   ├── agents/             # BeeAI agent implementations
 41 | │       │   │   ├── __init__.py
 42 | │       │   │   ├── base_agent.py   # Base agent class
 43 | │       │   │   ├── monitor/        # Agent A: The Monitor
 44 | │       │   │   │   ├── __init__.py
 45 | │       │   │   │   ├── agent.py    # Monitor agent implementation
 46 | │       │   │   │   ├── weather_service.py
 47 | │       │   │   │   ├── vendor_manager.py
 48 | │       │   │   │   └── config.py
 49 | │       │   │   ├── auditor/        # Agent B: The Auditor
 50 | │       │   │   │   ├── __init__.py
 51 | │       │   │   │   ├── agent.py    # Auditor agent implementation
 52 | │       │   │   │   ├── emissions_calculator.py
 53 | │       │   │   │   ├── fleet_prioritizer.py
 54 | │       │   │   │   └── config.py
 55 | │       │   │   └── orchestrator/   # Agent coordination
 56 | │       │   │       ├── __init__.py
 57 | │       │   │       ├── coordinator.py
 58 | │       │   │       └── message_bus.py
 59 | │       │   ├── api/                # FastAPI/Flask REST API
 60 | │       │   │   ├── __init__.py
 61 | │       │   │   ├── main.py         # API entry point
 62 | │       │   │   ├── routes/
 63 | │       │   │   │   ├── __init__.py
 64 | │       │   │   │   ├── agents.py   # Agent status/control endpoints
 65 | │       │   │   │   ├── emissions.py # Emissions data endpoints
 66 | │       │   │   │   ├── vendors.py  # Vendor management endpoints
 67 | │       │   │   │   └── weather.py  # Weather data endpoints
 68 | │       │   │   ├── middleware/
 69 | │       │   │   │   ├── __init__.py
 70 | │       │   │   │   ├── cors.py
 71 | │       │   │   │   └── auth.py
 72 | │       │   │   └── schemas/        # Pydantic models
 73 | │       │   │       ├── __init__.py
 74 | │       │   │       ├── agent.py
 75 | │       │   │       ├── emissions.py
 76 | │       │   │       └── vendor.py
 77 | │       │   ├── services/           # Business logic layer
 78 | │       │   │   ├── __init__.py
 79 | │       │   │   ├── watsonx_service.py  # IBM watsonx.ai integration
 80 | │       │   │   ├── openweather_service.py
 81 | │       │   │   └── data_processor.py
 82 | │       │   ├── models/             # Data models
 83 | │       │   │   ├── __init__.py
 84 | │       │   │   ├── vendor.py
 85 | │       │   │   ├── emission.py
 86 | │       │   │   └── weather.py
 87 | │       │   ├── utils/              # Backend utilities
 88 | │       │   │   ├── __init__.py
 89 | │       │   │   ├── logger.py
 90 | │       │   │   ├── config.py
 91 | │       │   │   └── validators.py
 92 | │       │   └── db/                 # Database layer (if needed)
 93 | │       │       ├── __init__.py
 94 | │       │       └── connection.py
 95 | │       ├── tests/                  # Backend tests
 96 | │       │   ├── unit/
 97 | │       │   ├── integration/
 98 | │       │   └── conftest.py
 99 | │       ├── requirements.txt
100 | │       ├── requirements-dev.txt
101 | │       ├── pyproject.toml
102 | │       └── README.md
103 | │
104 | ├── packages/                        # Shared packages
105 | │   ├── types/                      # Shared TypeScript types
106 | │   │   ├── src/
107 | │   │   │   ├── index.ts
108 | │   │   │   ├── agent.types.ts
109 | │   │   │   ├── emissions.types.ts
110 | │   │   │   ├── vendor.types.ts
111 | │   │   │   └── api.types.ts
112 | │   │   ├── package.json
113 | │   │   └── tsconfig.json
114 | │   │
115 | │   └── config/                     # Shared configuration
116 | │       ├── eslint-config/          # Shared ESLint config
117 | │       │   ├── index.js
118 | │       │   └── package.json
119 | │       └── tsconfig/               # Shared TypeScript configs
120 | │           ├── base.json
121 | │           ├── nextjs.json
122 | │           └── package.json
123 | │
124 | ├── scripts/                         # Development and deployment scripts
125 | │   ├── setup.sh                    # Initial setup script
126 | │   ├── dev.sh                      # Start all services in dev mode
127 | │   ├── build.sh                    # Build all applications
128 | │   ├── test.sh                     # Run all tests
129 | │   └── deploy.sh                   # Deployment script
130 | │
131 | ├── docs/                           # Documentation
132 | │   ├── ARCHITECTURE.md             # This file
133 | │   ├── API.md                      # API documentation
134 | │   ├── AGENTS.md                   # Agent behavior documentation
135 | │   ├── DEPLOYMENT.md               # Deployment guide
136 | │   └── DEVELOPMENT.md              # Development guide
137 | │
138 | ├── config/                         # Root-level configuration
139 | │   ├── .env.example                # Environment variables template
140 | │   ├── docker-compose.yml          # Docker composition (optional)
141 | │   └── nginx.conf                  # Nginx config (if needed)
142 | │
143 | ├── .github/                        # GitHub configuration
144 | │   └── workflows/
145 | │       ├── ci.yml                  # CI pipeline
146 | │       └── deploy.yml              # Deployment pipeline
147 | │
148 | ├── .gitignore
149 | ├── README.md
150 | ├── AGENTS.md                       # Agent guidance file
151 | ├── package.json                    # Root package.json (workspace config)
152 | ├── pnpm-workspace.yaml             # PNPM workspace config
153 | └── turbo.json                      # Turborepo config (optional)
154 | ```
155 | 
156 | ## 🎯 Architectural Rationale
157 | 
158 | ### 1. **Monorepo Structure Choice**
159 | 
160 | **Decision:** Apps-based monorepo with shared packages
161 | 
162 | **Rationale:**
163 | - **Clear Separation:** [`apps/`](apps/) directory clearly separates deployable applications
164 | - **Code Reuse:** [`packages/`](packages/) enables sharing types and configs between frontend/backend
165 | - **Independent Deployment:** Each app can be deployed independently
166 | - **Scalability:** Easy to add new agents or services without restructuring
167 | - **Hackathon-Friendly:** Simple mental model, easy for team members to navigate
168 | 
169 | ### 2. **Frontend Structure ([`apps/frontend/`](apps/frontend/))**
170 | 
171 | **Technology:** Next.js 13+ with App Router
172 | 
173 | **Key Decisions:**
174 | - **App Router:** Modern Next.js structure for better performance and DX
175 | - **Component Organization:** Separated by function (ui, dashboard, charts, animations)
176 | - **API Routes as Proxy:** Next.js API routes proxy to Python backend for security
177 | - **GSAP Integration:** Dedicated [`animations/`](apps/frontend/src/components/animations/) directory for GSAP components
178 | - **Type Safety:** Local types + shared types from [`packages/types/`](packages/types/)
179 | 
180 | **Benefits:**
181 | - Fast development with Next.js hot reload
182 | - Built-in API routes for backend communication
183 | - Tailwind CSS for rapid styling
184 | - GSAP for smooth, professional animations
185 | 
186 | ### 3. **Backend Structure ([`apps/backend/`](apps/backend/))**
187 | 
188 | **Technology:** Python with BeeAI framework + FastAPI
189 | 
190 | **Key Decisions:**
191 | 
192 | #### **Agent Organization ([`src/agents/`](apps/backend/src/agents/))**
193 | ```
194 | agents/
195 | ├── base_agent.py          # Abstract base class for all agents
196 | ├── monitor/               # Agent A: Weather monitoring & vendor management
197 | ├── auditor/               # Agent B: Emissions calculation & fleet prioritization
198 | └── orchestrator/          # Coordinates agent communication
199 | ```
200 | 
201 | **Agent Design Principles:**
202 | - **Modularity:** Each agent is self-contained with its own config
203 | - **Extensibility:** Base agent class makes adding new agents trivial
204 | - **Separation of Concerns:** Each agent has dedicated service modules
205 | - **BeeAI Integration:** Agents use BeeAI framework for AI capabilities
206 | - **Message Bus:** Orchestrator enables inter-agent communication
207 | 
208 | #### **API Layer ([`src/api/`](apps/backend/src/api/))**
209 | - **FastAPI:** Modern, fast, with automatic OpenAPI docs
210 | - **Route Organization:** Grouped by domain (agents, emissions, vendors, weather)
211 | - **Pydantic Schemas:** Type-safe request/response validation
212 | - **Middleware:** CORS, auth, logging centralized
213 | 
214 | #### **Services Layer ([`src/services/`](apps/backend/src/services/))**
215 | - **watsonx_service.py:** IBM watsonx.ai Granite-3.0-8b integration
216 | - **openweather_service.py:** OpenWeather API client
217 | - **data_processor.py:** Business logic for data transformation
218 | 
219 | **Benefits:**
220 | - Clean architecture with clear layers
221 | - Easy to test each component independently
222 | - Scalable for adding more agents
223 | - Type-safe with Pydantic models
224 | 
225 | ### 4. **Shared Packages ([`packages/`](packages/))**
226 | 
227 | #### **Types Package ([`packages/types/`](packages/types/))**
228 | **Purpose:** Single source of truth for data structures
229 | 
230 | **Contents:**
231 | - [`agent.types.ts`](packages/types/src/agent.types.ts): Agent status, configuration types
232 | - [`emissions.types.ts`](packages/types/src/emissions.types.ts): Scope 3 emissions data structures
233 | - [`vendor.types.ts`](packages/types/src/vendor.types.ts): Vendor and fleet information
234 | - [`api.types.ts`](packages/types/src/api.types.ts): API request/response types
235 | 
236 | **Benefits:**
237 | - Frontend and backend share same type definitions
238 | - Reduces bugs from type mismatches
239 | - Single place to update when data structures change
240 | 
241 | #### **Config Package ([`packages/config/`](packages/config/))**
242 | **Purpose:** Shared linting and TypeScript configurations
243 | 
244 | **Benefits:**
245 | - Consistent code style across all TypeScript code
246 | - DRY principle for configuration
247 | - Easy to update standards project-wide
248 | 
249 | ### 5. **Configuration Management**
250 | 
251 | #### **Environment Variables Strategy**
252 | 
253 | ```
254 | config/
255 | └── .env.example          # Template with all required variables
256 | 
257 | apps/frontend/
258 | └── .env.local            # Frontend-specific variables
259 | 
260 | apps/backend/
261 | └── .env                  # Backend-specific variables
262 | ```
263 | 
264 | **Key Variables:**
265 | ```bash
266 | # Backend (.env)
267 | WATSONX_API_KEY=your_key
268 | WATSONX_PROJECT_ID=your_project
269 | OPENWEATHER_API_KEY=your_key
270 | DATABASE_URL=postgresql://...
271 | CORS_ORIGINS=http://localhost:3000
272 | 
273 | # Frontend (.env.local)
274 | NEXT_PUBLIC_API_URL=http://localhost:8000
275 | NEXT_PUBLIC_ENABLE_ANALYTICS=false
276 | ```
277 | 
278 | **Benefits:**
279 | - Clear separation of frontend/backend secrets
280 | - Template file prevents missing variables
281 | - NEXT_PUBLIC_ prefix for client-safe variables
282 | 
283 | ### 6. **Agent Architecture Deep Dive**
284 | 
285 | #### **Agent A: The Monitor**
286 | 
287 | **Location:** [`apps/backend/src/agents/monitor/`](apps/backend/src/agents/monitor/)
288 | 
289 | **Responsibilities:**
290 | 1. Poll OpenWeather API for weather data
291 | 2. Manage vendor lists and availability
292 | 3. Trigger alerts based on weather conditions
293 | 4. Communicate with Auditor agent
294 | 
295 | **Key Files:**
296 | - [`agent.py`](apps/backend/src/agents/monitor/agent.py): Main agent logic using BeeAI
297 | - [`weather_service.py`](apps/backend/src/agents/monitor/weather_service.py): OpenWeather API integration
298 | - [`vendor_manager.py`](apps/backend/src/agents/monitor/vendor_manager.py): Vendor CRUD operations
299 | - [`config.py`](apps/backend/src/agents/monitor/config.py): Agent-specific configuration
300 | 
301 | **Data Flow:**
302 | ```
303 | OpenWeather API → weather_service.py → agent.py → orchestrator → Frontend
304 |                                       ↓
305 |                                 vendor_manager.py → Database
306 | ```
307 | 
308 | #### **Agent B: The Auditor**
309 | 
310 | **Location:** [`apps/backend/src/agents/auditor/`](apps/backend/src/agents/auditor/)
311 | 
312 | **Responsibilities:**
313 | 1. Calculate Scope 3 emissions for supply chain
314 | 2. Prioritize hydrogen-fueled fleets
315 | 3. Generate sustainability reports
316 | 4. Provide recommendations via watsonx.ai
317 | 
318 | **Key Files:**
319 | - [`agent.py`](apps/backend/src/agents/auditor/agent.py): Main agent logic using BeeAI
320 | - [`emissions_calculator.py`](apps/backend/src/agents/auditor/emissions_calculator.py): Scope 3 calculations
321 | - [`fleet_prioritizer.py`](apps/backend/src/agents/auditor/fleet_prioritizer.py): Fleet ranking logic
322 | - [`config.py`](apps/backend/src/agents/auditor/config.py): Agent-specific configuration
323 | 
324 | **Data Flow:**
325 | ```
326 | Vendor Data → emissions_calculator.py → agent.py → watsonx.ai (Granite-3.0-8b)
327 |                                        ↓
328 |                               fleet_prioritizer.py → Recommendations → Frontend
329 | ```
330 | 
331 | #### **Agent Orchestrator**
332 | 
333 | **Location:** [`apps/backend/src/agents/orchestrator/`](apps/backend/src/agents/orchestrator/)
334 | 
335 | **Purpose:** Coordinate communication between agents
336 | 
337 | **Key Components:**
338 | - [`coordinator.py`](apps/backend/src/agents/orchestrator/coordinator.py): Manages agent lifecycle
339 | - [`message_bus.py`](apps/backend/src/agents/orchestrator/message_bus.py): Inter-agent messaging
340 | 
341 | **Communication Pattern:**
342 | ```
343 | Monitor Agent → Message Bus → Auditor Agent
344 |       ↓                            ↓
345 |   Weather Data              Emissions Analysis
346 |       ↓                            ↓
347 |       └──────→ Orchestrator ←──────┘
348 |                     ↓
349 |               API Layer → Frontend
350 | ```
351 | 
352 | ### 7. **API Integration Points**
353 | 
354 | #### **Frontend → Backend Communication**
355 | 
356 | **Architecture:** Next.js API Routes as Proxy
357 | 
358 | ```typescript
359 | // apps/frontend/src/app/api/agents/route.ts
360 | export async function GET() {
361 |   const response = await fetch(`${process.env.BACKEND_URL}/api/agents`);
362 |   return Response.json(await response.json());
363 | }
364 | ```
365 | 
366 | **Benefits:**
367 | - Hides backend URL from client
368 | - Enables server-side authentication
369 | - CORS handled automatically
370 | - Can add caching/rate limiting
371 | 
372 | #### **Backend API Endpoints**
373 | 
374 | **Base URL:** `http://localhost:8000/api`
375 | 
376 | **Key Endpoints:**
377 | 
378 | ```python
379 | # Agent Management
380 | GET    /api/agents                    # List all agents and status
381 | GET    /api/agents/{agent_id}         # Get specific agent details
382 | POST   /api/agents/{agent_id}/start   # Start an agent
383 | POST   /api/agents/{agent_id}/stop    # Stop an agent
384 | 
385 | # Weather Data (Monitor Agent)
386 | GET    /api/weather/current           # Current weather data
387 | GET    /api/weather/forecast          # Weather forecast
388 | GET    /api/weather/alerts            # Weather alerts
389 | 
390 | # Vendor Management (Monitor Agent)
391 | GET    /api/vendors                   # List all vendors
392 | POST   /api/vendors                   # Add new vendor
393 | PUT    /api/vendors/{vendor_id}       # Update vendor
394 | DELETE /api/vendors/{vendor_id}       # Remove vendor
395 | 
396 | # Emissions Data (Auditor Agent)
397 | GET    /api/emissions/scope3          # Scope 3 emissions data
398 | GET    /api/emissions/analysis        # Emissions analysis
399 | POST   /api/emissions/calculate       # Calculate emissions for route
400 | 
401 | # Fleet Management (Auditor Agent)
402 | GET    /api/fleets                    # List all fleets
403 | GET    /api/fleets/prioritized        # Hydrogen-prioritized fleets
404 | GET    /api/fleets/{fleet_id}/score   # Get fleet sustainability score
405 | ```
406 | 
407 | #### **WebSocket Support (Optional for Real-time Updates)**
408 | 
409 | ```python
410 | # apps/backend/src/api/websocket.py
411 | @app.websocket("/ws/agents")
412 | async def agent_updates(websocket: WebSocket):
413 |     # Stream agent status updates to frontend
414 |     pass
415 | ```
416 | 
417 | ### 8. **Testing Strategy**
418 | 
419 | #### **Frontend Tests ([`apps/frontend/tests/`](apps/frontend/tests/))**
420 | ```
421 | tests/
422 | ├── unit/                  # Component unit tests
423 | │   ├── components/
424 | │   └── hooks/
425 | ├── integration/           # API integration tests
426 | └── e2e/                   # End-to-end tests (Playwright)
427 | ```
428 | 
429 | **Tools:** Jest, React Testing Library, Playwright
430 | 
431 | #### **Backend Tests ([`apps/backend/tests/`](apps/backend/tests/))**
432 | ```
433 | tests/
434 | ├── unit/                  # Unit tests for services/agents
435 | │   ├── test_agents.py
436 | │   ├── test_services.py
437 | │   └── test_utils.py
438 | ├── integration/           # API integration tests
439 | │   ├── test_api_routes.py
440 | │   └── test_agent_communication.py
441 | └── conftest.py            # Pytest fixtures
442 | ```
443 | 
444 | **Tools:** pytest, pytest-asyncio, httpx (for API testing)
445 | 
446 | ### 9. **Development Workflow**
447 | 
448 | #### **Quick Start Commands**
449 | 
450 | ```bash
451 | # Initial setup
452 | ./scripts/setup.sh
453 | 
454 | # Start all services in development mode
455 | ./scripts/dev.sh
456 | 
457 | # Run tests
458 | ./scripts/test.sh
459 | 
460 | # Build for production
461 | ./scripts/build.sh
462 | ```
463 | 
464 | #### **Individual Service Commands**
465 | 
466 | ```bash
467 | # Frontend only
468 | cd apps/frontend
469 | npm run dev              # Start dev server on :3000
470 | 
471 | # Backend only
472 | cd apps/backend
473 | python -m uvicorn src.api.main:app --reload  # Start API on :8000
474 | ```
475 | 
476 | ### 10. **Scalability Considerations**
477 | 
478 | #### **Adding New Agents**
479 | 
480 | **Process:**
481 | 1. Create new directory in [`apps/backend/src/agents/`](apps/backend/src/agents/)
482 | 2. Extend [`base_agent.py`](apps/backend/src/agents/base_agent.py)
483 | 3. Register with orchestrator
484 | 4. Add API routes if needed
485 | 5. Update frontend to display agent status
486 | 
487 | **Example Structure:**
488 | ```python
489 | # apps/backend/src/agents/optimizer/agent.py
490 | from agents.base_agent import BaseAgent
491 | 
492 | class OptimizerAgent(BaseAgent):
493 |     def __init__(self):
494 |         super().__init__(name="optimizer")
495 |     
496 |     async def execute(self):
497 |         # Agent logic here
498 |         pass
499 | ```
500 | 
501 | #### **Future Agent Ideas**
502 | - **Route Optimizer:** Optimizes delivery routes based on emissions
503 | - **Demand Forecaster:** Predicts supply chain demand using AI
504 | - **Risk Assessor:** Evaluates supply chain risks
505 | - **Cost Analyzer:** Analyzes cost vs. sustainability tradeoffs
506 | 
507 | ### 11. **Technology Integration Details**
508 | 
509 | #### **IBM watsonx.ai Integration**
510 | 
511 | **Location:** [`apps/backend/src/services/watsonx_service.py`](apps/backend/src/services/watsonx_service.py)
512 | 
513 | ```python
514 | from ibm_watsonx_ai import Credentials, APIClient
515 | from ibm_watsonx_ai.foundation_models import ModelInference
516 | 
517 | class WatsonXService:
518 |     def __init__(self):
519 |         self.credentials = Credentials(
520 |             api_key=os.getenv("WATSONX_API_KEY"),
521 |             url="https://us-south.ml.cloud.ibm.com"
522 |         )
523 |         self.client = APIClient(self.credentials)
524 |         self.model = ModelInference(
525 |             model_id="ibm/granite-3-8b-instruct",
526 |             credentials=self.credentials,
527 |             project_id=os.getenv("WATSONX_PROJECT_ID")
528 |         )
529 |     
530 |     async def generate_recommendations(self, emissions_data):
531 |         prompt = f"Analyze emissions data and provide recommendations: {emissions_data}"
532 |         response = self.model.generate(prompt=prompt)
533 |         return response
534 | ```
535 | 
536 | #### **BeeAI Framework Integration**
537 | 
538 | **Location:** [`apps/backend/src/agents/base_agent.py`](apps/backend/src/agents/base_agent.py)
539 | 
540 | ```python
541 | from bee_agent import BeeAgent, Tool
542 | 
543 | class BaseAgent(BeeAgent):
544 |     def __init__(self, name: str):
545 |         super().__init__(name=name)
546 |         self.tools = self._register_tools()
547 |     
548 |     def _register_tools(self) -> list[Tool]:
549 |         # Register tools for the agent
550 |         return []
551 |     
552 |     async def execute(self):
553 |         # Override in subclasses
554 |         raise NotImplementedError
555 | ```
556 | 
557 | #### **GSAP Animation Setup**
558 | 
559 | **Location:** [`apps/frontend/src/lib/animations.ts`](apps/frontend/src/lib/animations.ts)
560 | 
561 | ```typescript
562 | import gsap from 'gsap';
563 | import { ScrollTrigger } from 'gsap/ScrollTrigger';
564 | 
565 | gsap.registerPlugin(ScrollTrigger);
566 | 
567 | export const fadeInUp = (element: HTMLElement) => {
568 |   gsap.from(element, {
569 |     y: 50,
570 |     opacity: 0,
571 |     duration: 0.8,
572 |     ease: 'power3.out'
573 |   });
574 | };
575 | 
576 | export const animateEmissionsChart = (data: number[]) => {
577 |   // Custom GSAP animations for charts
578 | };
579 | ```
580 | 
581 | ### 12. **Hackathon-Specific Optimizations**
582 | 
583 | #### **Rapid Development Priorities**
584 | 
585 | 1. **Use Mock Data Initially**
586 |    - Create [`apps/backend/src/utils/mock_data.py`](apps/backend/src/utils/mock_data.py)
587 |    - Allows frontend development without waiting for API integrations
588 | 
589 | 2. **Parallel Development**
590 |    - Frontend team: Work on UI with mock data
591 |    - Backend team: Implement agents and API
592 |    - Integration: Last 12 hours
593 | 
594 | 3. **Pre-built Components**
595 |    - Use shadcn/ui for rapid UI development
596 |    - Tailwind CSS for quick styling
597 |    - Chart.js or Recharts for data visualization
598 | 
599 | 4. **Simplified Authentication**
600 |    - Skip complex auth for hackathon
601 |    - Use simple API key if needed
602 | 
603 | 5. **Docker Compose for Easy Setup**
604 |    ```yaml
605 |    # config/docker-compose.yml
606 |    services:
607 |      frontend:
608 |        build: ./apps/frontend
609 |        ports:
610 |          - "3000:3000"
611 |      backend:
612 |        build: ./apps/backend
613 |        ports:
614 |          - "8000:8000"
615 |        environment:
616 |          - WATSONX_API_KEY=${WATSONX_API_KEY}
617 |    ```
618 | 
619 | ### 13. **Documentation Strategy**
620 | 
621 | #### **Essential Documentation Files**
622 | 
623 | 1. **[`docs/API.md`](docs/API.md)**: Complete API documentation with examples
624 | 2. **[`docs/AGENTS.md`](docs/AGENTS.md)**: Agent behavior and communication patterns
625 | 3. **[`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)**: Setup and development guide
626 | 4. **[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)**: Deployment instructions
627 | 
628 | #### **Code Documentation**
629 | 
630 | - **Python:** Docstrings for all classes and functions
631 | - **TypeScript:** JSDoc comments for complex functions
632 | - **README.md:** In each major directory explaining its purpose
633 | 
634 | ## 🚀 Implementation Timeline (48 Hours)
635 | 
636 | ### **Hour 0-4: Setup & Foundation**
637 | - [ ] Initialize monorepo structure
638 | - [ ] Set up Next.js frontend
639 | - [ ] Set up Python backend with FastAPI
640 | - [ ] Configure shared types package
641 | - [ ] Set up development scripts
642 | 
643 | ### **Hour 4-12: Core Agent Development**
644 | - [ ] Implement Monitor Agent (Agent A)
645 | - [ ] Implement Auditor Agent (Agent B)
646 | - [ ] Set up agent orchestrator
647 | - [ ] Integrate OpenWeather API
648 | - [ ] Integrate IBM watsonx.ai
649 | 
650 | ### **Hour 12-24: API & Integration**
651 | - [ ] Build FastAPI endpoints
652 | - [ ] Implement frontend API client
653 | - [ ] Connect agents to API
654 | - [ ] Test agent communication
655 | - [ ] Set up WebSocket for real-time updates
656 | 
657 | ### **Hour 24-36: Frontend Development**
658 | - [ ] Build dashboard UI
659 | - [ ] Implement data visualization
660 | - [ ] Add GSAP animations
661 | - [ ] Connect to backend API
662 | - [ ] Responsive design with Tailwind
663 | 
664 | ### **Hour 36-44: Testing & Polish**
665 | - [ ] Integration testing
666 | - [ ] Bug fixes
667 | - [ ] Performance optimization
668 | - [ ] Documentation
669 | - [ ] Demo preparation
670 | 
671 | ### **Hour 44-48: Final Touches**
672 | - [ ] Final testing
673 | - [ ] Deployment
674 | - [ ] Demo rehearsal
675 | - [ ] Presentation materials
676 | 
677 | ## 📊 Architecture Diagram
678 | 
679 | ```mermaid
680 | graph TB
681 |     subgraph "Frontend - Next.js"
682 |         UI[User Interface]
683 |         API_ROUTES[API Routes Proxy]
684 |         COMPONENTS[React Components]
685 |         GSAP[GSAP Animations]
686 |     end
687 | 
688 |     subgraph "Backend - Python"
689 |         FASTAPI[FastAPI Server]
690 |         
691 |         subgraph "Agents"
692 |             MONITOR[Monitor Agent<br/>Weather & Vendors]
693 |             AUDITOR[Auditor Agent<br/>Emissions & Fleets]
694 |             ORCH[Orchestrator]
695 |         end
696 |         
697 |         subgraph "Services"
698 |             WATSONX[watsonx.ai Service<br/>Granite-3.0-8b]
699 |             WEATHER_SVC[OpenWeather Service]
700 |             DATA_PROC[Data Processor]
701 |         end
702 |     end
703 | 
704 |     subgraph "External APIs"
705 |         OPENWEATHER[OpenWeather API]
706 |         IBM_WATSONX[IBM watsonx.ai]
707 |     end
708 | 
709 |     subgraph "Shared"
710 |         TYPES[Shared Types Package]
711 |     end
712 | 
713 |     UI --> API_ROUTES
714 |     API_ROUTES --> FASTAPI
715 |     COMPONENTS --> GSAP
716 |     COMPONENTS --> TYPES
717 |     
718 |     FASTAPI --> MONITOR
719 |     FASTAPI --> AUDITOR
720 |     MONITOR --> ORCH
721 |     AUDITOR --> ORCH
722 |     
723 |     MONITOR --> WEATHER_SVC
724 |     AUDITOR --> WATSONX
725 |     AUDITOR --> DATA_PROC
726 |     
727 |     WEATHER_SVC --> OPENWEATHER
728 |     WATSONX --> IBM_WATSONX
729 |     
730 |     FASTAPI --> TYPES
731 | ```
732 | 
733 | ## 🎯 Key Benefits of This Architecture
734 | 
735 | 1. **Clear Separation of Concerns**
736 |    - Frontend and backend are completely independent
737 |    - Agents are modular and self-contained
738 |    - Easy to understand and navigate
739 | 
740 | 2. **Scalability**
741 |    - Adding new agents is straightforward
742 |    - Can scale frontend and backend independently
743 |    - Shared types prevent integration issues
744 | 
745 | 3. **Developer Experience**
746 |    - Fast hot reload in development
747 |    - Clear directory structure
748 |    - Comprehensive documentation
749 | 
750 | 4. **Hackathon-Optimized**
751 |    - Parallel development possible
752 |    - Mock data support for rapid iteration
753 |    - Simple deployment with Docker
754 | 
755 | 5. **Production-Ready Foundation**
756 |    - Clean architecture for future expansion
757 |    - Proper testing structure
758 |    - Environment configuration management
759 | 
760 | ## 📝 Next Steps
761 | 
762 | 1. Review this architecture plan
763 | 2. Confirm tech stack choices
764 | 3. Set up initial monorepo structure
765 | 4. Begin parallel development on frontend and backend
766 | 5. Regular integration checkpoints
767 | 
768 | ---
769 | 
770 | **Questions or Concerns?**
771 | This architecture is designed to be flexible. If you need to adjust any part based on team expertise or time constraints, the modular structure makes it easy to adapt.
</content>
</file>
<file><path>package.json</path>
<content lines="1-78">
 1 | {
 2 |   "name": "eco-shift",
 3 |   "version": "1.0.0",
 4 |   "description": "AI-powered logistics optimization platform for sustainable supply chain management",
 5 |   "private": true,
 6 |   "workspaces": [
 7 |     "apps/*",
 8 |     "packages/*"
 9 |   ],
10 |   "scripts": {
11 |     "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
12 |     "dev:frontend": "cd apps/frontend && npm run dev",
13 |     "dev:backend": "cd apps/backend && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000",
14 |     "build": "npm run build:frontend && npm run build:backend",
15 |     "build:frontend": "cd apps/frontend && npm run build",
16 |     "build:backend": "cd apps/backend && pip install -r requirements.txt",
17 |     "start": "concurrently \"npm run start:backend\" \"npm run start:frontend\"",
18 |     "start:frontend": "cd apps/frontend && npm start",
19 |     "start:backend": "cd apps/backend && uvicorn src.main:app --host 0.0.0.0 --port 8000",
20 |     "test": "npm run test:frontend && npm run test:backend",
21 |     "test:frontend": "cd apps/frontend && npm test",
22 |     "test:backend": "cd apps/backend && pytest",
23 |     "test:watch": "npm run test:frontend -- --watch",
24 |     "lint": "npm run lint:frontend && npm run lint:backend",
25 |     "lint:frontend": "cd apps/frontend && npm run lint",
26 |     "lint:backend": "cd apps/backend && flake8 src/ tests/",
27 |     "lint:fix": "npm run lint:frontend -- --fix",
28 |     "format": "npm run format:frontend && npm run format:backend",
29 |     "format:frontend": "cd apps/frontend && prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
30 |     "format:backend": "cd apps/backend && black src/ tests/",
31 |     "type-check": "cd apps/frontend && tsc --noEmit",
32 |     "clean": "npm run clean:frontend && npm run clean:backend",
33 |     "clean:frontend": "cd apps/frontend && rm -rf .next node_modules",
34 |     "clean:backend": "cd apps/backend && find . -type d -name __pycache__ -exec rm -rf {} + && rm -rf .pytest_cache .mypy_cache",
35 |     "docker:build": "docker-compose build",
36 |     "docker:up": "docker-compose up -d",
37 |     "docker:down": "docker-compose down",
38 |     "docker:logs": "docker-compose logs -f",
39 |     "docker:restart": "docker-compose restart",
40 |     "docker:clean": "docker-compose down -v --remove-orphans",
41 |     "setup": "npm run setup:frontend && npm run setup:backend",
42 |     "setup:frontend": "cd apps/frontend && npm install",
43 |     "setup:backend": "cd apps/backend && pip install -r requirements.txt",
44 |     "setup:env": "node scripts/setup-env.js",
45 |     "agents:status": "cd apps/backend && python -m src.agents.orchestrator.cli status",
46 |     "agents:start": "cd apps/backend && python -m src.agents.orchestrator.cli start",
47 |     "agents:stop": "cd apps/backend && python -m src.agents.orchestrator.cli stop",
48 |     "db:migrate": "cd apps/backend && alembic upgrade head",
49 |     "db:rollback": "cd apps/backend && alembic downgrade -1",
50 |     "db:reset": "cd apps/backend && alembic downgrade base && alembic upgrade head",
51 |     "logs": "tail -f apps/backend/logs/app.log",
52 |     "health": "curl http://localhost:8000/health && curl http://localhost:3000/api/health"
53 |   },
54 |   "devDependencies": {
55 |     "concurrently": "^8.2.2",
56 |     "prettier": "^3.1.1"
57 |   },
58 |   "engines": {
59 |     "node": ">=18.0.0",
60 |     "npm": ">=9.0.0",
61 |     "python": ">=3.11.0"
62 |   },
63 |   "repository": {
64 |     "type": "git",
65 |     "url": "https://github.com/yourusername/eco-shift.git"
66 |   },
67 |   "keywords": [
68 |     "logistics",
69 |     "ai",
70 |     "sustainability",
71 |     "supply-chain",
72 |     "emissions",
73 |     "optimization",
74 |     "ibm-watsonx"
75 |   ],
76 |   "author": "Eco-Shift Team",
77 |   "license": "MIT"
78 | }
</content>
</file>
<file><path>apps/frontend/package.json</path>
<content lines="1-37">
 1 | {
 2 |   "name": "@eco-shift/frontend",
 3 |   "version": "0.1.0",
 4 |   "private": true,
 5 |   "scripts": {
 6 |     "dev": "next dev",
 7 |     "build": "next build",
 8 |     "start": "next start",
 9 |     "lint": "next lint",
10 |     "type-check": "tsc --noEmit",
11 |     "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\""
12 |   },
13 |   "dependencies": {
14 |     "next": "14.2.3",
15 |     "react": "^18.3.1",
16 |     "react-dom": "^18.3.1",
17 |     "axios": "^1.7.2",
18 |     "date-fns": "^3.6.0",
19 |     "gsap": "^3.12.5",
20 |     "clsx": "^2.1.1",
21 |     "tailwind-merge": "^2.3.0"
22 |   },
23 |   "devDependencies": {
24 |     "@types/node": "^20.12.12",
25 |     "@types/react": "^18.3.3",
26 |     "@types/react-dom": "^18.3.0",
27 |     "typescript": "^5.4.5",
28 |     "eslint": "^8.57.0",
29 |     "eslint-config-next": "14.2.3",
30 |     "eslint-config-prettier": "^9.1.0",
31 |     "prettier": "^3.2.5",
32 |     "tailwindcss": "^3.4.3",
33 |     "postcss": "^8.4.38",
34 |     "autoprefixer": "^10.4.19",
35 |     "@tailwindcss/typography": "^0.5.13"
36 |   }
37 | }
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
README.md

# VSCode Open Tabs
.gitignore,AGENTS.md,docs/ARCHITECTURE.md,docs/QUICK_START.md,apps/frontend/package.json,apps/frontend/tsconfig.json,apps/frontend/tailwind.config.ts,apps/frontend/next.config.js,apps/frontend/.eslintrc.json,apps/frontend/postcss.config.js,apps/frontend/src/styles/globals.css,apps/frontend/src/app/layout.tsx,apps/frontend/src/app/page.tsx,apps/frontend/src/lib/api.ts,apps/frontend/.env.example,apps/frontend/README.md,apps/frontend/src/lib/utils.ts,apps/frontend/src/lib/animations.ts,apps/frontend/.gitignore,apps/frontend/.prettierrc

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T07:21:47.691Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I need to read more files to gather comprehensive information about the agent system, backend configuration, and specific implementation details.

<read_file>
<args>
<file>
<path>apps/backend/pyproject.toml</path>
</file>
<file>
<path>apps/backend/src/agents/orchestrator/message_bus.py</path>
</file>
<file>
<path>apps/backend/src/agents/auditor/fleet_prioritizer.py</path>
</file>
<file>
<path>apps/backend/src/agents/monitor/weather_monitor.py</path>
</file>
<file>
<path>apps/backend/src/config/settings.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>apps/backend/pyproject.toml</path>
<content lines="1-123">
  1 | [build-system]
  2 | requires = ["setuptools>=68.0", "wheel"]
  3 | build-backend = "setuptools.build_meta"
  4 | 
  5 | [project]
  6 | name = "eco-shift-backend"
  7 | version = "0.1.0"
  8 | description = "Eco-Shift Backend - AI-powered carbon emissions monitoring and optimization"
  9 | readme = "README.md"
 10 | requires-python = ">=3.10"
 11 | license = {text = "MIT"}
 12 | authors = [
 13 |     {name = "Eco-Shift Team", email = "team@eco-shift.com"}
 14 | ]
 15 | keywords = ["carbon-emissions", "ai", "sustainability", "watsonx", "fastapi"]
 16 | classifiers = [
 17 |     "Development Status :: 3 - Alpha",
 18 |     "Intended Audience :: Developers",
 19 |     "License :: OSI Approved :: MIT License",
 20 |     "Programming Language :: Python :: 3",
 21 |     "Programming Language :: Python :: 3.10",
 22 |     "Programming Language :: Python :: 3.11",
 23 |     "Programming Language :: Python :: 3.12",
 24 | ]
 25 | 
 26 | dependencies = [
 27 |     "fastapi>=0.109.0",
 28 |     "uvicorn[standard]>=0.27.0",
 29 |     "python-multipart>=0.0.6",
 30 |     "ibm-watsonx-ai>=0.2.6",
 31 |     "ibm-watson-machine-learning>=1.0.335",
 32 |     "httpx>=0.26.0",
 33 |     "aiohttp>=3.9.1",
 34 |     "requests>=2.31.0",
 35 |     "pydantic>=2.5.3",
 36 |     "pydantic-settings>=2.1.0",
 37 |     "python-dotenv>=1.0.0",
 38 |     "python-json-logger>=2.0.7",
 39 |     "python-jose[cryptography]>=3.3.0",
 40 |     "passlib[bcrypt]>=1.7.4",
 41 |     "python-dateutil>=2.8.2",
 42 |     "pytz>=2023.3",
 43 | ]
 44 | 
 45 | [project.optional-dependencies]
 46 | dev = [
 47 |     "pytest>=7.4.3",
 48 |     "pytest-asyncio>=0.23.3",
 49 |     "pytest-cov>=4.1.0",
 50 |     "pytest-mock>=3.12.0",
 51 |     "flake8>=7.0.0",
 52 |     "black>=23.12.1",
 53 |     "isort>=5.13.2",
 54 |     "mypy>=1.8.0",
 55 | ]
 56 | 
 57 | [project.urls]
 58 | Homepage = "https://github.com/eco-shift/backend"
 59 | Documentation = "https://github.com/eco-shift/backend/docs"
 60 | Repository = "https://github.com/eco-shift/backend"
 61 | Issues = "https://github.com/eco-shift/backend/issues"
 62 | 
 63 | [tool.black]
 64 | line-length = 100
 65 | target-version = ['py310', 'py311', 'py312']
 66 | include = '\.pyi?$'
 67 | extend-exclude = '''
 68 | /(
 69 |   # directories
 70 |   \.eggs
 71 |   | \.git
 72 |   | \.hg
 73 |   | \.mypy_cache
 74 |   | \.tox
 75 |   | \.venv
 76 |   | build
 77 |   | dist
 78 | )/
 79 | '''
 80 | 
 81 | [tool.isort]
 82 | profile = "black"
 83 | line_length = 100
 84 | multi_line_output = 3
 85 | include_trailing_comma = true
 86 | force_grid_wrap = 0
 87 | use_parentheses = true
 88 | ensure_newline_before_comments = true
 89 | 
 90 | [tool.mypy]
 91 | python_version = "3.10"
 92 | warn_return_any = true
 93 | warn_unused_configs = true
 94 | disallow_untyped_defs = true
 95 | disallow_incomplete_defs = true
 96 | check_untyped_defs = true
 97 | no_implicit_optional = true
 98 | warn_redundant_casts = true
 99 | warn_unused_ignores = true
100 | warn_no_return = true
101 | strict_equality = true
102 | 
103 | [tool.pytest.ini_options]
104 | minversion = "7.0"
105 | addopts = "-ra -q --strict-markers --cov=src --cov-report=term-missing --cov-report=html"
106 | testpaths = ["tests"]
107 | pythonpath = ["src"]
108 | asyncio_mode = "auto"
109 | 
110 | [tool.coverage.run]
111 | source = ["src"]
112 | omit = ["*/tests/*", "*/test_*.py"]
113 | 
114 | [tool.coverage.report]
115 | exclude_lines = [
116 |     "pragma: no cover",
117 |     "def __repr__",
118 |     "raise AssertionError",
119 |     "raise NotImplementedError",
120 |     "if __name__ == .__main__.:",
121 |     "if TYPE_CHECKING:",
122 |     "@abstractmethod",
123 | ]
</content>
</file>
<file><path>apps/backend/src/agents/orchestrator/message_bus.py</path>
<content lines="1-375">
  1 | """
  2 | Message Bus for Inter-Agent Communication
  3 | 
  4 | This module provides a simple message bus for communication between agents
  5 | in the Eco-Shift system. It supports publish-subscribe pattern and message queuing.
  6 | """
  7 | 
  8 | import asyncio
  9 | import logging
 10 | from datetime import datetime, timedelta
 11 | from typing import Dict, List, Callable, Any, Optional
 12 | from dataclasses import dataclass, field
 13 | from enum import Enum
 14 | from collections import defaultdict
 15 | import uuid
 16 | 
 17 | 
 18 | logger = logging.getLogger(__name__)
 19 | 
 20 | 
 21 | class MessagePriority(Enum):
 22 |     """Message priority levels"""
 23 |     LOW = 1
 24 |     NORMAL = 2
 25 |     HIGH = 3
 26 |     CRITICAL = 4
 27 | 
 28 | 
 29 | class MessageType(Enum):
 30 |     """Types of messages that can be sent between agents"""
 31 |     WEATHER_ALERT = "weather_alert"
 32 |     VENDOR_LIST = "vendor_list"
 33 |     AUDIT_REQUEST = "audit_request"
 34 |     AUDIT_RESULT = "audit_result"
 35 |     OPTIMIZATION_REQUEST = "optimization_request"
 36 |     OPTIMIZATION_RESULT = "optimization_result"
 37 |     AGENT_STATUS = "agent_status"
 38 |     ERROR = "error"
 39 |     COMMAND = "command"
 40 | 
 41 | 
 42 | @dataclass
 43 | class Message:
 44 |     """Represents a message in the system"""
 45 |     
 46 |     id: str = field(default_factory=lambda: str(uuid.uuid4()))
 47 |     type: MessageType = MessageType.COMMAND
 48 |     sender: str = ""
 49 |     recipient: Optional[str] = None  # None means broadcast
 50 |     payload: Dict[str, Any] = field(default_factory=dict)
 51 |     priority: MessagePriority = MessagePriority.NORMAL
 52 |     timestamp: datetime = field(default_factory=datetime.utcnow)
 53 |     ttl: Optional[int] = None  # Time-to-live in seconds
 54 |     correlation_id: Optional[str] = None  # For request-response patterns
 55 |     
 56 |     def is_expired(self) -> bool:
 57 |         """Check if the message has expired"""
 58 |         if self.ttl is None:
 59 |             return False
 60 |         expiry_time = self.timestamp + timedelta(seconds=self.ttl)
 61 |         return datetime.utcnow() > expiry_time
 62 |     
 63 |     def to_dict(self) -> Dict[str, Any]:
 64 |         """Convert message to dictionary"""
 65 |         return {
 66 |             "id": self.id,
 67 |             "type": self.type.value,
 68 |             "sender": self.sender,
 69 |             "recipient": self.recipient,
 70 |             "payload": self.payload,
 71 |             "priority": self.priority.value,
 72 |             "timestamp": self.timestamp.isoformat(),
 73 |             "ttl": self.ttl,
 74 |             "correlation_id": self.correlation_id
 75 |         }
 76 | 
 77 | 
 78 | class MessageBus:
 79 |     """
 80 |     Simple message bus for inter-agent communication.
 81 |     
 82 |     Supports:
 83 |     - Publish-subscribe pattern
 84 |     - Message queuing
 85 |     - Priority-based delivery
 86 |     - Message expiration
 87 |     - Request-response patterns
 88 |     """
 89 |     
 90 |     def __init__(self, max_queue_size: int = 1000, default_ttl: int = 3600):
 91 |         self.max_queue_size = max_queue_size
 92 |         self.default_ttl = default_ttl
 93 |         
 94 |         # Subscribers: topic -> list of callback functions
 95 |         self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
 96 |         
 97 |         # Message queues: agent_id -> priority queue
 98 |         self._queues: Dict[str, asyncio.PriorityQueue] = {}
 99 |         
100 |         # Pending responses: correlation_id -> Future
101 |         self._pending_responses: Dict[str, asyncio.Future] = {}
102 |         
103 |         # Message history for debugging
104 |         self._message_history: List[Message] = []
105 |         self._max_history = 100
106 |         
107 |         self._running = False
108 |         self._cleanup_task: Optional[asyncio.Task] = None
109 |         
110 |         logger.info("Message bus initialized")
111 |     
112 |     async def start(self):
113 |         """Start the message bus"""
114 |         if self._running:
115 |             logger.warning("Message bus already running")
116 |             return
117 |         
118 |         self._running = True
119 |         self._cleanup_task = asyncio.create_task(self._cleanup_expired_messages())
120 |         logger.info("Message bus started")
121 |     
122 |     async def stop(self):
123 |         """Stop the message bus"""
124 |         if not self._running:
125 |             return
126 |         
127 |         self._running = False
128 |         if self._cleanup_task:
129 |             self._cleanup_task.cancel()
130 |             try:
131 |                 await self._cleanup_task
132 |             except asyncio.CancelledError:
133 |                 pass
134 |         
135 |         logger.info("Message bus stopped")
136 |     
137 |     def subscribe(self, topic: str, callback: Callable):
138 |         """
139 |         Subscribe to a topic
140 |         
141 |         Args:
142 |             topic: Topic to subscribe to (e.g., "weather_alert", "audit_result")
143 |             callback: Async function to call when message is received
144 |         """
145 |         self._subscribers[topic].append(callback)
146 |         logger.debug(f"Subscribed to topic: {topic}")
147 |     
148 |     def unsubscribe(self, topic: str, callback: Callable):
149 |         """Unsubscribe from a topic"""
150 |         if topic in self._subscribers and callback in self._subscribers[topic]:
151 |             self._subscribers[topic].remove(callback)
152 |             logger.debug(f"Unsubscribed from topic: {topic}")
153 |     
154 |     async def publish(self, message: Message):
155 |         """
156 |         Publish a message to all subscribers of its type
157 |         
158 |         Args:
159 |             message: Message to publish
160 |         """
161 |         if message.is_expired():
162 |             logger.warning(f"Attempted to publish expired message: {message.id}")
163 |             return
164 |         
165 |         # Set default TTL if not specified
166 |         if message.ttl is None:
167 |             message.ttl = self.default_ttl
168 |         
169 |         # Add to history
170 |         self._add_to_history(message)
171 |         
172 |         # Get topic from message type
173 |         topic = message.type.value
174 |         
175 |         # Publish to subscribers
176 |         if topic in self._subscribers:
177 |             logger.debug(f"Publishing message {message.id} to {len(self._subscribers[topic])} subscribers")
178 |             for callback in self._subscribers[topic]:
179 |                 try:
180 |                     if asyncio.iscoroutinefunction(callback):
181 |                         await callback(message)
182 |                     else:
183 |                         callback(message)
184 |                 except Exception as e:
185 |                     logger.error(f"Error in subscriber callback: {e}", exc_info=True)
186 |         
187 |         # If message has a specific recipient, add to their queue
188 |         if message.recipient:
189 |             await self._enqueue_message(message.recipient, message)
190 |     
191 |     async def send(self, message: Message):
192 |         """
193 |         Send a message directly to a recipient's queue
194 |         
195 |         Args:
196 |             message: Message to send
197 |         """
198 |         if not message.recipient:
199 |             raise ValueError("Message must have a recipient for direct send")
200 |         
201 |         if message.ttl is None:
202 |             message.ttl = self.default_ttl
203 |         
204 |         self._add_to_history(message)
205 |         await self._enqueue_message(message.recipient, message)
206 |     
207 |     async def request(self, message: Message, timeout: float = 30.0) -> Message:
208 |         """
209 |         Send a request and wait for a response
210 |         
211 |         Args:
212 |             message: Request message
213 |             timeout: Timeout in seconds
214 |             
215 |         Returns:
216 |             Response message
217 |         """
218 |         if not message.correlation_id:
219 |             message.correlation_id = str(uuid.uuid4())
220 |         
221 |         # Create a future for the response
222 |         future = asyncio.Future()
223 |         self._pending_responses[message.correlation_id] = future
224 |         
225 |         try:
226 |             # Send the request
227 |             await self.publish(message)
228 |             
229 |             # Wait for response with timeout
230 |             response = await asyncio.wait_for(future, timeout=timeout)
231 |             return response
232 |         except asyncio.TimeoutError:
233 |             logger.error(f"Request {message.correlation_id} timed out")
234 |             raise
235 |         finally:
236 |             # Clean up
237 |             self._pending_responses.pop(message.correlation_id, None)
238 |     
239 |     async def respond(self, request_message: Message, response_payload: Dict[str, Any]):
240 |         """
241 |         Send a response to a request
242 |         
243 |         Args:
244 |             request_message: Original request message
245 |             response_payload: Response data
246 |         """
247 |         if not request_message.correlation_id:
248 |             logger.warning("Cannot respond to message without correlation_id")
249 |             return
250 |         
251 |         response = Message(
252 |             type=request_message.type,
253 |             sender=request_message.recipient or "unknown",
254 |             recipient=request_message.sender,
255 |             payload=response_payload,
256 |             correlation_id=request_message.correlation_id
257 |         )
258 |         
259 |         # If there's a pending future, resolve it
260 |         if request_message.correlation_id in self._pending_responses:
261 |             future = self._pending_responses[request_message.correlation_id]
262 |             if not future.done():
263 |                 future.set_result(response)
264 |         else:
265 |             # Otherwise, just publish the response
266 |             await self.publish(response)
267 |     
268 |     async def receive(self, agent_id: str, timeout: Optional[float] = None) -> Optional[Message]:
269 |         """
270 |         Receive a message from an agent's queue
271 |         
272 |         Args:
273 |             agent_id: Agent identifier
274 |             timeout: Optional timeout in seconds
275 |             
276 |         Returns:
277 |             Message or None if timeout
278 |         """
279 |         if agent_id not in self._queues:
280 |             self._queues[agent_id] = asyncio.PriorityQueue(maxsize=self.max_queue_size)
281 |         
282 |         try:
283 |             if timeout:
284 |                 priority, message = await asyncio.wait_for(
285 |                     self._queues[agent_id].get(),
286 |                     timeout=timeout
287 |                 )
288 |             else:
289 |                 priority, message = await self._queues[agent_id].get()
290 |             
291 |             return message
292 |         except asyncio.TimeoutError:
293 |             return None
294 |     
295 |     async def _enqueue_message(self, agent_id: str, message: Message):
296 |         """Add a message to an agent's queue"""
297 |         if agent_id not in self._queues:
298 |             self._queues[agent_id] = asyncio.PriorityQueue(maxsize=self.max_queue_size)
299 |         
300 |         # Use negative priority for correct ordering (higher priority first)
301 |         priority = -message.priority.value
302 |         
303 |         try:
304 |             await self._queues[agent_id].put((priority, message))
305 |             logger.debug(f"Enqueued message {message.id} for {agent_id}")
306 |         except asyncio.QueueFull:
307 |             logger.error(f"Queue full for agent {agent_id}, dropping message {message.id}")
308 |     
309 |     def _add_to_history(self, message: Message):
310 |         """Add message to history"""
311 |         self._message_history.append(message)
312 |         if len(self._message_history) > self._max_history:
313 |             self._message_history.pop(0)
314 |     
315 |     async def _cleanup_expired_messages(self):
316 |         """Periodically clean up expired messages"""
317 |         while self._running:
318 |             try:
319 |                 await asyncio.sleep(60)  # Check every minute
320 |                 
321 |                 # Clean up message history
322 |                 self._message_history = [
323 |                     msg for msg in self._message_history
324 |                     if not msg.is_expired()
325 |                 ]
326 |                 
327 |                 logger.debug("Cleaned up expired messages")
328 |             except asyncio.CancelledError:
329 |                 break
330 |             except Exception as e:
331 |                 logger.error(f"Error in cleanup task: {e}", exc_info=True)
332 |     
333 |     def get_stats(self) -> Dict[str, Any]:
334 |         """Get message bus statistics"""
335 |         return {
336 |             "running": self._running,
337 |             "subscribers": {topic: len(callbacks) for topic, callbacks in self._subscribers.items()},
338 |             "queues": {agent_id: queue.qsize() for agent_id, queue in self._queues.items()},
339 |             "pending_responses": len(self._pending_responses),
340 |             "message_history_size": len(self._message_history)
341 |         }
342 |     
343 |     def get_message_history(self, limit: int = 50) -> List[Dict[str, Any]]:
344 |         """Get recent message history"""
345 |         return [msg.to_dict() for msg in self._message_history[-limit:]]
346 | 
347 | 
348 | # Global message bus instance
349 | _message_bus: Optional[MessageBus] = None
350 | 
351 | 
352 | def get_message_bus() -> MessageBus:
353 |     """Get the global message bus instance"""
354 |     global _message_bus
355 |     if _message_bus is None:
356 |         _message_bus = MessageBus()
357 |     return _message_bus
358 | 
359 | 
360 | async def initialize_message_bus(max_queue_size: int = 1000, default_ttl: int = 3600):
361 |     """Initialize and start the global message bus"""
362 |     global _message_bus
363 |     _message_bus = MessageBus(max_queue_size=max_queue_size, default_ttl=default_ttl)
364 |     await _message_bus.start()
365 |     return _message_bus
366 | 
367 | 
368 | async def shutdown_message_bus():
369 |     """Shutdown the global message bus"""
370 |     global _message_bus
371 |     if _message_bus:
372 |         await _message_bus.stop()
373 |         _message_bus = None
374 | 
375 | # Made with Bob
</content>
</file>
<file><path>apps/backend/src/agents/auditor/fleet_prioritizer.py</path>
<content lines="1-374">
  1 | """
  2 | Fleet prioritization system with heavy emphasis on hydrogen-fueled solutions.
  3 | """
  4 | 
  5 | from typing import Dict, Any, List, Optional
  6 | from pydantic import BaseModel, Field
  7 | 
  8 | from .config import auditor_config, get_fleet_priority
  9 | from .emissions_calculator import RouteEmissions
 10 | from src.utils.logger import get_logger
 11 | 
 12 | logger = get_logger(__name__)
 13 | 
 14 | 
 15 | class VendorScore(BaseModel):
 16 |     """Model for vendor scoring results."""
 17 |     
 18 |     vendor_id: str = Field(description="Vendor identifier")
 19 |     vendor_name: str = Field(description="Vendor name")
 20 |     fleet_type: str = Field(description="Fleet type")
 21 |     
 22 |     # Score components
 23 |     fleet_type_score: float = Field(description="Base fleet type score")
 24 |     eco_rating_score: float = Field(description="Eco rating score")
 25 |     reliability_score: float = Field(description="Reliability score")
 26 |     capacity_score: float = Field(description="Capacity score")
 27 |     emissions_score: float = Field(description="Emissions score")
 28 |     
 29 |     # Total score
 30 |     total_score: float = Field(description="Total weighted score")
 31 |     
 32 |     # Rankings
 33 |     rank: Optional[int] = Field(default=None, description="Overall rank")
 34 |     
 35 |     # Additional data
 36 |     emissions_kg: float = Field(description="Total emissions in kg CO2e")
 37 |     emissions_reduction_percent: float = Field(description="Emissions reduction vs baseline")
 38 |     eco_rating: float = Field(description="Vendor eco rating")
 39 |     reliability: float = Field(description="Vendor reliability score")
 40 |     
 41 |     # Recommendation strength
 42 |     recommendation_level: str = Field(description="Recommendation level (highly_recommended/recommended/acceptable)")
 43 | 
 44 | 
 45 | class FleetPrioritizer:
 46 |     """Prioritize vendors with heavy emphasis on hydrogen fleets."""
 47 |     
 48 |     def __init__(self):
 49 |         """Initialize fleet prioritizer."""
 50 |         self.config = auditor_config
 51 |         logger.info("Fleet prioritizer initialized with hydrogen-first strategy")
 52 |     
 53 |     def score_vendors(
 54 |         self,
 55 |         vendors: List[Dict[str, Any]],
 56 |         emissions_data: List[RouteEmissions],
 57 |     ) -> List[VendorScore]:
 58 |         """
 59 |         Score and rank vendors with hydrogen fleets receiving highest priority.
 60 |         
 61 |         Args:
 62 |             vendors: List of vendor data dictionaries
 63 |             emissions_data: List of calculated emissions for each vendor
 64 |             
 65 |         Returns:
 66 |             List of VendorScore objects, sorted by total score (highest first)
 67 |         """
 68 |         try:
 69 |             # Create emissions lookup
 70 |             emissions_map = {e.vendor_id: e for e in emissions_data}
 71 |             
 72 |             scores = []
 73 |             for vendor in vendors:
 74 |                 vendor_id = vendor.get("id", "unknown")
 75 |                 emissions = emissions_map.get(vendor_id)
 76 |                 
 77 |                 if not emissions:
 78 |                     logger.warning(f"No emissions data for vendor {vendor_id}, skipping")
 79 |                     continue
 80 |                 
 81 |                 score = self._calculate_vendor_score(vendor, emissions)
 82 |                 scores.append(score)
 83 |             
 84 |             # Sort by total score (highest first)
 85 |             scores.sort(key=lambda s: s.total_score, reverse=True)
 86 |             
 87 |             # Assign ranks
 88 |             for i, score in enumerate(scores, 1):
 89 |                 score.rank = i
 90 |             
 91 |             logger.info(f"Scored and ranked {len(scores)} vendors")
 92 |             return scores
 93 |             
 94 |         except Exception as e:
 95 |             logger.error(f"Error scoring vendors: {e}")
 96 |             raise
 97 |     
 98 |     def _calculate_vendor_score(
 99 |         self,
100 |         vendor: Dict[str, Any],
101 |         emissions: RouteEmissions,
102 |     ) -> VendorScore:
103 |         """
104 |         Calculate comprehensive score for a vendor.
105 |         
106 |         Args:
107 |             vendor: Vendor data
108 |             emissions: Emissions calculation results
109 |             
110 |         Returns:
111 |             VendorScore object
112 |         """
113 |         vendor_id = vendor.get("id", "unknown")
114 |         vendor_name = vendor.get("name", "Unknown")
115 |         fleet_type = vendor.get("fleet_type", "diesel").lower()
116 |         eco_rating = vendor.get("eco_rating", 0)
117 |         reliability = vendor.get("reliability_score", 0)
118 |         capacity = vendor.get("capacity_tons", 0)
119 |         
120 |         # 1. Fleet Type Score (Base Priority)
121 |         fleet_type_score = get_fleet_priority(fleet_type)
122 |         
123 |         # Apply 10x multiplier for hydrogen fleets (as specified)
124 |         if fleet_type == "hydrogen":
125 |             fleet_type_score *= 10.0
126 |             logger.debug(f"Applied 10x hydrogen multiplier to {vendor_name}")
127 |         
128 |         # 2. Eco Rating Score
129 |         eco_rating_score = eco_rating * self.config.fleet_priorities.eco_rating_multiplier
130 |         
131 |         # 3. Reliability Score
132 |         reliability_score = reliability * self.config.fleet_priorities.reliability_multiplier
133 |         
134 |         # 4. Capacity Score
135 |         capacity_score = capacity * self.config.fleet_priorities.capacity_multiplier
136 |         
137 |         # 5. Emissions Score (inverse - lower emissions = higher score)
138 |         # Normalize emissions to 0-100 scale
139 |         max_emissions = 500.0  # Assume max emissions for normalization
140 |         emissions_score = max(0, 100 - (emissions.total_emissions_kg / max_emissions * 100))
141 |         
142 |         # Boost emissions score for low-emission fleets
143 |         emissions_reduction = emissions.emissions_reduction_percent or 0
144 |         if emissions_reduction > 90:
145 |             emissions_score *= 1.5
146 |         elif emissions_reduction > 80:
147 |             emissions_score *= 1.3
148 |         elif emissions_reduction > 70:
149 |             emissions_score *= 1.2
150 |         
151 |         # Calculate total score
152 |         total_score = (
153 |             fleet_type_score +
154 |             eco_rating_score +
155 |             reliability_score +
156 |             capacity_score +
157 |             emissions_score
158 |         )
159 |         
160 |         # Determine recommendation level
161 |         recommendation_level = self._determine_recommendation_level(
162 |             fleet_type, total_score, emissions_reduction
163 |         )
164 |         
165 |         return VendorScore(
166 |             vendor_id=vendor_id,
167 |             vendor_name=vendor_name,
168 |             fleet_type=fleet_type,
169 |             fleet_type_score=round(fleet_type_score, 2),
170 |             eco_rating_score=round(eco_rating_score, 2),
171 |             reliability_score=round(reliability_score, 2),
172 |             capacity_score=round(capacity_score, 2),
173 |             emissions_score=round(emissions_score, 2),
174 |             total_score=round(total_score, 2),
175 |             emissions_kg=emissions.total_emissions_kg,
176 |             emissions_reduction_percent=emissions.emissions_reduction_percent or 0,
177 |             eco_rating=eco_rating,
178 |             reliability=reliability,
179 |             recommendation_level=recommendation_level,
180 |         )
181 |     
182 |     def _determine_recommendation_level(
183 |         self,
184 |         fleet_type: str,
185 |         total_score: float,
186 |         emissions_reduction: float,
187 |     ) -> str:
188 |         """
189 |         Determine recommendation level for a vendor.
190 |         
191 |         Args:
192 |             fleet_type: Type of fleet
193 |             total_score: Total vendor score
194 |             emissions_reduction: Emissions reduction percentage
195 |             
196 |         Returns:
197 |             Recommendation level string
198 |         """
199 |         # Hydrogen fleets are always highly recommended
200 |         if fleet_type == "hydrogen":
201 |             return "highly_recommended"
202 |         
203 |         # Electric with high emissions reduction
204 |         if fleet_type == "electric" and emissions_reduction > 85:
205 |             return "highly_recommended"
206 |         
207 |         # High score and good emissions reduction
208 |         if total_score > 200 and emissions_reduction > 70:
209 |             return "recommended"
210 |         
211 |         # Acceptable alternatives
212 |         if total_score > 100 and emissions_reduction > 50:
213 |             return "acceptable"
214 |         
215 |         # Default
216 |         return "acceptable"
217 |     
218 |     def get_top_recommendations(
219 |         self,
220 |         scored_vendors: List[VendorScore],
221 |         limit: Optional[int] = None,
222 |     ) -> List[VendorScore]:
223 |         """
224 |         Get top vendor recommendations.
225 |         
226 |         Args:
227 |             scored_vendors: List of scored vendors
228 |             limit: Maximum number of recommendations (uses config default if not provided)
229 |             
230 |         Returns:
231 |             List of top recommended vendors
232 |         """
233 |         if limit is None:
234 |             limit = self.config.top_recommendations
235 |         
236 |         return scored_vendors[:limit]
237 |     
238 |     def get_hydrogen_vendors(self, scored_vendors: List[VendorScore]) -> List[VendorScore]:
239 |         """
240 |         Get all hydrogen-fueled vendors.
241 |         
242 |         Args:
243 |             scored_vendors: List of scored vendors
244 |             
245 |         Returns:
246 |             List of hydrogen vendors
247 |         """
248 |         return [v for v in scored_vendors if v.fleet_type == "hydrogen"]
249 |     
250 |     def get_eco_friendly_vendors(
251 |         self,
252 |         scored_vendors: List[VendorScore],
253 |         min_eco_rating: Optional[float] = None,
254 |     ) -> List[VendorScore]:
255 |         """
256 |         Get eco-friendly vendors (hydrogen and electric with high ratings).
257 |         
258 |         Args:
259 |             scored_vendors: List of scored vendors
260 |             min_eco_rating: Minimum eco rating (uses config default if not provided)
261 |             
262 |         Returns:
263 |             List of eco-friendly vendors
264 |         """
265 |         if min_eco_rating is None:
266 |             min_eco_rating = self.config.min_eco_rating
267 |         
268 |         return [
269 |             v for v in scored_vendors
270 |             if v.fleet_type in ["hydrogen", "electric"] and v.eco_rating >= min_eco_rating
271 |         ]
272 |     
273 |     def get_scoring_summary(self, scored_vendors: List[VendorScore]) -> Dict[str, Any]:
274 |         """
275 |         Generate summary of scoring results.
276 |         
277 |         Args:
278 |             scored_vendors: List of scored vendors
279 |             
280 |         Returns:
281 |             Summary dictionary
282 |         """
283 |         if not scored_vendors:
284 |             return {
285 |                 "total_vendors": 0,
286 |                 "hydrogen_vendors": 0,
287 |                 "electric_vendors": 0,
288 |                 "highly_recommended": 0,
289 |             }
290 |         
291 |         # Count by fleet type
292 |         fleet_counts = {}
293 |         for vendor in scored_vendors:
294 |             fleet_type = vendor.fleet_type
295 |             fleet_counts[fleet_type] = fleet_counts.get(fleet_type, 0) + 1
296 |         
297 |         # Count by recommendation level
298 |         recommendation_counts = {
299 |             "highly_recommended": 0,
300 |             "recommended": 0,
301 |             "acceptable": 0,
302 |         }
303 |         for vendor in scored_vendors:
304 |             level = vendor.recommendation_level
305 |             recommendation_counts[level] = recommendation_counts.get(level, 0) + 1
306 |         
307 |         # Get top vendor
308 |         top_vendor = scored_vendors[0] if scored_vendors else None
309 |         
310 |         # Calculate average scores
311 |         avg_total_score = sum(v.total_score for v in scored_vendors) / len(scored_vendors)
312 |         avg_emissions_reduction = sum(v.emissions_reduction_percent for v in scored_vendors) / len(scored_vendors)
313 |         
314 |         return {
315 |             "total_vendors": len(scored_vendors),
316 |             "fleet_type_counts": fleet_counts,
317 |             "recommendation_counts": recommendation_counts,
318 |             "top_vendor": {
319 |                 "id": top_vendor.vendor_id,
320 |                 "name": top_vendor.vendor_name,
321 |                 "fleet_type": top_vendor.fleet_type,
322 |                 "score": top_vendor.total_score,
323 |                 "emissions_reduction": top_vendor.emissions_reduction_percent,
324 |             } if top_vendor else None,
325 |             "average_total_score": round(avg_total_score, 2),
326 |             "average_emissions_reduction": round(avg_emissions_reduction, 2),
327 |             "hydrogen_vendors": fleet_counts.get("hydrogen", 0),
328 |             "electric_vendors": fleet_counts.get("electric", 0),
329 |             "highly_recommended_count": recommendation_counts["highly_recommended"],
330 |         }
331 |     
332 |     def filter_by_criteria(
333 |         self,
334 |         scored_vendors: List[VendorScore],
335 |         min_score: Optional[float] = None,
336 |         min_emissions_reduction: Optional[float] = None,
337 |         fleet_types: Optional[List[str]] = None,
338 |         recommendation_levels: Optional[List[str]] = None,
339 |     ) -> List[VendorScore]:
340 |         """
341 |         Filter vendors by various criteria.
342 |         
343 |         Args:
344 |             scored_vendors: List of scored vendors
345 |             min_score: Minimum total score
346 |             min_emissions_reduction: Minimum emissions reduction percentage
347 |             fleet_types: List of acceptable fleet types
348 |             recommendation_levels: List of acceptable recommendation levels
349 |             
350 |         Returns:
351 |             Filtered list of vendors
352 |         """
353 |         filtered = scored_vendors
354 |         
355 |         if min_score is not None:
356 |             filtered = [v for v in filtered if v.total_score >= min_score]
357 |         
358 |         if min_emissions_reduction is not None:
359 |             filtered = [v for v in filtered if v.emissions_reduction_percent >= min_emissions_reduction]
360 |         
361 |         if fleet_types:
362 |             filtered = [v for v in filtered if v.fleet_type in fleet_types]
363 |         
364 |         if recommendation_levels:
365 |             filtered = [v for v in filtered if v.recommendation_level in recommendation_levels]
366 |         
367 |         return filtered
368 | 
369 | 
370 | # Global prioritizer instance
371 | fleet_prioritizer = FleetPrioritizer()
372 | 
373 | 
374 | # Made with Bob
</content>
</file>
<file><path>apps/backend/src/agents/monitor/weather_monitor.py</path>
<content lines="1-347">
  1 | """
  2 | Weather monitoring module for the Monitor Agent.
  3 | """
  4 | 
  5 | from typing import Dict, Any, List, Optional
  6 | from datetime import datetime, timedelta
  7 | import asyncio
  8 | 
  9 | from src.services.weather_service import WeatherService
 10 | from src.models.schemas import WeatherData
 11 | from src.utils.logger import get_logger
 12 | from .config import MonitorConfig
 13 | 
 14 | logger = get_logger(__name__)
 15 | 
 16 | 
 17 | class WeatherAlert(Dict[str, Any]):
 18 |     """Weather alert data structure."""
 19 |     
 20 |     def __init__(
 21 |         self,
 22 |         location: str,
 23 |         severity: str,
 24 |         alert_type: str,
 25 |         message: str,
 26 |         weather_data: WeatherData,
 27 |         timestamp: Optional[datetime] = None,
 28 |     ):
 29 |         """Initialize weather alert."""
 30 |         super().__init__(
 31 |             location=location,
 32 |             severity=severity,
 33 |             alert_type=alert_type,
 34 |             message=message,
 35 |             weather_data=weather_data.dict(),
 36 |             timestamp=timestamp or datetime.utcnow(),
 37 |         )
 38 | 
 39 | 
 40 | class WeatherMonitor:
 41 |     """Weather monitoring service for detecting severe weather conditions."""
 42 | 
 43 |     def __init__(self, config: Optional[MonitorConfig] = None):
 44 |         """
 45 |         Initialize weather monitor.
 46 |         
 47 |         Args:
 48 |             config: Monitor configuration (uses default if not provided)
 49 |         """
 50 |         self.config = config or MonitorConfig()
 51 |         self.weather_service = WeatherService()
 52 |         self._cache: Dict[str, Dict[str, Any]] = {}
 53 |         self._alert_history: Dict[str, datetime] = {}
 54 |         self._initialized = False
 55 | 
 56 |     async def initialize(self) -> None:
 57 |         """Initialize weather service."""
 58 |         if not self._initialized:
 59 |             await self.weather_service.initialize()
 60 |             self._initialized = True
 61 |             logger.info("Weather monitor initialized")
 62 | 
 63 |     async def close(self) -> None:
 64 |         """Close weather service and cleanup."""
 65 |         await self.weather_service.close()
 66 |         self._initialized = False
 67 |         logger.info("Weather monitor closed")
 68 | 
 69 |     def _is_cached(self, location: str) -> bool:
 70 |         """
 71 |         Check if weather data is cached and still valid.
 72 |         
 73 |         Args:
 74 |             location: Location to check
 75 |             
 76 |         Returns:
 77 |             True if cached data is valid
 78 |         """
 79 |         if location not in self._cache:
 80 |             return False
 81 |         
 82 |         cache_entry = self._cache[location]
 83 |         cache_time = cache_entry.get("timestamp")
 84 |         
 85 |         if not cache_time:
 86 |             return False
 87 |         
 88 |         age = (datetime.utcnow() - cache_time).total_seconds()
 89 |         return age < self.config.cache_duration
 90 | 
 91 |     def _get_cached_data(self, location: str) -> Optional[WeatherData]:
 92 |         """
 93 |         Get cached weather data.
 94 |         
 95 |         Args:
 96 |             location: Location to get data for
 97 |             
 98 |         Returns:
 99 |             Cached weather data or None
100 |         """
101 |         if self._is_cached(location):
102 |             return self._cache[location]["data"]
103 |         return None
104 | 
105 |     def _cache_data(self, location: str, data: WeatherData) -> None:
106 |         """
107 |         Cache weather data.
108 |         
109 |         Args:
110 |             location: Location to cache data for
111 |             data: Weather data to cache
112 |         """
113 |         self._cache[location] = {
114 |             "data": data,
115 |             "timestamp": datetime.utcnow(),
116 |         }
117 | 
118 |     def _is_severe_weather(self, weather_data: WeatherData) -> tuple[bool, List[str]]:
119 |         """
120 |         Check if weather conditions are severe.
121 |         
122 |         Args:
123 |             weather_data: Weather data to check
124 |             
125 |         Returns:
126 |             Tuple of (is_severe, list of reasons)
127 |         """
128 |         reasons = []
129 |         
130 |         # Check wind speed
131 |         if weather_data.wind_speed >= self.config.severe_wind_speed_threshold:
132 |             reasons.append(
133 |                 f"High wind speed: {weather_data.wind_speed:.1f} m/s "
134 |                 f"(threshold: {self.config.severe_wind_speed_threshold} m/s)"
135 |             )
136 |         
137 |         # Check temperature extremes
138 |         if weather_data.temperature <= self.config.extreme_temperature_low:
139 |             reasons.append(
140 |                 f"Extreme low temperature: {weather_data.temperature:.1f}°C "
141 |                 f"(threshold: {self.config.extreme_temperature_low}°C)"
142 |             )
143 |         elif weather_data.temperature >= self.config.extreme_temperature_high:
144 |             reasons.append(
145 |                 f"Extreme high temperature: {weather_data.temperature:.1f}°C "
146 |                 f"(threshold: {self.config.extreme_temperature_high}°C)"
147 |             )
148 |         
149 |         # Check humidity
150 |         if weather_data.humidity >= self.config.severe_humidity_threshold:
151 |             reasons.append(
152 |                 f"High humidity: {weather_data.humidity:.1f}% "
153 |                 f"(threshold: {self.config.severe_humidity_threshold}%)"
154 |             )
155 |         
156 |         # Check weather description for severe keywords
157 |         description_lower = weather_data.description.lower()
158 |         for keyword in self.config.severe_weather_keywords:
159 |             if keyword in description_lower:
160 |                 reasons.append(f"Severe weather condition detected: {weather_data.description}")
161 |                 break
162 |         
163 |         return len(reasons) > 0, reasons
164 | 
165 |     def _can_send_alert(self, location: str) -> bool:
166 |         """
167 |         Check if an alert can be sent for a location (respects cooldown).
168 |         
169 |         Args:
170 |             location: Location to check
171 |             
172 |         Returns:
173 |             True if alert can be sent
174 |         """
175 |         if location not in self._alert_history:
176 |             return True
177 |         
178 |         last_alert = self._alert_history[location]
179 |         time_since_alert = (datetime.utcnow() - last_alert).total_seconds()
180 |         
181 |         return time_since_alert >= self.config.alert_cooldown
182 | 
183 |     def _record_alert(self, location: str) -> None:
184 |         """
185 |         Record that an alert was sent for a location.
186 |         
187 |         Args:
188 |             location: Location to record alert for
189 |         """
190 |         self._alert_history[location] = datetime.utcnow()
191 | 
192 |     async def check_location(self, location: str) -> Optional[WeatherAlert]:
193 |         """
194 |         Check weather conditions for a single location.
195 |         
196 |         Args:
197 |             location: Location to check
198 |             
199 |         Returns:
200 |             WeatherAlert if severe weather detected, None otherwise
201 |         """
202 |         try:
203 |             # Check cache first
204 |             cached_data = self._get_cached_data(location)
205 |             if cached_data:
206 |                 weather_data = cached_data
207 |                 logger.debug(f"Using cached weather data for {location}")
208 |             else:
209 |                 # Fetch fresh data
210 |                 weather_data = await self.weather_service.get_weather(location)
211 |                 self._cache_data(location, weather_data)
212 |                 logger.info(f"Fetched weather data for {location}")
213 |             
214 |             # Check for severe weather
215 |             is_severe, reasons = self._is_severe_weather(weather_data)
216 |             
217 |             if is_severe:
218 |                 # Check if we can send an alert (cooldown)
219 |                 if not self._can_send_alert(location):
220 |                     logger.debug(
221 |                         f"Severe weather detected at {location} but alert is in cooldown"
222 |                     )
223 |                     return None
224 |                 
225 |                 # Create alert
226 |                 alert = WeatherAlert(
227 |                     location=location,
228 |                     severity="high" if len(reasons) > 2 else "medium",
229 |                     alert_type="severe_weather",
230 |                     message=f"Severe weather detected at {location}: {'; '.join(reasons)}",
231 |                     weather_data=weather_data,
232 |                 )
233 |                 
234 |                 self._record_alert(location)
235 |                 logger.warning(f"Severe weather alert for {location}: {reasons}")
236 |                 
237 |                 return alert
238 |             
239 |             logger.debug(f"Normal weather conditions at {location}")
240 |             return None
241 |             
242 |         except Exception as e:
243 |             logger.error(f"Error checking weather for {location}: {e}")
244 |             return None
245 | 
246 |     async def check_all_locations(
247 |         self,
248 |         locations: Optional[List[str]] = None,
249 |     ) -> List[WeatherAlert]:
250 |         """
251 |         Check weather conditions for multiple locations.
252 |         
253 |         Args:
254 |             locations: List of locations to check (uses config default if not provided)
255 |             
256 |         Returns:
257 |             List of weather alerts for locations with severe weather
258 |         """
259 |         if not self._initialized:
260 |             await self.initialize()
261 |         
262 |         locations = locations or self.config.monitored_locations
263 |         alerts = []
264 |         
265 |         # Check locations with rate limiting
266 |         for location in locations:
267 |             alert = await self.check_location(location)
268 |             if alert:
269 |                 alerts.append(alert)
270 |             
271 |             # Small delay to avoid rate limiting
272 |             await asyncio.sleep(0.5)
273 |         
274 |         if alerts:
275 |             logger.info(f"Found {len(alerts)} severe weather alerts")
276 |         else:
277 |             logger.info("No severe weather detected at monitored locations")
278 |         
279 |         return alerts
280 | 
281 |     async def get_location_forecast(
282 |         self,
283 |         location: str,
284 |         days: int = 3,
285 |     ) -> Dict[str, Any]:
286 |         """
287 |         Get weather forecast for a location.
288 |         
289 |         Args:
290 |             location: Location to get forecast for
291 |             days: Number of days for forecast
292 |             
293 |         Returns:
294 |             Forecast data
295 |         """
296 |         try:
297 |             if not self._initialized:
298 |                 await self.initialize()
299 |             
300 |             forecast = await self.weather_service.get_forecast(location, days=days)
301 |             logger.info(f"Retrieved {days}-day forecast for {location}")
302 |             return forecast
303 |             
304 |         except Exception as e:
305 |             logger.error(f"Error getting forecast for {location}: {e}")
306 |             raise
307 | 
308 |     def get_cache_stats(self) -> Dict[str, Any]:
309 |         """
310 |         Get cache statistics.
311 |         
312 |         Returns:
313 |             Dictionary with cache statistics
314 |         """
315 |         valid_entries = sum(1 for loc in self._cache if self._is_cached(loc))
316 |         
317 |         return {
318 |             "total_entries": len(self._cache),
319 |             "valid_entries": valid_entries,
320 |             "expired_entries": len(self._cache) - valid_entries,
321 |             "cache_duration_seconds": self.config.cache_duration,
322 |         }
323 | 
324 |     def clear_cache(self) -> None:
325 |         """Clear the weather data cache."""
326 |         self._cache.clear()
327 |         logger.info("Weather data cache cleared")
328 | 
329 |     def clear_alert_history(self) -> None:
330 |         """Clear the alert history."""
331 |         self._alert_history.clear()
332 |         logger.info("Alert history cleared")
333 | 
334 |     def get_alert_history(self) -> Dict[str, str]:
335 |         """
336 |         Get alert history.
337 |         
338 |         Returns:
339 |             Dictionary mapping locations to last alert timestamps
340 |         """
341 |         return {
342 |             location: timestamp.isoformat()
343 |             for location, timestamp in self._alert_history.items()
344 |         }
345 | 
346 | 
347 | # Made with Bob
</content>
</file>
<file><path>apps/backend/src/config/settings.py</path>
<content lines="1-139">
  1 | """
  2 | Application configuration using pydantic-settings.
  3 | """
  4 | 
  5 | from typing import List, Optional
  6 | from pydantic import Field, validator
  7 | from pydantic_settings import BaseSettings, SettingsConfigDict
  8 | 
  9 | 
 10 | class Settings(BaseSettings):
 11 |     """Application settings loaded from environment variables."""
 12 | 
 13 |     model_config = SettingsConfigDict(
 14 |         env_file=".env",
 15 |         env_file_encoding="utf-8",
 16 |         case_sensitive=False,
 17 |         extra="ignore",
 18 |     )
 19 | 
 20 |     # Application Settings
 21 |     app_name: str = Field(default="Eco-Shift Backend", description="Application name")
 22 |     app_version: str = Field(default="0.1.0", description="Application version")
 23 |     environment: str = Field(default="development", description="Environment (development/production)")
 24 |     debug: bool = Field(default=True, description="Debug mode")
 25 |     log_level: str = Field(default="INFO", description="Logging level")
 26 | 
 27 |     # Server Configuration
 28 |     host: str = Field(default="0.0.0.0", description="Server host")
 29 |     port: int = Field(default=8000, description="Server port")
 30 |     reload: bool = Field(default=True, description="Auto-reload on code changes")
 31 | 
 32 |     # CORS Settings
 33 |     cors_origins: str = Field(
 34 |         default="http://localhost:3000,http://localhost:3001",
 35 |         description="Allowed CORS origins (comma-separated)",
 36 |     )
 37 |     cors_allow_credentials: bool = Field(default=True, description="Allow credentials")
 38 |     cors_allow_methods: str = Field(default="*", description="Allowed HTTP methods")
 39 |     cors_allow_headers: str = Field(default="*", description="Allowed HTTP headers")
 40 | 
 41 |     # IBM watsonx.ai Configuration
 42 |     watsonx_api_key: Optional[str] = Field(default=None, description="watsonx.ai API key")
 43 |     watsonx_project_id: Optional[str] = Field(default=None, description="watsonx.ai project ID")
 44 |     watsonx_url: str = Field(
 45 |         default="https://us-south.ml.cloud.ibm.com",
 46 |         description="watsonx.ai service URL",
 47 |     )
 48 |     watsonx_model_id: str = Field(
 49 |         default="ibm/granite-13b-chat-v2",
 50 |         description="Default model ID",
 51 |     )
 52 | 
 53 |     # IBM Cloud Configuration
 54 |     ibm_cloud_api_key: Optional[str] = Field(default=None, description="IBM Cloud API key")
 55 |     ibm_cloud_url: str = Field(
 56 |         default="https://us-south.ml.cloud.ibm.com",
 57 |         description="IBM Cloud URL",
 58 |     )
 59 | 
 60 |     # OpenWeather API Configuration
 61 |     openweather_api_key: Optional[str] = Field(default=None, description="OpenWeather API key")
 62 |     openweather_base_url: str = Field(
 63 |         default="https://api.openweathermap.org/data/2.5",
 64 |         description="OpenWeather API base URL",
 65 |     )
 66 | 
 67 |     # Agent Configuration
 68 |     agent_monitor_enabled: bool = Field(default=True, description="Enable monitoring agent")
 69 |     agent_auditor_enabled: bool = Field(default=True, description="Enable auditor agent")
 70 |     agent_orchestrator_enabled: bool = Field(default=True, description="Enable orchestrator agent")
 71 |     agent_polling_interval: int = Field(default=300, description="Agent polling interval (seconds)")
 72 | 
 73 |     # Security
 74 |     secret_key: str = Field(
 75 |         default="change_this_secret_key_in_production",
 76 |         description="Secret key for JWT",
 77 |     )
 78 |     algorithm: str = Field(default="HS256", description="JWT algorithm")
 79 |     access_token_expire_minutes: int = Field(
 80 |         default=30,
 81 |         description="Access token expiration time",
 82 |     )
 83 | 
 84 |     # Rate Limiting
 85 |     rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
 86 |     rate_limit_per_minute: int = Field(default=60, description="Requests per minute limit")
 87 | 
 88 |     # External APIs
 89 |     carbon_intensity_api_url: str = Field(
 90 |         default="https://api.carbonintensity.org.uk",
 91 |         description="Carbon Intensity API URL",
 92 |     )
 93 |     electricity_maps_api_key: Optional[str] = Field(
 94 |         default=None,
 95 |         description="Electricity Maps API key",
 96 |     )
 97 | 
 98 |     # Monitoring and Logging
 99 |     sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
100 |     enable_metrics: bool = Field(default=True, description="Enable metrics collection")
101 |     metrics_port: int = Field(default=9090, description="Metrics server port")
102 | 
103 |     # Feature Flags
104 |     enable_weather_integration: bool = Field(default=True, description="Enable weather integration")
105 |     enable_vendor_recommendations: bool = Field(
106 |         default=True,
107 |         description="Enable vendor recommendations",
108 |     )
109 |     enable_emissions_tracking: bool = Field(
110 |         default=True,
111 |         description="Enable emissions tracking",
112 |     )
113 |     enable_real_time_monitoring: bool = Field(
114 |         default=True,
115 |         description="Enable real-time monitoring",
116 |     )
117 | 
118 |     @validator("cors_origins", pre=True)
119 |     def parse_cors_origins(cls, v: str) -> List[str]:
120 |         """Parse comma-separated CORS origins into a list."""
121 |         if isinstance(v, str):
122 |             return [origin.strip() for origin in v.split(",")]
123 |         return v
124 | 
125 |     @property
126 |     def is_production(self) -> bool:
127 |         """Check if running in production environment."""
128 |         return self.environment.lower() == "production"
129 | 
130 |     @property
131 |     def is_development(self) -> bool:
132 |         """Check if running in development environment."""
133 |         return self.environment.lower() == "development"
134 | 
135 | 
136 | # Global settings instance
137 | settings = Settings()
138 | 
139 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
README.md

# VSCode Open Tabs
.gitignore,AGENTS.md,docs/ARCHITECTURE.md,docs/QUICK_START.md,apps/frontend/package.json,apps/frontend/tsconfig.json,apps/frontend/tailwind.config.ts,apps/frontend/next.config.js,apps/frontend/.eslintrc.json,apps/frontend/postcss.config.js,apps/frontend/src/styles/globals.css,apps/frontend/src/app/layout.tsx,apps/frontend/src/app/page.tsx,apps/frontend/src/lib/api.ts,apps/frontend/.env.example,apps/frontend/README.md,apps/frontend/src/lib/utils.ts,apps/frontend/src/lib/animations.ts,apps/frontend/.gitignore,apps/frontend/.prettierrc

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T07:21:54.299Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I have comprehensive information about the project. Let me write the updated AGENTS.md file with non-obvious, project-specific details.

<write_to_file>
<path>AGENTS.md</path>
<content>
# AGENTS.md

This file provides guidance to AI agents when working with the Eco-Shift codebase. It focuses on non-obvious architectural decisions, project-specific patterns, and critical gotchas.

## Project Overview

**Eco-Shift** is a multi-agent logistics optimization platform that uses IBM watsonx.ai and real-time weather data to reduce carbon emissions in supply chains. The system employs three coordinating agents (Monitor, Auditor, Orchestrator) that communicate via a custom message bus.

**Key Technologies:**
- Frontend: Next.js 14.2.3 (App Router), React 18.3.1, TypeScript 5.4.5, Tailwind CSS 3.4.3, GSAP 3.12.5
- Backend: Python 3.10+, FastAPI 0.109.0+, Pydantic 2.5.3+, IBM watsonx.ai 0.2.6+
- Agent Framework: Custom multi-agent system with pub/sub message bus
- APIs: OpenWeather API, IBM watsonx.ai (Granite models)

## Build, Test, and Lint Commands

### Root-Level Commands (from workspace root)
```bash
# Development
npm run dev                    # Start both frontend and backend concurrently
npm run dev:frontend           # Frontend only (port 3000)
npm run dev:backend            # Backend only (port 8000)

# Building
npm run build                  # Build both apps
npm run build:frontend         # Next.js production build
npm run build:backend          # Install Python dependencies

# Testing
npm run test                   # Run all tests (frontend + backend)
npm run test:frontend          # Jest tests for frontend
npm run test:backend           # pytest for backend
npm run test:watch             # Frontend tests in watch mode

# Code Quality
npm run lint                   # Lint both apps
npm run lint:frontend          # ESLint for frontend
npm run lint:backend           # flake8 for backend (src/ and tests/)
npm run format                 # Format both apps
npm run format:frontend        # Prettier for frontend
npm run format:backend         # Black for backend
npm run type-check             # TypeScript type checking

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

### Frontend Commands (from `apps/frontend/`)
```bash
npm run dev                    # Development server (port 3000)
npm run build                  # Production build
npm run start                  # Start production server
npm run lint                   # ESLint
npm run type-check             # TypeScript checking
npm run format                 # Prettier formatting
```

### Backend Commands (from `apps/backend/`)
```bash
# Development
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Testing
pytest                         # Run all tests
pytest --cov=src              # With coverage
pytest -v                      # Verbose output
pytest tests/unit/            # Unit tests only
pytest tests/integration/     # Integration tests only

# Code Quality
flake8 src/ tests/            # Linting
black src/ tests/             # Formatting
isort src/ tests/             # Import sorting
mypy src/                     # Type checking
```

## Code Style Guidelines

### TypeScript/React (Frontend)
- **Line length:** 100 characters (Prettier default)
- **Import order:** React imports → Third-party → Local components → Utils → Types
- **Component structure:** Functional components with TypeScript interfaces
- **File naming:** `kebab-case.tsx` for components, `camelCase.ts` for utilities
- **Type definitions:** Use interfaces for props, types for unions/intersections
- **Async operations:** Use React hooks (useState, useEffect) with proper cleanup

### Python (Backend)
- **Line length:** 100 characters (Black configuration)
- **Import order:** Standard library → Third-party → Local imports (enforced by isort with Black profile)
- **Type hints:** Required for all function signatures (mypy strict mode)
- **Docstrings:** Google-style docstrings for all public functions/classes
- **Async/await:** Use async/await for all I/O operations
- **Error handling:** Use custom exceptions, log with structured logging

### Naming Conventions
- **Python:** `snake_case` for functions/variables, `PascalCase` for classes
- **TypeScript:** `camelCase` for functions/variables, `PascalCase` for components/types
- **Constants:** `UPPER_SNAKE_CASE` in both languages
- **Private methods:** Prefix with `_` in Python

## Architecture-Specific Rules (NON-OBVIOUS)

### Agent Communication via Message Bus
**Critical:** Agents communicate through `apps/backend/src/agents/orchestrator/message_bus.py`, NOT direct function calls.

**Message Bus Patterns:**
- **Publish-Subscribe:** Use `publish()` for broadcasting to all subscribers of a message type
- **Direct Send:** Use `send()` for targeted messages to specific agents (requires `recipient` field)
- **Request-Response:** Use `request()` with `correlation_id` for synchronous-style communication
- **Priority Queuing:** Messages use negative priority values internally (-4 to -1) for correct ordering

**Message TTL:** Default 3600 seconds. Messages expire and are cleaned up every 60 seconds. Set custom TTL for time-sensitive operations.

**Queue Size:** Max 1000 messages per agent queue. Exceeding this drops messages with error log.

### Monitor and Auditor Agent Interaction
**Workflow Pattern:**
1. Monitor Agent polls weather every 300 seconds (configurable via `agent_polling_interval`)
2. Severe weather triggers `MessageType.WEATHER_ALERT` with `MessagePriority.HIGH`
3. Orchestrator receives alert and publishes `MessageType.AUDIT_REQUEST` to Auditor
4. Auditor processes request and publishes `MessageType.AUDIT_RESULT`
5. Orchestrator aggregates results for frontend API

**Weather Cache:** Monitor Agent caches weather data for 300 seconds (5 minutes) to avoid API rate limits. Cache is location-specific and checked before each API call.

**Alert Cooldown:** Weather alerts have 1800-second (30-minute) cooldown per location to prevent spam. Tracked in `_alert_history` dict.

### Orchestrator Workflow Patterns
**Lifecycle Management:**
- Agents are NOT automatically started on backend startup
- Must explicitly call `orchestrator.start_agents()` or use CLI commands
- Each agent runs in its own asyncio task
- Graceful shutdown requires `orchestrator.stop_agents()` to cancel tasks

**Error Handling:**
- Failed agent tasks are logged but don't crash the orchestrator
- Use `MessageType.ERROR` for agent-level errors
- Orchestrator maintains agent status in memory (not persisted)

### API Integration Between Frontend and Backend
**Proxy Pattern:** Frontend uses Next.js API routes (`apps/frontend/src/app/api/`) as proxies to backend. This hides backend URL and enables server-side auth.

**Base URL Configuration:**
- Frontend: `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`)
- Backend: `cors_origins` setting (default: `http://localhost:3000,http://localhost:3001`)

**API Client:** `apps/frontend/src/lib/api.ts` uses axios with 30-second timeout. All requests include error handling with structured error objects.

### Environment Variable Requirements
**Critical Dependencies:**
- `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` - Required for Auditor Agent AI recommendations
- `OPENWEATHER_API_KEY` - Required for Monitor Agent weather data
- Backend fails gracefully if keys missing, but agents won't function

**Optional but Recommended:**
- `WATSONX_MODEL_ID` - Defaults to `ibm/granite-13b-chat-v2` if not set
- `LOG_LEVEL` - Defaults to `INFO`, use `DEBUG` for development

**CORS Configuration:** `cors_origins` must include frontend URL or requests will fail. Comma-separated string, not array.

### Configuration Dependencies
**Settings Cascade:**
1. Environment variables (`.env` files)
2. `apps/backend/src/config/settings.py` defaults
3. Agent-specific configs in `apps/backend/src/agents/*/config.py`

**Agent Configs:** Each agent has its own config class (e.g., `MonitorConfig`, `AuditorConfig`) that can override global settings. These are NOT loaded from environment variables directly.

## Agent System Details (NON-OBVIOUS)

### Agent Lifecycle Management
**Initialization Order:**
1. Message bus must be initialized first: `await initialize_message_bus()`
2. Create agent instances (they auto-subscribe to message bus)
3. Start agents: `await agent.start()`
4. Agents run in background asyncio tasks until stopped

**Shutdown Order:**
1. Stop agents: `await agent.stop()`
2. Shutdown message bus: `await shutdown_message_bus()`
3. Close external service connections (weather service, watsonx client)

### Message Bus Usage Patterns
**Subscription Pattern:**
```python
# Subscribe to message type
message_bus.subscribe("weather_alert", callback_function)

# Callback receives Message object
async def callback_function(message: Message):
    payload = message.payload
    # Process message
```

**Publishing Pattern:**
```python
# Create message
message = Message(
    type=MessageType.WEATHER_ALERT,
    sender="monitor_agent",
    payload={"location": "New York", "severity": "high"},
    priority=MessagePriority.HIGH,
    ttl=1800  # 30 minutes
)

# Publish to all subscribers
await message_bus.publish(message)
```

**Request-Response Pattern:**
```python
# Send request and wait for response
request = Message(
    type=MessageType.AUDIT_REQUEST,
    sender="orchestrator",
    recipient="auditor_agent",
    payload={"vendors": vendor_list}
)

response = await message_bus.request(request, timeout=30.0)
result = response.payload
```

### How to Add New Agents
1. Create directory in `apps/backend/src/agents/new_agent/`
2. Extend `BaseAgent` class from `apps/backend/src/agents/base_agent.py`
3. Implement `start()`, `stop()`, and main logic methods
4. Create agent-specific config in `config.py`
5. Register with orchestrator in `apps/backend/src/agents/orchestrator/orchestrator_agent.py`
6. Add message type to `MessageType` enum if needed
7. Subscribe to relevant message types in agent's `start()` method

### Agent Configuration Patterns
**Config Classes:** Use Pydantic BaseModel for type safety and validation
```python
class NewAgentConfig(BaseModel):
    enabled: bool = True
    polling_interval: int = 300
    custom_setting: str = "default"
```

**Loading Configs:** Configs are instantiated at agent creation, not loaded from env vars. Override defaults by passing config instance to agent constructor.

### Error Handling in Agent Workflows
**Agent-Level Errors:**
- Catch exceptions in agent methods
- Log with structured logging: `logger.error(f"Error: {e}", exc_info=True)`
- Publish `MessageType.ERROR` message to notify orchestrator
- Don't let exceptions crash the agent task

**Message Bus Errors:**
- Subscriber callback exceptions are caught and logged by message bus
- Failed message delivery logs error but doesn't raise exception
- Expired messages are silently dropped with debug log

## Development Workflow

### Starting the Full Stack
```bash
# Option 1: Using npm scripts (recommended)
npm run dev

# Option 2: Manual start
# Terminal 1 - Backend
cd apps/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd apps/frontend
npm run dev

# Option 3: Docker
npm run docker:up
```

### Testing Individual Agents
```bash
# From apps/backend/
python -m pytest tests/unit/test_agents.py -v

# Test specific agent
python -m pytest tests/unit/test_agents.py::TestMonitorAgent -v

# Run agent directly (for debugging)
python -m src.agents.monitor.monitor_agent
```

### Debugging Agent Communication
**View Message History:**
```python
from src.agents.orchestrator.message_bus import get_message_bus

message_bus = get_message_bus()
history = message_bus.get_message_history(limit=50)
print(history)
```

**Check Message Bus Stats:**
```python
stats = message_bus.get_stats()
# Returns: subscribers, queue sizes, pending responses, history size
```

**Enable Debug Logging:**
Set `LOG_LEVEL=DEBUG` in `.env` to see detailed message bus activity.

### Common Development Tasks
**Add New API Endpoint:**
1. Create route in `apps/backend/src/api/` (e.g., `new_feature.py`)
2. Import and include router in `apps/backend/src/main.py`
3. Add Pydantic schemas in `apps/backend/src/models/schemas.py`
4. Update frontend API client in `apps/frontend/src/lib/api.ts`

**Add New Frontend Component:**
1. Create component in `apps/frontend/src/components/`
2. Use TypeScript interfaces for props
3. Import types from `apps/frontend/src/types/index.ts`
4. Use Tailwind CSS for styling
5. Add GSAP animations via `apps/frontend/src/lib/animations.ts`

## Critical Gotchas (NON-OBVIOUS)

### Hydrogen Fleet Prioritization (10x Multiplier)
**CRITICAL:** In `apps/backend/src/agents/auditor/fleet_prioritizer.py`, hydrogen fleets receive a **10x score multiplier** (line 124-126). This is intentional and central to the business logic.

```python
if fleet_type == "hydrogen":
    fleet_type_score *= 10.0  # 10x multiplier for hydrogen
```

This means hydrogen fleets will almost always rank first unless they have catastrophically bad other metrics. Don't "fix" this - it's by design.

### Emissions Calculation Specifics
**Baseline Calculation:** Emissions reduction percentage is calculated against a diesel baseline (2.68 kg CO2e per liter). Found in `apps/backend/src/agents/auditor/emissions_calculator.py`.

**Fuel Type Factors:**
- Diesel: 2.68 kg CO2e/L
- Petrol: 2.31 kg CO2e/L
- Electric: 0.0 kg CO2e (direct emissions only)
- Hybrid: 1.34 kg CO2e/L (50% reduction)
- Hydrogen: 0.0 kg CO2e (direct emissions only)

**Scope 3 Emissions:** System calculates transportation emissions only. Does not include manufacturing, maintenance, or end-of-life emissions.

### Weather Polling Intervals and Caching
**Polling Interval:** Default 300 seconds (5 minutes) set in `settings.py` as `agent_polling_interval`.

**Cache Duration:** Weather data cached for 300 seconds (5 minutes) in `WeatherMonitor._cache`. This is SEPARATE from polling interval.

**Race Condition:** If multiple requests hit the same location within cache window, only the first fetches from API. Others use cached data. This is intentional to avoid rate limits.

**Cache Invalidation:** No automatic invalidation. Cache entries expire based on timestamp. Use `weather_monitor.clear_cache()` to force refresh.

### API Rate Limiting Considerations
**OpenWeather Free Tier:** 60 calls/minute, 1,000,000 calls/month. Monitor Agent adds 0.5-second delay between location checks to stay under limit.

**watsonx.ai Rate Limits:** Varies by plan. No built-in rate limiting in code. Implement retry logic with exponential backoff if needed.

**Message Bus Queue Full:** If agent queue exceeds 1000 messages, new messages are dropped with error log. This can happen if agent is slow or stopped. Monitor queue sizes via `get_stats()`.

### watsonx.ai Integration Requirements
**Model ID:** Default is `ibm/granite-13b-chat-v2` but can be overridden via `WATSONX_MODEL_ID` env var.

**Project ID Required:** `WATSONX_PROJECT_ID` is mandatory. Requests fail without it. No fallback.

**URL Configuration:** Default is `https://us-south.ml.cloud.ibm.com`. Change via `WATSONX_URL` for different regions.

**Async Operations:** watsonx service in `apps/backend/src/services/watsonx_service.py` uses synchronous IBM SDK. Wrap calls in `asyncio.to_thread()` for async compatibility.

**Token Limits:** Granite models have token limits. Long prompts may be truncated. Monitor response for truncation warnings.

### TypeScript Path Aliases
Frontend uses path aliases configured in `tsconfig.json`:
- `@/components/*` → `src/components/*`
- `@/lib/*` → `src/lib/*`
- `@/types/*` → `src/types/*`

These work in Next.js but may not work in test files without additional Jest configuration.

### Pydantic V2 Breaking Changes
Backend uses Pydantic V2 (2.5.3+). Key differences from V1:
- `.dict()` is now `.model_dump()`
- `.parse_obj()` is now `.model_validate()`
- Config is now `model_config` dict, not nested `Config` class
- Validators use `@field_validator` decorator, not `@validator`

### Message Bus Priority Queue Gotcha
Priority queue uses NEGATIVE priority values internally (line 301 in `message_bus.py`):
```python
priority = -message.priority.value  # Negative for correct ordering
```

This means `MessagePriority.CRITICAL` (value 4) becomes -4 in queue, ensuring it's processed first. Don't change this without understanding asyncio.PriorityQueue behavior.

### CORS Configuration Format
`cors_origins` in settings is a COMMA-SEPARATED STRING, not a list. The `@validator` converts it to a list at runtime (line 119 in `settings.py`). Don't pass a list directly to the Settings constructor.

### Agent Status Not Persisted
Agent status (running/stopped) is stored in memory only. Restarting the backend resets all agent states. Implement database persistence if needed for production.

---

**Last Updated:** 2026-05-02  
**Maintained By:** Eco-Shift Development Team
</content>
<line_count>485</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'AGENTS.md'] Result:
<file_write_result>
<path>AGENTS.md</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.gitignore,docs/ARCHITECTURE.md,docs/QUICK_START.md,apps/frontend/package.json,apps/frontend/tsconfig.json,apps/frontend/tailwind.config.ts,apps/frontend/next.config.js,apps/frontend/.eslintrc.json,apps/frontend/postcss.config.js,apps/frontend/src/styles/globals.css,apps/frontend/src/app/layout.tsx,apps/frontend/src/app/page.tsx,apps/frontend/src/lib/api.ts,apps/frontend/.env.example,apps/frontend/README.md,apps/frontend/src/lib/utils.ts,apps/frontend/src/lib/animations.ts,apps/frontend/.gitignore,apps/frontend/.prettierrc,apps/frontend/src/types/index.ts

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T07:23:25.844Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.19

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Successfully updated AGENTS.md with comprehensive project-specific information for the Eco-Shift project. The file now includes:

## Key Sections Added:

1. **Project Overview** - Multi-agent architecture with IBM watsonx.ai and OpenWeather API integration, including specific technology versions

2. **Build, Test, and Lint Commands** - Complete command reference for:
   - Root-level npm scripts (dev, build, test, lint, format, docker, agents)
   - Frontend-specific commands (Next.js)
   - Backend-specific commands (Python/FastAPI)

3. **Code Style Guidelines** - Language-specific conventions:
   - TypeScript/React: 100-char lines, import ordering, component patterns
   - Python: Black formatting, isort profiles, type hints, docstrings
   - Naming conventions for both languages

4. **Architecture-Specific Rules (NON-OBVIOUS)**:
   - Agent communication via message bus (NOT direct calls)
   - Message TTL (3600s default), queue size limits (1000 messages)
   - Weather cache (300s) and alert cooldown (1800s)
   - Orchestrator lifecycle management (agents not auto-started)
   - API proxy pattern through Next.js routes
   - Environment variable requirements and CORS configuration

5. **Agent System Details (NON-OBVIOUS)**:
   - Initialization order (message bus → agents → start)
   - Message bus patterns (pub/sub, request/response)
   - How to add new agents (7-step process)
   - Agent configuration patterns (Pydantic BaseModel)
   - Error handling strategies

6. **Development Workflow**:
   - Three ways to start the full stack
   - Testing individual agents
   - Debugging agent communication
   - Common development tasks

7. **Critical Gotchas (NON-OBVIOUS)**:
   - **Hydrogen fleet 10x multiplier** (line 124-126 in fleet_prioritizer.py) - INTENTIONAL
   - Emissions calculation specifics (diesel baseline: 2.68 kg CO2e/L)
   - Weather polling vs caching (both 300s but separate)
   - OpenWeather rate limits (0.5s delay between calls)
   - watsonx.ai requirements (PROJECT_ID mandatory)
   - TypeScript path aliases
   - Pydantic V2 breaking changes
   - Message bus priority queue uses negative values
   - CORS origins as comma-separated string
   - Agent status not persisted

The file follows the "non-obvious only" principle, focusing on project-specific patterns, counterintuitive design decisions, and critical implementation details that aren't evident from reading the code alone.
</result>
</attempt_completion>

