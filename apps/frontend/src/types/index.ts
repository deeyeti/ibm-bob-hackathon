/**
 * Frontend Type Definitions for Eco-Shift
 * 
 * These types define the data structures used throughout the frontend application.
 * They should match the backend API response types.
 */

// ============================================================================
// Agent Types
// ============================================================================

export type AgentStatus = 'idle' | 'running' | 'paused' | 'error'

export interface Agent {
  id: string
  name: string
  type: 'monitor' | 'auditor' | 'orchestrator'
  status: AgentStatus
  description: string
  lastActive?: string
  metrics?: {
    tasksCompleted: number
    successRate: number
    averageResponseTime: number
  }
}

export interface AgentAction {
  id: string
  agentId: string
  action: string
  timestamp: string
  status: 'success' | 'failed' | 'pending'
  details?: string
}

// ============================================================================
// Weather Types
// ============================================================================

export interface WeatherData {
  location: string
  temperature: number
  condition: string
  humidity: number
  windSpeed: number
  timestamp: string
  forecast?: WeatherForecast[]
}

export interface WeatherForecast {
  date: string
  temperature: {
    min: number
    max: number
  }
  condition: string
  precipitationChance: number
}

export interface WeatherAlert {
  id: string
  type: 'warning' | 'watch' | 'advisory'
  severity: 'low' | 'medium' | 'high' | 'critical'
  title: string
  description: string
  startTime: string
  endTime: string
  affectedAreas: string[]
}

// ============================================================================
// Vendor Types
// ============================================================================

export interface Vendor {
  id: string
  name: string
  location: string
  type: 'supplier' | 'manufacturer' | 'distributor'
  status: 'active' | 'inactive' | 'pending'
  sustainabilityScore: number
  fleets: Fleet[]
  contact?: {
    email: string
    phone: string
    address: string
  }
}

export interface Fleet {
  id: string
  vendorId: string
  name: string
  fuelType: 'diesel' | 'electric' | 'hydrogen' | 'hybrid'
  vehicleCount: number
  capacity: number
  emissionsPerKm: number
  sustainabilityScore: number
  status: 'available' | 'in-use' | 'maintenance'
}

// ============================================================================
// Emissions Types
// ============================================================================

export interface EmissionsData {
  scope3Total: number
  breakdown: {
    transportation: number
    manufacturing: number
    distribution: number
    other: number
  }
  trend: EmissionsTrend[]
  comparisonToPrevious: number
}

export interface EmissionsTrend {
  date: string
  value: number
  category: string
}

export interface EmissionsCalculation {
  routeId: string
  distance: number
  fuelType: string
  emissions: number
  recommendations: string[]
}

export interface EmissionsAnalysis {
  totalEmissions: number
  averagePerRoute: number
  topEmitters: {
    vendorId: string
    vendorName: string
    emissions: number
  }[]
  reductionOpportunities: {
    description: string
    potentialSavings: number
    priority: 'low' | 'medium' | 'high'
  }[]
}

// ============================================================================
// Dashboard Types
// ============================================================================

export interface DashboardMetrics {
  totalVendors: number
  activeFleets: number
  totalEmissions: number
  sustainabilityScore: number
  weatherAlerts: number
  agentStatus: {
    monitor: AgentStatus
    auditor: AgentStatus
  }
}

export interface ChartData {
  labels: string[]
  datasets: {
    label: string
    data: number[]
    backgroundColor?: string | string[]
    borderColor?: string | string[]
  }[]
}

// ============================================================================
// API Response Types
// ============================================================================

export interface APIResponse<T> {
  success: boolean
  data: T
  message?: string
  timestamp: string
}

export interface APIError {
  success: false
  error: string
  message: string
  statusCode: number
  timestamp: string
}

export interface PaginatedResponse<T> {
  success: boolean
  data: T[]
  pagination: {
    page: number
    pageSize: number
    totalPages: number
    totalItems: number
  }
}

// ============================================================================
// UI Component Types
// ============================================================================

export interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

export interface TableColumn<T> {
  key: keyof T
  label: string
  sortable?: boolean
  render?: (value: any, row: T) => React.ReactNode
}

export interface FilterOption {
  key: string
  label: string
  type: 'select' | 'range' | 'date' | 'text'
  options?: SelectOption[]
}

// ============================================================================
// Notification Types
// ============================================================================

export type NotificationType = 'success' | 'error' | 'warning' | 'info'

export interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  timestamp: string
  read: boolean
  actionUrl?: string
}

// ============================================================================
// User Types (for future authentication)
// ============================================================================

export interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'manager' | 'viewer'
  avatar?: string
}

// ============================================================================
// Utility Types
// ============================================================================

export type SortOrder = 'asc' | 'desc'

export interface SortConfig<T> {
  key: keyof T
  order: SortOrder
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error'

export interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

// ============================================================================
// Orchestrator Types
// ============================================================================

export interface OrchestratorRequest {
  origin: string
  destination: string
}

export interface OrchestratorResponse {
  workflow_id: string
  status: 'completed' | 'error'
  reroute_required: boolean
  approved_vendor_id?: string
  emissions_saving?: string
  justification?: string
  weather_status?: string
  timestamp: string
  error?: string
  route_details?: {
    distance: number
    eta: string
    origin_coords?: [number, number]
    destination_coords?: [number, number]
  }
}

export interface AgentLog {
  id: string
  timestamp: string
  agent: 'monitor' | 'auditor' | 'orchestrator'
  level: 'info' | 'warning' | 'error' | 'success'
  message: string
}

// ============================================================================
// Chat Types
// ============================================================================

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface ChatRequest {
  message: string
  shift_order_context?: any
}

export interface ChatResponse {
  response: string
  timestamp: string
}

// Made with Bob
