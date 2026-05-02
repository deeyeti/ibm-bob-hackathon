"""Data models and schemas for Eco-Shift backend."""

from .schemas import (
    # Enums
    AgentStatus,
    EmissionCategory,
    VendorCategory,
    # Base Models
    HealthResponse,
    # Weather Models
    WeatherData,
    WeatherRequest,
    # Emissions Models
    EmissionData,
    EmissionSummary,
    EmissionRequest,
    # Vendor Models
    Vendor,
    VendorRecommendation,
    VendorSearchRequest,
    # Agent Models
    AgentInfo,
    AgentAction,
    AgentResponse,
    # Monitoring Models
    MonitoringAlert,
    MonitoringMetrics,
    # Analysis Models
    EmissionAnalysis,
    OptimizationSuggestion,
    # Error Models
    ErrorResponse,
)

__all__ = [
    # Enums
    "AgentStatus",
    "EmissionCategory",
    "VendorCategory",
    # Base Models
    "HealthResponse",
    # Weather Models
    "WeatherData",
    "WeatherRequest",
    # Emissions Models
    "EmissionData",
    "EmissionSummary",
    "EmissionRequest",
    # Vendor Models
    "Vendor",
    "VendorRecommendation",
    "VendorSearchRequest",
    # Agent Models
    "AgentInfo",
    "AgentAction",
    "AgentResponse",
    # Monitoring Models
    "MonitoringAlert",
    "MonitoringMetrics",
    # Analysis Models
    "EmissionAnalysis",
    "OptimizationSuggestion",
    # Error Models
    "ErrorResponse",
]

# Made with Bob
