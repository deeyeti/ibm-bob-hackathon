/**
 * Shared TypeScript Type Definitions for Eco-Shift
 * 
 * This file contains all shared types used across frontend and backend
 */

// =============================================================================
// Agent Types
// =============================================================================

export type AgentStatus = 'idle' | 'running' | 'error' | 'stopped';

export type AgentType = 'monitor' | 'auditor' | 'orchestrator';

export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  status: AgentStatus;
  last_run: string | null;
  next_run: string | null;
  metrics: Record<string, any>;
}

export interface AgentInfo extends Agent {
  description?: string;
  version?: string;
  capabilities?: string[];
}

// =============================================================================
// Weather Types
// =============================================================================

export interface WeatherCondition {
  id: number;
  main: string;
  description: string;
  icon: string;
}

export interface WeatherData {
  location: string;
  latitude: number;
  longitude: number;
  temperature: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  pressure: number;
  humidity: number;
  visibility: number;
  wind_speed: number;
  wind_deg: number;
  wind_gust?: number;
  clouds: number;
  conditions: WeatherCondition[];
  timestamp: string;
  sunrise?: string;
  sunset?: string;
}

export interface WeatherAlert {
  id: string;
  type: 'temperature' | 'wind' | 'precipitation' | 'visibility' | 'general';
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  location: string;
  affected_vendors: string[];
  timestamp: string;
  expires_at?: string;
  recommendations?: string[];
}

export interface WeatherForecast {
  location: string;
  forecasts: Array<{
    timestamp: string;
    temperature: number;
    conditions: WeatherCondition[];
    precipitation_probability: number;
    wind_speed: number;
  }>;
}

// =============================================================================
// Vendor Types
// =============================================================================

export interface VendorLocation {
  latitude: number;
  longitude: number;
  address: string;
  city: string;
  state: string;
  country: string;
  postal_code?: string;
}

export interface Vendor {
  id: string;
  name: string;
  location: VendorLocation;
  contact?: {
    email?: string;
    phone?: string;
    website?: string;
  };
  capacity?: number;
  operating_hours?: {
    open: string;
    close: string;
    days: string[];
  };
  weather_data?: WeatherData;
  last_updated: string;
}

export interface VendorWithWeather extends Vendor {
  weather_data: WeatherData;
  weather_alerts: WeatherAlert[];
  risk_level: 'low' | 'medium' | 'high' | 'critical';
}

// =============================================================================
// Emissions Types
// =============================================================================

export type FuelType = 'diesel' | 'petrol' | 'electric' | 'hybrid' | 'cng';

export interface EmissionFactors {
  diesel: number;
  petrol: number;
  electric: number;
  hybrid: number;
  cng: number;
}

export interface EmissionsData {
  total_emissions: number;
  emissions_by_fuel: Record<FuelType, number>;
  emissions_by_route: Array<{
    route_id: string;
    emissions: number;
    distance: number;
  }>;
  baseline_emissions?: number;
  reduction_percentage?: number;
  carbon_offset_cost?: number;
}

export interface EmissionsCalculation {
  vehicle_id: string;
  fuel_type: FuelType;
  distance_km: number;
  emissions_kg: number;
  calculation_method: string;
  timestamp: string;
}

// =============================================================================
// Fleet Types
// =============================================================================

export interface Vehicle {
  id: string;
  type: 'truck' | 'van' | 'car' | 'bike';
  fuel_type: FuelType;
  capacity_kg: number;
  fuel_efficiency: number;
  emissions_factor: number;
  status: 'available' | 'in_use' | 'maintenance' | 'retired';
  current_location?: {
    latitude: number;
    longitude: number;
  };
  last_maintenance?: string;
  next_maintenance?: string;
}

export interface FleetStats {
  total_vehicles: number;
  available_vehicles: number;
  in_use_vehicles: number;
  maintenance_vehicles: number;
  total_capacity_kg: number;
  average_fuel_efficiency: number;
  vehicles_by_fuel_type: Record<FuelType, number>;
}

export interface FleetPrioritization {
  vehicle_id: string;
  priority_score: number;
  reasons: string[];
  recommended_routes: string[];
  estimated_emissions: number;
}

// =============================================================================
// Route Types
// =============================================================================

export interface RoutePoint {
  latitude: number;
  longitude: number;
  address?: string;
  arrival_time?: string;
  departure_time?: string;
}

export interface Route {
  id: string;
  name: string;
  origin: RoutePoint;
  destination: RoutePoint;
  waypoints: RoutePoint[];
  distance_km: number;
  duration_minutes: number;
  estimated_emissions: number;
  weather_conditions?: WeatherData[];
  traffic_conditions?: 'light' | 'moderate' | 'heavy';
  road_conditions?: 'good' | 'fair' | 'poor';
  status: 'planned' | 'active' | 'completed' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface OptimizedRoute extends Route {
  optimization_score: number;
  emissions_reduction: number;
  time_savings: number;
  cost_savings: number;
  alternative_routes?: Route[];
  optimization_factors: string[];
}

export interface RouteOptimization {
  original_route: Route;
  optimized_route: OptimizedRoute;
  improvements: {
    distance_reduction_km: number;
    time_reduction_minutes: number;
    emissions_reduction_kg: number;
    cost_reduction: number;
  };
  recommendations: string[];
}

// =============================================================================
// Audit Types
// =============================================================================

export interface AuditRequest {
  vendor_ids: string[];
  timestamp: string;
  priority?: 'low' | 'normal' | 'high';
  options?: {
    include_weather?: boolean;
    include_routes?: boolean;
    include_emissions?: boolean;
  };
}

export interface AuditResult {
  audit_id: string;
  timestamp: string;
  vendors_audited: number;
  total_emissions: number;
  optimizations_found: number;
  potential_savings: {
    emissions_kg: number;
    cost: number;
    time_minutes: number;
  };
  recommendations: Array<{
    type: 'route' | 'fleet' | 'vendor' | 'general';
    priority: 'low' | 'medium' | 'high';
    description: string;
    impact: string;
  }>;
  fleet_prioritization?: FleetPrioritization[];
  route_optimizations?: RouteOptimization[];
  emissions_data?: EmissionsData;
}

// =============================================================================
// Orchestrator Types
// =============================================================================

export interface WorkflowStep {
  step: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'skipped';
  data?: any;
  error?: string;
  timestamp?: string;
  duration_ms?: number;
}

export interface WorkflowResult {
  workflow_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  timestamp: string;
  steps: WorkflowStep[];
  error?: string;
  duration_ms?: number;
}

export interface OrchestratorStatus {
  orchestrator: Agent;
  child_agents: {
    monitor: Agent | null;
    auditor: Agent | null;
  };
  last_weather_check: string | null;
  last_audit: string | null;
  active_workflows: number;
  message_bus_stats?: {
    running: boolean;
    subscribers: Record<string, number>;
    queues: Record<string, number>;
    pending_responses: number;
    message_history_size: number;
  };
}

// =============================================================================
// Message Bus Types
// =============================================================================

export type MessageType = 
  | 'weather_alert'
  | 'vendor_list'
  | 'audit_request'
  | 'audit_result'
  | 'optimization_request'
  | 'optimization_result'
  | 'agent_status'
  | 'error'
  | 'command';

export type MessagePriority = 'low' | 'normal' | 'high' | 'critical';

export interface Message {
  id: string;
  type: MessageType;
  sender: string;
  recipient: string | null;
  payload: Record<string, any>;
  priority: MessagePriority;
  timestamp: string;
  ttl: number | null;
  correlation_id: string | null;
}

// =============================================================================
// API Response Types
// =============================================================================

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  timestamp: string;
}

export interface PaginatedResponse<T = any> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// =============================================================================
// Dashboard Types
// =============================================================================

export interface DashboardStats {
  total_vendors: number;
  active_alerts: number;
  total_emissions_today: number;
  emissions_reduction: number;
  active_routes: number;
  fleet_utilization: number;
  weather_alerts: WeatherAlert[];
  recent_audits: AuditResult[];
}

export interface ChartDataPoint {
  timestamp: string;
  value: number;
  label?: string;
}

export interface EmissionsChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    backgroundColor?: string;
    borderColor?: string;
  }>;
}

// =============================================================================
// Configuration Types
// =============================================================================

export interface AppConfig {
  api_url: string;
  app_name: string;
  app_version: string;
  environment: 'development' | 'staging' | 'production';
  features: {
    real_time_updates: boolean;
    advanced_analytics: boolean;
    export_reports: boolean;
  };
}

// =============================================================================
// Utility Types
// =============================================================================

export type Nullable<T> = T | null;

export type Optional<T> = T | undefined;

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type AsyncFunction<T = any> = (...args: any[]) => Promise<T>;

// =============================================================================
// End of type definitions
// =============================================================================

// Made with Bob
