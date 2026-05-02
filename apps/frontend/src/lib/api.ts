import axios, { AxiosInstance, AxiosError } from 'axios'

/**
 * API Client for Eco-Shift Backend
 * 
 * This client handles all communication with the Python FastAPI backend.
 * It includes error handling, request/response interceptors, and type-safe methods.
 */

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_TIMEOUT = 30000 // 30 seconds

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add authentication token if available
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Log request in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`)
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Log response in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Response] ${response.config.url}`, response.data)
    }
    return response
  },
  (error: AxiosError) => {
    // Handle errors
    if (error.response) {
      // Server responded with error status
      console.error(`[API Error] ${error.response.status}:`, error.response.data)
      
      // Handle specific error codes
      if (error.response.status === 401) {
        // Unauthorized - clear token and redirect to login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token')
          // window.location.href = '/login'
        }
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('[API Error] No response received:', error.request)
    } else {
      // Error in request setup
      console.error('[API Error] Request setup error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// ============================================================================
// API Methods
// ============================================================================

/**
 * Agent Management API
 */
export const agentsAPI = {
  /**
   * Get all agents and their status
   */
  getAll: async () => {
    const response = await apiClient.get('/api/agents')
    return response.data
  },

  /**
   * Get specific agent details
   */
  getById: async (agentId: string) => {
    const response = await apiClient.get(`/api/agents/${agentId}`)
    return response.data
  },

  /**
   * Start an agent
   */
  start: async (agentId: string) => {
    const response = await apiClient.post(`/api/agents/${agentId}/start`)
    return response.data
  },

  /**
   * Stop an agent
   */
  stop: async (agentId: string) => {
    const response = await apiClient.post(`/api/agents/${agentId}/stop`)
    return response.data
  },
}

/**
 * Weather Data API (Monitor Agent)
 */
export const weatherAPI = {
  /**
   * Get current weather data
   */
  getCurrent: async () => {
    const response = await apiClient.get('/api/weather/current')
    return response.data
  },

  /**
   * Get weather forecast
   */
  getForecast: async () => {
    const response = await apiClient.get('/api/weather/forecast')
    return response.data
  },

  /**
   * Get weather alerts
   */
  getAlerts: async () => {
    const response = await apiClient.get('/api/weather/alerts')
    return response.data
  },
}

/**
 * Vendor Management API (Monitor Agent)
 */
export const vendorsAPI = {
  /**
   * Get all vendors
   */
  getAll: async () => {
    const response = await apiClient.get('/api/vendors')
    return response.data
  },

  /**
   * Add new vendor
   */
  create: async (vendorData: any) => {
    const response = await apiClient.post('/api/vendors', vendorData)
    return response.data
  },

  /**
   * Update vendor
   */
  update: async (vendorId: string, vendorData: any) => {
    const response = await apiClient.put(`/api/vendors/${vendorId}`, vendorData)
    return response.data
  },

  /**
   * Delete vendor
   */
  delete: async (vendorId: string) => {
    const response = await apiClient.delete(`/api/vendors/${vendorId}`)
    return response.data
  },
}

/**
 * Emissions Data API (Auditor Agent)
 */
export const emissionsAPI = {
  /**
   * Get Scope 3 emissions data
   */
  getScope3: async () => {
    const response = await apiClient.get('/api/emissions/scope3')
    return response.data
  },

  /**
   * Get emissions analysis
   */
  getAnalysis: async () => {
    const response = await apiClient.get('/api/emissions/analysis')
    return response.data
  },

  /**
   * Calculate emissions for a route
   */
  calculate: async (routeData: any) => {
    const response = await apiClient.post('/api/emissions/calculate', routeData)
    return response.data
  },
}

/**
 * Fleet Management API (Auditor Agent)
 */
export const fleetsAPI = {
  /**
   * Get all fleets
   */
  getAll: async () => {
    const response = await apiClient.get('/api/fleets')
    return response.data
  },

  /**
   * Get prioritized fleets (hydrogen-first)
   */
  getPrioritized: async () => {
    const response = await apiClient.get('/api/fleets/prioritized')
    return response.data
  },

  /**
   * Get fleet sustainability score
   */
  getScore: async (fleetId: string) => {
    const response = await apiClient.get(`/api/fleets/${fleetId}/score`)
    return response.data
  },
}

/**
 * Health Check API
 */
export const healthAPI = {
  /**
   * Check API health
   */
  check: async () => {
    const response = await apiClient.get('/health')
    return response.data
  },
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Check if API is available
 */
export const isAPIAvailable = async (): Promise<boolean> => {
  try {
    await healthAPI.check()
    return true
  } catch (error) {
    return false
  }
}

/**
 * Format API error for display
 */
export const formatAPIError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message
  }
  if (error.message) {
    return error.message
  }
  return 'An unexpected error occurred'
}

// Export the axios instance for custom requests
export default apiClient

// Made with Bob
