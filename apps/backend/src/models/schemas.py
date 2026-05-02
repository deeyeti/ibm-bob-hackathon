"""
Pydantic models for API requests and responses.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator


# Enums
class AgentStatus(str, Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


class EmissionCategory(str, Enum):
    """Emission category enumeration."""
    SCOPE1 = "scope1"
    SCOPE2 = "scope2"
    SCOPE3 = "scope3"


class VendorCategory(str, Enum):
    """Vendor category enumeration."""
    RENEWABLE_ENERGY = "renewable_energy"
    CARBON_OFFSET = "carbon_offset"
    ENERGY_EFFICIENCY = "energy_efficiency"
    SUSTAINABLE_TRANSPORT = "sustainable_transport"


# Base Models
class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy", description="Service health status")
    version: str = Field(description="Application version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current timestamp")


# Weather Models
class WeatherData(BaseModel):
    """Weather data model."""
    location: str = Field(description="Location name")
    temperature: float = Field(description="Temperature in Celsius")
    humidity: float = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in m/s")
    description: str = Field(description="Weather description")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")


class WeatherRequest(BaseModel):
    """Weather data request."""
    location: str = Field(description="Location name or coordinates")
    units: str = Field(default="metric", description="Units (metric/imperial)")


# Emissions Models
class EmissionData(BaseModel):
    """Carbon emission data model."""
    source: str = Field(description="Emission source")
    category: EmissionCategory = Field(description="Emission category")
    amount: float = Field(description="Emission amount in kg CO2e")
    unit: str = Field(default="kg_co2e", description="Measurement unit")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Measurement timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class EmissionSummary(BaseModel):
    """Emission summary model."""
    total_emissions: float = Field(description="Total emissions in kg CO2e")
    scope1: float = Field(description="Scope 1 emissions")
    scope2: float = Field(description="Scope 2 emissions")
    scope3: float = Field(description="Scope 3 emissions")
    period_start: datetime = Field(description="Period start date")
    period_end: datetime = Field(description="Period end date")
    reduction_target: Optional[float] = Field(default=None, description="Reduction target percentage")


class EmissionRequest(BaseModel):
    """Request to log emission data."""
    source: str = Field(description="Emission source")
    category: EmissionCategory = Field(description="Emission category")
    amount: float = Field(gt=0, description="Emission amount (must be positive)")
    unit: str = Field(default="kg_co2e", description="Measurement unit")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


# Vendor Models
class Vendor(BaseModel):
    """Vendor model."""
    id: str = Field(description="Vendor ID")
    name: str = Field(description="Vendor name")
    category: VendorCategory = Field(description="Vendor category")
    description: str = Field(description="Vendor description")
    carbon_reduction_potential: float = Field(description="Potential CO2 reduction in kg")
    cost_estimate: Optional[float] = Field(default=None, description="Estimated cost")
    rating: Optional[float] = Field(default=None, ge=0, le=5, description="Vendor rating (0-5)")
    contact_info: Optional[Dict[str, str]] = Field(default=None, description="Contact information")


class VendorRecommendation(BaseModel):
    """Vendor recommendation model."""
    vendor: Vendor = Field(description="Recommended vendor")
    relevance_score: float = Field(ge=0, le=1, description="Relevance score (0-1)")
    reasoning: str = Field(description="Recommendation reasoning")
    estimated_impact: float = Field(description="Estimated emission reduction in kg CO2e")


class VendorSearchRequest(BaseModel):
    """Vendor search request."""
    category: Optional[VendorCategory] = Field(default=None, description="Filter by category")
    min_reduction: Optional[float] = Field(default=None, description="Minimum CO2 reduction")
    max_cost: Optional[float] = Field(default=None, description="Maximum cost")
    location: Optional[str] = Field(default=None, description="Location preference")


# Agent Models
class AgentInfo(BaseModel):
    """Agent information model."""
    id: str = Field(description="Agent ID")
    name: str = Field(description="Agent name")
    type: str = Field(description="Agent type (monitor/auditor/orchestrator)")
    status: AgentStatus = Field(description="Current agent status")
    last_run: Optional[datetime] = Field(default=None, description="Last execution timestamp")
    next_run: Optional[datetime] = Field(default=None, description="Next scheduled execution")
    metrics: Optional[Dict[str, Any]] = Field(default=None, description="Agent metrics")


class AgentAction(BaseModel):
    """Agent action model."""
    agent_id: str = Field(description="Agent ID")
    action: str = Field(description="Action to perform (start/stop/restart)")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Action parameters")


class AgentResponse(BaseModel):
    """Agent action response."""
    agent_id: str = Field(description="Agent ID")
    status: AgentStatus = Field(description="Agent status after action")
    message: str = Field(description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


# Monitoring Models
class MonitoringAlert(BaseModel):
    """Monitoring alert model."""
    id: str = Field(description="Alert ID")
    severity: str = Field(description="Alert severity (info/warning/critical)")
    title: str = Field(description="Alert title")
    message: str = Field(description="Alert message")
    source: str = Field(description="Alert source")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Alert timestamp")
    resolved: bool = Field(default=False, description="Alert resolution status")


class MonitoringMetrics(BaseModel):
    """System monitoring metrics."""
    cpu_usage: float = Field(ge=0, le=100, description="CPU usage percentage")
    memory_usage: float = Field(ge=0, le=100, description="Memory usage percentage")
    active_agents: int = Field(ge=0, description="Number of active agents")
    api_requests: int = Field(ge=0, description="Total API requests")
    error_rate: float = Field(ge=0, le=100, description="Error rate percentage")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Metrics timestamp")


# Analysis Models
class EmissionAnalysis(BaseModel):
    """Emission analysis result."""
    total_emissions: float = Field(description="Total emissions analyzed")
    trend: str = Field(description="Emission trend (increasing/decreasing/stable)")
    insights: List[str] = Field(description="Key insights from analysis")
    recommendations: List[str] = Field(description="Recommendations for reduction")
    confidence_score: float = Field(ge=0, le=1, description="Analysis confidence score")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class OptimizationSuggestion(BaseModel):
    """Optimization suggestion model."""
    id: str = Field(description="Suggestion ID")
    title: str = Field(description="Suggestion title")
    description: str = Field(description="Detailed description")
    potential_reduction: float = Field(description="Potential CO2 reduction in kg")
    implementation_cost: Optional[float] = Field(default=None, description="Implementation cost")
    priority: str = Field(description="Priority level (high/medium/low)")
    category: str = Field(description="Suggestion category")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Suggestion timestamp")


# Error Models
class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

# Made with Bob
