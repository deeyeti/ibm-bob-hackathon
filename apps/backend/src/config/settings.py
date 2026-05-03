"""
Application configuration using pydantic-settings.
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Settings
    app_name: str = Field(default="Eco-Shift Backend", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    environment: str = Field(default="development", description="Environment (development/production)")
    debug: bool = Field(default=True, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(default=True, description="Auto-reload on code changes")

    # CORS Settings
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:3001",
        description="Allowed CORS origins (comma-separated)",
    )
    cors_allow_credentials: bool = Field(default=True, description="Allow credentials")
    cors_allow_methods: str = Field(default="*", description="Allowed HTTP methods")
    cors_allow_headers: str = Field(default="*", description="Allowed HTTP headers")

    # IBM watsonx.ai Configuration
    watsonx_api_key: Optional[str] = Field(default=None, description="watsonx.ai API key")
    watsonx_project_id: Optional[str] = Field(default=None, description="watsonx.ai project ID")
    watsonx_url: str = Field(
        default="https://us-south.ml.cloud.ibm.com",
        description="watsonx.ai service URL",
    )
    watsonx_model_id: str = Field(
        default="meta-llama/llama-3-3-70b-instruct",
        description="Default model ID",
    )

    # IBM Cloud Configuration
    ibm_cloud_api_key: Optional[str] = Field(default=None, description="IBM Cloud API key")
    ibm_cloud_url: str = Field(
        default="https://us-south.ml.cloud.ibm.com",
        description="IBM Cloud URL",
    )

    # OpenWeather API Configuration
    openweather_api_key: Optional[str] = Field(default=None, description="OpenWeather API key")
    openweather_base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5",
        description="OpenWeather API base URL",
    )

    # Agent Configuration
    agent_monitor_enabled: bool = Field(default=True, description="Enable monitoring agent")
    agent_auditor_enabled: bool = Field(default=True, description="Enable auditor agent")
    agent_orchestrator_enabled: bool = Field(default=True, description="Enable orchestrator agent")
    agent_polling_interval: int = Field(default=300, description="Agent polling interval (seconds)")
    
    # BeeAI Framework Configuration
    use_beeai: bool = Field(default=True, description="Use BeeAI framework for agents")
    beeai_log_level: str = Field(default="INFO", description="BeeAI framework log level")
    beeai_timeout: int = Field(default=30, description="BeeAI agent timeout (seconds)")

    # Security
    secret_key: str = Field(
        default="change_this_secret_key_in_production",
        description="Secret key for JWT",
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time",
    )

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_per_minute: int = Field(default=60, description="Requests per minute limit")

    # External APIs
    carbon_intensity_api_url: str = Field(
        default="https://api.carbonintensity.org.uk",
        description="Carbon Intensity API URL",
    )
    electricity_maps_api_key: Optional[str] = Field(
        default=None,
        description="Electricity Maps API key",
    )

    # Monitoring and Logging
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=9090, description="Metrics server port")

    # Feature Flags
    enable_weather_integration: bool = Field(default=True, description="Enable weather integration")
    enable_vendor_recommendations: bool = Field(
        default=True,
        description="Enable vendor recommendations",
    )
    enable_emissions_tracking: bool = Field(
        default=True,
        description="Enable emissions tracking",
    )
    enable_real_time_monitoring: bool = Field(
        default=True,
        description="Enable real-time monitoring",
    )

    @field_validator("cors_origins", mode="after")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()

# Made with Bob