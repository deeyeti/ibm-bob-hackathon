# Eco-Shift Quick Start Guide

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