# =============================================================================
# Eco-Shift Test Script (PowerShell)
# =============================================================================
# This script runs all tests for frontend and backend
# Usage: .\scripts\test.ps1

param(
    [switch]$Frontend,
    [switch]$Backend,
    [switch]$Watch,
    [switch]$Coverage
)

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  ECO-SHIFT TEST RUNNER" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

$runFrontend = $Frontend -or (-not $Backend)
$runBackend = $Backend -or (-not $Frontend)

$exitCode = 0

# Run backend tests
if ($runBackend) {
    Write-Host "Running Backend Tests (pytest)..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location "apps/backend"
    
    # Activate virtual environment if it exists
    if (Test-Path "venv/Scripts/Activate.ps1") {
        & "venv/Scripts/Activate.ps1"
    }
    
    $pytestArgs = @()
    
    if ($Coverage) {
        $pytestArgs += "--cov=src"
        $pytestArgs += "--cov-report=html"
        $pytestArgs += "--cov-report=term"
    }
    
    if ($Watch) {
        $pytestArgs += "-f"
    }
    
    python -m pytest @pytestArgs
    
    if ($LASTEXITCODE -ne 0) {
        $exitCode = 1
        Write-Host ""
        Write-Host "❌ Backend tests failed" -ForegroundColor Red
    } else {
        Write-Host ""
        Write-Host "✓ Backend tests passed" -ForegroundColor Green
    }
    
    if ($Coverage) {
        Write-Host ""
        Write-Host "Coverage report generated in apps/backend/htmlcov/index.html" -ForegroundColor Cyan
    }
    
    Set-Location "../.."
    Write-Host ""
}

# Run frontend tests
if ($runFrontend) {
    Write-Host "Running Frontend Tests (Jest)..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location "apps/frontend"
    
    $jestArgs = @("test")
    
    if ($Watch) {
        $jestArgs += "--watch"
    }
    
    if ($Coverage) {
        $jestArgs += "--coverage"
    }
    
    npm run @jestArgs
    
    if ($LASTEXITCODE -ne 0) {
        $exitCode = 1
        Write-Host ""
        Write-Host "❌ Frontend tests failed" -ForegroundColor Red
    } else {
        Write-Host ""
        Write-Host "✓ Frontend tests passed" -ForegroundColor Green
    }
    
    if ($Coverage) {
        Write-Host ""
        Write-Host "Coverage report generated in apps/frontend/coverage/index.html" -ForegroundColor Cyan
    }
    
    Set-Location "../.."
    Write-Host ""
}

# Summary
Write-Host "==============================================================================" -ForegroundColor Cyan
if ($exitCode -eq 0) {
    Write-Host "  ALL TESTS PASSED ✓" -ForegroundColor Green
} else {
    Write-Host "  SOME TESTS FAILED ❌" -ForegroundColor Red
}
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

exit $exitCode

# Made with Bob
