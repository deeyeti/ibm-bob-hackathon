# =============================================================================
# Eco-Shift Development Script (PowerShell)
# =============================================================================
# This script starts both frontend and backend in development mode
# Usage: .\scripts\dev.ps1

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  ECO-SHIFT DEVELOPMENT ENVIRONMENT" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-Not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file. Please update it with your API keys." -ForegroundColor Green
    Write-Host ""
    Read-Host "Press Enter to continue or Ctrl+C to exit and configure .env"
}

# Function to check if a command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Cyan

$missingPrereqs = @()

if (-Not (Test-Command "node")) {
    $missingPrereqs += "Node.js"
}

if (-Not (Test-Command "npm")) {
    $missingPrereqs += "npm"
}

if (-Not (Test-Command "python")) {
    $missingPrereqs += "Python"
}

if (-Not (Test-Command "pip")) {
    $missingPrereqs += "pip"
}

if ($missingPrereqs.Count -gt 0) {
    Write-Host "❌ Missing prerequisites: $($missingPrereqs -join ', ')" -ForegroundColor Red
    Write-Host "Please install the missing tools and try again." -ForegroundColor Red
    exit 1
}

Write-Host "✓ All prerequisites found" -ForegroundColor Green
Write-Host ""

# Start backend
Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Set-Location "apps/backend"
    
    # Activate virtual environment if it exists
    if (Test-Path "venv/Scripts/Activate.ps1") {
        & "venv/Scripts/Activate.ps1"
    }
    
    # Start FastAPI with uvicorn
    python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
}

Write-Host "✓ Backend starting on http://localhost:8000" -ForegroundColor Green
Write-Host ""

# Wait a moment for backend to start
Start-Sleep -Seconds 2

# Start frontend
Write-Host "Starting Frontend (Next.js)..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Set-Location "apps/frontend"
    npm run dev
}

Write-Host "✓ Frontend starting on http://localhost:3000" -ForegroundColor Green
Write-Host ""

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  DEVELOPMENT SERVERS RUNNING" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Yellow
Write-Host ""

# Monitor jobs and display output
try {
    while ($true) {
        # Check if jobs are still running
        if ($backendJob.State -ne "Running" -and $frontendJob.State -ne "Running") {
            Write-Host "All servers stopped" -ForegroundColor Yellow
            break
        }
        
        # Receive output from jobs
        Receive-Job -Job $backendJob -ErrorAction SilentlyContinue
        Receive-Job -Job $frontendJob -ErrorAction SilentlyContinue
        
        Start-Sleep -Seconds 1
    }
}
finally {
    # Cleanup: Stop all jobs
    Write-Host ""
    Write-Host "Stopping servers..." -ForegroundColor Yellow
    
    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job -Job $frontendJob -ErrorAction SilentlyContinue
    
    Remove-Job -Job $backendJob -Force -ErrorAction SilentlyContinue
    Remove-Job -Job $frontendJob -Force -ErrorAction SilentlyContinue
    
    Write-Host "✓ All servers stopped" -ForegroundColor Green
}

# Made with Bob
