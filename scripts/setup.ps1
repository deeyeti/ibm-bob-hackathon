# =============================================================================
# Eco-Shift Setup Script (PowerShell)
# =============================================================================
# This script sets up the development environment
# Usage: .\scripts\setup.ps1

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  ECO-SHIFT PROJECT SETUP" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "Step 1: Checking prerequisites..." -ForegroundColor Cyan
Write-Host ""

$allPrereqsMet = $true

# Check Node.js
if (Test-Command "node") {
    $nodeVersion = node --version
    Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
    Write-Host "   Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Yellow
    $allPrereqsMet = $false
}

# Check npm
if (Test-Command "npm") {
    $npmVersion = npm --version
    Write-Host "✓ npm: v$npmVersion" -ForegroundColor Green
} else {
    Write-Host "❌ npm not found" -ForegroundColor Red
    $allPrereqsMet = $false
}

# Check Python
if (Test-Command "python") {
    $pythonVersion = python --version
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found" -ForegroundColor Red
    Write-Host "   Please install Python 3.11+ from https://www.python.org/" -ForegroundColor Yellow
    $allPrereqsMet = $false
}

# Check pip
if (Test-Command "pip") {
    $pipVersion = pip --version
    Write-Host "✓ pip: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "❌ pip not found" -ForegroundColor Red
    $allPrereqsMet = $false
}

Write-Host ""

if (-Not $allPrereqsMet) {
    Write-Host "❌ Some prerequisites are missing. Please install them and run this script again." -ForegroundColor Red
    exit 1
}

# Setup environment file
Write-Host "Step 2: Setting up environment file..." -ForegroundColor Cyan
Write-Host ""

if (-Not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file from .env.example" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Please update .env with your API keys:" -ForegroundColor Yellow
    Write-Host "   - WATSONX_API_KEY" -ForegroundColor Yellow
    Write-Host "   - WATSONX_PROJECT_ID" -ForegroundColor Yellow
    Write-Host "   - OPENWEATHER_API_KEY" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
    Write-Host ""
}

# Install frontend dependencies
Write-Host "Step 3: Installing frontend dependencies..." -ForegroundColor Cyan
Write-Host ""

Set-Location "apps/frontend"
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    Set-Location "../.."
    exit 1
}
Set-Location "../.."
Write-Host ""

# Setup Python virtual environment
Write-Host "Step 4: Setting up Python virtual environment..." -ForegroundColor Cyan
Write-Host ""

Set-Location "apps/backend"

if (-Not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✓ Created virtual environment" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
& "venv/Scripts/Activate.ps1"
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install backend dependencies" -ForegroundColor Red
    Set-Location "../.."
    exit 1
}

Set-Location "../.."
Write-Host ""

# Create necessary directories
Write-Host "Step 5: Creating necessary directories..." -ForegroundColor Cyan
Write-Host ""

$directories = @(
    "apps/backend/logs",
    "apps/backend/data",
    "apps/frontend/public/assets"
)

foreach ($dir in $directories) {
    if (-Not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ $dir already exists" -ForegroundColor Green
    }
}

Write-Host ""

# Summary
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host ""
Write-Host "1. Update .env file with your API keys" -ForegroundColor Yellow
Write-Host "2. Run development servers:" -ForegroundColor Yellow
Write-Host "   .\scripts\dev.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Or use Docker:" -ForegroundColor Yellow
Write-Host "   docker-compose up" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Access the application:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor White
Write-Host ""

# Made with Bob
