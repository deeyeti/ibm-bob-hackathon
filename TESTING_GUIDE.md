# CommandCenter Refactoring - Testing Guide

## Overview

This guide provides comprehensive testing instructions for the CommandCenter refactoring, which introduces origin/destination input, route visualization with Leaflet maps, and AI chatbot functionality.

**Last Updated:** 2026-05-03  
**Version:** 1.0.0

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Testing](#backend-testing)
3. [Frontend Testing](#frontend-testing)
4. [Integration Testing](#integration-testing)
5. [Feature-Specific Testing](#feature-specific-testing)
6. [Troubleshooting](#troubleshooting)
7. [Test Cases](#test-cases)

---

## Prerequisites

### Required Environment Variables

**Backend (.env in apps/backend/):**
```bash
WATSONX_API_KEY=your_watsonx_api_key
WATSONX_PROJECT_ID=your_project_id
OPENWEATHER_API_KEY=your_openweather_api_key
```

**Frontend (.env.local in apps/frontend/):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Required Dependencies

**Backend:**
- Python 3.10+
- All packages in `apps/backend/requirements.txt`

**Frontend:**
- Node.js 18+
- npm packages including:
  - leaflet ^1.9.4
  - react-leaflet ^4.2.1
  - @types/leaflet ^1.9.21

### Verify Installation

```bash
# Backend
cd apps/backend
python -m pip list | grep -E "fastapi|pydantic|ibm-watsonx-ai"

# Frontend
cd apps/frontend
npm list leaflet react-leaflet @types/leaflet
```

---

## Backend Testing

### 1. Syntax and Type Checking

```bash
cd apps/backend

# Check Python syntax
python -m py_compile src/api/chat.py
python -m py_compile src/api/orchestrator.py
python -m py_compile src/models/schemas.py

# Run flake8 linting
flake8 src/api/ src/models/

# Run mypy type checking
mypy src/api/ src/models/
```

**Expected Result:** No errors or warnings.

### 2. Start Backend Server

```bash
cd apps/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3. Verify API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-05-03T07:00:00.000000"
}
```

#### Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the benefits of hydrogen fleets?"
  }'
```

**Expected Response:**
```json
{
  "response": "Hydrogen fleets offer several key benefits...",
  "timestamp": "2026-05-03T07:00:00.000000"
}
```

#### Orchestrate Endpoint
```bash
curl -X POST http://localhost:8000/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Shanghai,CN",
    "destination": "Los Angeles,US"
  }'
```

**Expected Response:**
```json
{
  "workflow_id": "workflow_abc123",
  "status": "completed",
  "reroute_required": false,
  "weather_status": "Weather conditions are favorable",
  "route_details": {
    "distance": 9500.45,
    "eta": "9 days, 21 hours",
    "origin_coords": [31.2304, 121.4737],
    "destination_coords": [34.0522, -118.2437]
  },
  "timestamp": "2026-05-03T07:00:00.000000"
}
```

### 4. Backend API Documentation

Access interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Frontend Testing

### 1. TypeScript Type Checking

```bash
cd apps/frontend
npm run type-check
```

**Expected Output:**
```
> @eco-shift/frontend@0.1.0 type-check
> tsc --noEmit
```
(No errors should appear)

### 2. ESLint Checking

```bash
cd apps/frontend
npm run lint
```

**Expected Output:**
```
✔ No ESLint warnings or errors
```

### 3. Start Frontend Development Server

```bash
cd apps/frontend
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 14.2.3
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

### 4. Verify Frontend Build

```bash
cd apps/frontend
npm run build
```

**Expected Output:**
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages
✓ Finalizing page optimization
```

---

## Integration Testing

### Full Stack Testing Workflow

1. **Start Backend:**
   ```bash
   cd apps/backend
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend:**
   ```bash
   cd apps/frontend
   npm run dev
   ```

3. **Access Application:**
   Open browser to http://localhost:3000

4. **Verify CORS:**
   - Open browser DevTools (F12)
   - Check Console for CORS errors
   - Should see no errors related to cross-origin requests

---

## Feature-Specific Testing

### 1. Origin/Destination Input Workflow

**Test Steps:**

1. Navigate to http://localhost:3000
2. Locate the "Origin Port" input field
3. Enter: `Shanghai,CN`
4. Locate the "Destination Port" input field
5. Enter: `Los Angeles,US`
6. Click "Initiate Shift Order" button

**Expected Behavior:**
- Loading spinner appears
- After 2-5 seconds, Shift Order panel displays
- Route Details section shows:
  - Distance in kilometers
  - Estimated Time of Arrival (ETA)
  - Origin and destination coordinates
- Map updates with markers and route line

**Sample Test Data:**
```
Origin: Shanghai,CN → [31.2304, 121.4737]
Destination: Los Angeles,US → [34.0522, -118.2437]
Distance: ~9,500 km
ETA: ~9 days, 21 hours
```

### 2. Route Details Display

**Test Steps:**

1. Complete Origin/Destination input workflow
2. Observe the "Route Details" section

**Expected Display:**
- Distance in kilometers (e.g., "9,500.45 km")
- ETA in days and hours (e.g., "9 days, 21 hours")
- Origin coordinates displayed
- Destination coordinates displayed

**Verification:**
- All values should be numeric and properly formatted
- Coordinates should be in [latitude, longitude] format
- Distance should be reasonable for the route

### 3. Map Visualization

**Test Steps:**

1. Complete Origin/Destination input workflow
2. Scroll to the "Route Visualization" section
3. Observe the Leaflet map

**Expected Behavior:**
- Map loads with OpenStreetMap tiles
- Blue marker appears at origin location
- Red marker appears at destination location
- Polyline (route line) connects the two markers
- Map is centered between origin and destination
- Zoom level is appropriate to show both markers

**Interactive Testing:**
- Click and drag to pan the map
- Use mouse wheel to zoom in/out
- Click on markers to see popup (if implemented)

**Visual Verification:**
- Markers should be at correct geographic locations
- Route line should be visible and colored
- Map tiles should load without errors

### 4. AI Chatbot Functionality

**Test Steps:**

1. Complete Origin/Destination input workflow
2. Scroll to the "AI Assistant" section
3. Type a question in the chat input
4. Click "Send" or press Enter

**Sample Questions:**
```
1. "Why was this route selected?"
2. "What are the carbon emissions for this route?"
3. "How can we reduce emissions on this route?"
4. "What is the weather forecast for the destination?"
5. "Explain the benefits of hydrogen fleets"
```

**Expected Behavior:**
- Message appears in chat history with "user" role
- Loading indicator shows while waiting for response
- AI response appears with "assistant" role
- Response is relevant to the question
- Response references shift order data when applicable
- Timestamp is displayed for each message

**Context-Aware Testing:**
- Ask questions about the current route
- Verify AI references specific data (distance, ETA, etc.)
- Check that AI provides actionable recommendations

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Backend Won't Start

**Symptom:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
cd apps/backend
pip install -r requirements.txt
```

**Symptom:** `WATSONX_API_KEY not found`

**Solution:**
- Create `.env` file in `apps/backend/`
- Add required environment variables
- Restart backend server

#### 2. Frontend Build Errors

**Symptom:** `Cannot find module 'leaflet'`

**Solution:**
```bash
cd apps/frontend
npm install leaflet react-leaflet @types/leaflet
```

**Symptom:** TypeScript errors in CommandCenter.tsx

**Solution:**
```bash
cd apps/frontend
npm run type-check
# Fix any reported type errors
```

#### 3. Map Not Displaying

**Symptom:** Blank map area or "Map container not found"

**Solution:**
- Verify Leaflet CSS is imported in `layout.tsx`
- Check browser console for errors
- Ensure `react-leaflet` version is compatible with `leaflet`

**Symptom:** Map tiles not loading

**Solution:**
- Check internet connection
- Verify OpenStreetMap tile server is accessible
- Check browser console for CORS or network errors

#### 4. Chat Not Working

**Symptom:** "Failed to generate chat response"

**Solution:**
- Verify `WATSONX_API_KEY` is set correctly
- Check backend logs for detailed error messages
- Ensure watsonx.ai service is accessible

**Symptom:** Chat sends but no response

**Solution:**
- Check browser DevTools Network tab
- Verify `/api/chat` endpoint is being called
- Check for CORS errors
- Verify backend is running

#### 5. CORS Errors

**Symptom:** "Access-Control-Allow-Origin" errors in browser console

**Solution:**
- Verify `cors_origins` in backend settings includes frontend URL
- Default should be: `http://localhost:3000,http://localhost:3001`
- Restart backend after changing settings

#### 6. Route Details Not Showing

**Symptom:** Shift Order displays but no route details

**Solution:**
- Check backend response includes `route_details` field
- Verify coordinates are in correct format `[lat, lon]`
- Check browser console for JavaScript errors

---

## Test Cases

### Test Case 1: Basic Workflow

**Objective:** Verify complete origin-to-destination workflow

**Steps:**
1. Start backend and frontend
2. Navigate to http://localhost:3000
3. Enter origin: "Shanghai,CN"
4. Enter destination: "Los Angeles,US"
5. Click "Initiate Shift Order"

**Expected Results:**
- ✓ Shift Order panel appears
- ✓ Route details display with distance and ETA
- ✓ Map shows both markers and route line
- ✓ No errors in console

**Status:** [ ] Pass [ ] Fail

---

### Test Case 2: Multiple Port Combinations

**Objective:** Test various origin/destination combinations

**Test Data:**
| Origin | Destination | Expected Distance (approx) |
|--------|-------------|---------------------------|
| Shanghai,CN | Los Angeles,US | ~9,500 km |
| New York,US | Rotterdam,NL | ~5,900 km |
| Singapore,SG | Los Angeles,US | ~14,000 km |
| Rotterdam,NL | Shanghai,CN | ~9,200 km |

**Steps:**
1. For each combination, enter origin and destination
2. Click "Initiate Shift Order"
3. Verify route details and map display

**Expected Results:**
- ✓ All combinations work correctly
- ✓ Distances are reasonable
- ✓ Map markers appear at correct locations
- ✓ Route lines connect markers

**Status:** [ ] Pass [ ] Fail

---

### Test Case 3: Chat Context Awareness

**Objective:** Verify AI chatbot uses shift order context

**Steps:**
1. Complete origin/destination workflow
2. Ask: "What is the distance of this route?"
3. Ask: "What is the ETA?"
4. Ask: "What are the coordinates?"

**Expected Results:**
- ✓ AI provides specific distance from route details
- ✓ AI provides specific ETA from route details
- ✓ AI references actual coordinates
- ✓ Responses are accurate and contextual

**Status:** [ ] Pass [ ] Fail

---

### Test Case 4: Error Handling

**Objective:** Verify graceful error handling

**Steps:**
1. Stop backend server
2. Try to initiate shift order
3. Observe error message
4. Restart backend
5. Try again

**Expected Results:**
- ✓ User-friendly error message displays
- ✓ No application crash
- ✓ After backend restart, functionality resumes
- ✓ Error is logged in console

**Status:** [ ] Pass [ ] Fail

---

### Test Case 5: Map Interactivity

**Objective:** Verify map controls work correctly

**Steps:**
1. Complete origin/destination workflow
2. Click and drag map to pan
3. Zoom in using mouse wheel
4. Zoom out using mouse wheel
5. Click on origin marker
6. Click on destination marker

**Expected Results:**
- ✓ Map pans smoothly
- ✓ Zoom in/out works correctly
- ✓ Markers remain visible during interaction
- ✓ Route line remains visible
- ✓ No console errors during interaction

**Status:** [ ] Pass [ ] Fail

---

### Test Case 6: Chat Message History

**Objective:** Verify chat maintains conversation history

**Steps:**
1. Complete origin/destination workflow
2. Send message: "Hello"
3. Wait for response
4. Send message: "What is the route distance?"
5. Wait for response
6. Scroll up in chat

**Expected Results:**
- ✓ All messages remain visible
- ✓ Messages are in chronological order
- ✓ User and assistant messages are distinguishable
- ✓ Timestamps are displayed correctly

**Status:** [ ] Pass [ ] Fail

---

## Performance Testing

### Load Time Benchmarks

**Expected Performance:**
- Backend startup: < 5 seconds
- Frontend build: < 30 seconds
- Page load (first visit): < 3 seconds
- API response time: < 2 seconds
- Chat response time: < 5 seconds
- Map render time: < 1 second

### Testing Commands

```bash
# Backend response time
time curl http://localhost:8000/health

# Frontend build time
cd apps/frontend
time npm run build

# API endpoint performance
time curl -X POST http://localhost:8000/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"origin":"Shanghai,CN","destination":"Los Angeles,US"}'
```

---

## Accessibility Testing

### Keyboard Navigation

**Test Steps:**
1. Use Tab key to navigate through form fields
2. Use Enter key to submit form
3. Use Tab to navigate chat input
4. Use Enter to send chat message

**Expected Results:**
- ✓ All interactive elements are keyboard accessible
- ✓ Focus indicators are visible
- ✓ Tab order is logical

### Screen Reader Testing

**Test Steps:**
1. Enable screen reader (NVDA, JAWS, or VoiceOver)
2. Navigate through the page
3. Verify all content is announced

**Expected Results:**
- ✓ Form labels are announced
- ✓ Button purposes are clear
- ✓ Error messages are announced
- ✓ Chat messages are announced

---

## Security Testing

### Input Validation

**Test Steps:**
1. Try entering invalid origin/destination formats
2. Try SQL injection patterns
3. Try XSS patterns in chat input

**Expected Results:**
- ✓ Invalid inputs are rejected gracefully
- ✓ No SQL injection vulnerabilities
- ✓ XSS attempts are sanitized
- ✓ Error messages don't reveal sensitive info

---

## Regression Testing Checklist

After any code changes, verify:

- [ ] Backend starts without errors
- [ ] Frontend builds successfully
- [ ] TypeScript type checking passes
- [ ] All API endpoints respond correctly
- [ ] Origin/destination input works
- [ ] Route details display correctly
- [ ] Map renders with markers and route
- [ ] Chat functionality works
- [ ] No console errors
- [ ] No CORS errors
- [ ] Performance is acceptable

---

## Continuous Integration

### Automated Testing Commands

```bash
# Full test suite
npm run test

# Backend tests
cd apps/backend
pytest

# Frontend tests
cd apps/frontend
npm run test

# Type checking
cd apps/frontend
npm run type-check

# Linting
npm run lint
```

---

## Reporting Issues

When reporting issues, include:

1. **Environment:**
   - OS and version
   - Node.js version
   - Python version
   - Browser and version

2. **Steps to Reproduce:**
   - Exact steps taken
   - Input values used
   - Expected vs actual behavior

3. **Logs:**
   - Backend console output
   - Browser console errors
   - Network tab screenshots

4. **Screenshots:**
   - Visual issues
   - Error messages
   - Unexpected behavior

---

## Additional Resources

- **Backend API Docs:** http://localhost:8000/docs
- **AGENTS.md:** Agent system architecture and patterns
- **ARCHITECTURE.md:** Overall system architecture
- **README.md:** Project setup and overview

---

## Conclusion

This testing guide covers all aspects of the CommandCenter refactoring. Follow the test cases systematically to ensure all features work correctly. Report any issues with detailed information for quick resolution.

**Testing Status Summary:**
- Backend Services: ✓ Verified
- Frontend Build: ✓ Verified
- Integration Points: ✓ Verified
- Package Dependencies: ✓ Verified

**Known Issues:**
- None at this time

**Last Tested:** 2026-05-03

---

*Made with Bob*
