# AI Consultant Troubleshooting Guide

## Error: "Request failed with status code 500"

This error occurs when the AI Consultant cannot connect to IBM watsonx.ai service.

## Quick Fix Steps

### 1. Check Your Environment Variables

Make sure you have a `.env` file in the `apps/backend/` directory with valid IBM watsonx.ai credentials:

```bash
# Required for AI Consultant
WATSONX_API_KEY=your_actual_api_key_here
WATSONX_PROJECT_ID=your_actual_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### 2. Get IBM watsonx.ai Credentials

If you don't have credentials yet:

1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Create an account or log in
3. Navigate to **watsonx.ai** service
4. Create a new project or select an existing one
5. Get your **API Key** from IBM Cloud IAM
6. Get your **Project ID** from the watsonx.ai project settings

### 3. Copy Environment Variables

```bash
# From the project root
cd apps/backend
cp .env.example .env

# Edit .env and add your credentials
# On Windows:
notepad .env

# On Mac/Linux:
nano .env
```

### 4. Restart the Backend Server

After updating your `.env` file:

```bash
# Stop the current server (Ctrl+C)

# Restart from project root
npm run dev

# Or restart backend only
cd apps/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Verify Initialization

Check the backend logs for successful initialization:

```bash
# You should see:
✅ Watsonx service initialized successfully
```

If you see an error instead:
```bash
❌ Failed to initialize watsonx service: [error details]
⚠️ AI Consultant will not be available without valid watsonx credentials
```

This means your credentials are invalid or missing.

## Common Issues

### Issue 1: "Invalid API Key"

**Solution**: 
- Verify your API key is correct (no extra spaces)
- Make sure the API key has access to watsonx.ai
- Check if the API key is expired

### Issue 2: "Project ID not found"

**Solution**:
- Verify the Project ID matches your watsonx.ai project
- Ensure the project is in the same region as your WATSONX_URL
- Check that your API key has access to this project

### Issue 3: "Service Unavailable (503)"

**Solution**:
- The watsonx service couldn't initialize
- Check your internet connection
- Verify IBM Cloud services are operational
- Review backend logs for detailed error messages

### Issue 4: Environment Variables Not Loading

**Solution**:
```bash
# Make sure .env file is in the correct location
apps/backend/.env  # ✅ Correct
.env               # ❌ Wrong location

# Verify file contents
cat apps/backend/.env

# Restart the server completely
```

## Testing the Fix

1. Start the backend server
2. Check logs for "✅ Watsonx service initialized successfully"
3. Open the frontend at http://localhost:3000
4. Click on the AI Consultant chat icon
5. Send a test message like "What is Eco-Shift?"
6. You should receive an AI-generated response

## Still Having Issues?

### Check Backend Logs

```bash
# View real-time logs
npm run logs

# Or check the log file
cat apps/backend/logs/app.log
```

### Test API Directly

```bash
# Test the chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Verify Service Status

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check info endpoint
curl http://localhost:8000/info
```

## What Was Fixed

The following changes were made to resolve the AI Consultant error:

1. **`apps/backend/src/main.py`**: Added automatic watsonx service initialization on startup
2. **`apps/backend/src/api/chat.py`**: Added better error handling with user-friendly messages
3. **Service initialization**: Now happens automatically when the backend starts

## Need Help?

If you're still experiencing issues:

1. Check the [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
2. Review the backend logs for specific error messages
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Try using a different watsonx.ai model by setting `WATSONX_MODEL_ID` in `.env`

## Alternative: Run Without AI Consultant

If you want to test the application without the AI Consultant:

1. The rest of the application will work normally
2. Only the chat feature will be unavailable
3. Weather monitoring and emissions tracking will still function
4. You'll see a warning in logs but the app won't crash

---

**Last Updated**: 2026-05-03  
**Status**: ✅ Fixed in latest version