'use client'

import { useState, useEffect, useRef } from 'react'
import dynamic from 'next/dynamic'
import { orchestratorAPI, chatAPI } from '@/lib/api'
import { OrchestratorResponse, AgentLog, ChatMessage } from '@/types'
import { Port, getPortById } from '@/data/world-ports'
import {
  ShippingRoute,
  getRoutesBetweenPorts,
  RouteWaypoint,
  generateStormAvoidanceRoute,
  calculateRouteDistance,
  generateGreatCircleRoute
} from '@/data/shipping-routes'
import { PortSelector } from '@/components/ui/PortSelector'
import gsap from 'gsap'
import 'leaflet/dist/leaflet.css'

// Dynamic import for Leaflet to avoid SSR issues
const MapContainer = dynamic(
  () => import('react-leaflet').then((mod) => mod.MapContainer),
  { ssr: false }
)
const TileLayer = dynamic(
  () => import('react-leaflet').then((mod) => mod.TileLayer),
  { ssr: false }
)
const Marker = dynamic(
  () => import('react-leaflet').then((mod) => mod.Marker),
  { ssr: false }
)
const Circle = dynamic(
  () => import('react-leaflet').then((mod) => mod.Circle),
  { ssr: false }
)
const Popup = dynamic(
  () => import('react-leaflet').then((mod) => mod.Popup),
  { ssr: false }
)

// Custom Geodesic component wrapper
const GeodesicLine = dynamic(
  () => import('react-leaflet').then(async (mod) => {
    const { useMap } = mod
    const L = (await import('leaflet')).default
    await import('leaflet.geodesic')
    
    // Fix for default marker icons in Next.js
    delete (L.Icon.Default.prototype as any)._getIconUrl
    L.Icon.Default.mergeOptions({
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    })
    
    return function GeodesicLineComponent({ positions, color, weight, opacity }: any) {
      const map = useMap()
      
      useEffect(() => {
        if (!map || !positions || positions.length < 2) return
        
        // Create geodesic line with wrap option for proper Pacific crossing
        const geodesic = (L as any).geodesic([positions], {
          color: color || '#00ff00',
          weight: weight || 3,
          opacity: opacity || 0.8,
          steps: 50, // Number of intermediate points for smooth curve
          wrap: true, // Enable wrapping for proper 180th meridian crossing
        })
        
        geodesic.addTo(map)
        
        // Cleanup on unmount
        return () => {
          map.removeLayer(geodesic)
        }
      }, [map, positions, color, weight, opacity])
      
      return null
    }
  }),
  { ssr: false }
)

interface CommandCenterProps {
  onBack?: () => void
}

// Fleet type definitions with emission factors (kg CO2e per nautical mile)
const FLEET_TYPES = {
  diesel: { name: 'Diesel', factor: 0.0158, color: '#ef4444' },
  hybrid: { name: 'Hybrid', factor: 0.0079, color: '#f59e0b' },
  electric: { name: 'Electric', factor: 0.0, color: '#10b981' },
  hydrogen: { name: 'Hydrogen', factor: 0.0, color: '#06b6d4' },
} as const

type FleetType = keyof typeof FLEET_TYPES

interface RouteOption {
  id: string
  name: string
  waypoints: RouteWaypoint[]
  distanceNm: number
  transitDays: number
  type: 'primary' | 'alternative' | 'eco'
  color: string
}

interface EmissionsData {
  fleetType: FleetType
  distanceNm: number
  emissionsKg: number
  emissionsPerNm: number
  baselineEmissionsKg: number
  savingsKg: number
  savingsPercent: number
}

export default function CommandCenter({ onBack }: CommandCenterProps) {
  // Logistics state - now using Port objects
  const [originPort, setOriginPort] = useState<Port | null>(getPortById('CNSHA') || null) // Shanghai
  const [destinationPort, setDestinationPort] = useState<Port | null>(getPortById('USLAX') || null) // Los Angeles
  const [selectedRoute, setSelectedRoute] = useState<ShippingRoute | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [shiftOrder, setShiftOrder] = useState<OrchestratorResponse | null>(null)
  const [agentLogs, setAgentLogs] = useState<AgentLog[]>([])
  const [error, setError] = useState<string | null>(null)
  
  // Storm simulation state
  const [stormSimulationEnabled, setStormSimulationEnabled] = useState(false)
  const [stormLocation, setStormLocation] = useState<{ lat: number; lng: number } | null>(null)
  
  // Route comparison state
  const [routeOptions, setRouteOptions] = useState<RouteOption[]>([])
  const [selectedFleetType, setSelectedFleetType] = useState<FleetType>('diesel')
  const [emissionsComparison, setEmissionsComparison] = useState<EmissionsData[]>([])
  
  // Route details state
  const [routeDetails, setRouteDetails] = useState<{
    distanceNm: number
    distanceKm: number
    transitDays: number
    transitHours: number
  } | null>(null)
  
  // Chat state
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([])
  const [chatInput, setChatInput] = useState('')
  const [isChatLoading, setIsChatLoading] = useState(false)
  
  const logsEndRef = useRef<HTMLDivElement>(null)
  const shiftOrderRef = useRef<HTMLDivElement>(null)
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll logs to bottom
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [agentLogs])

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  // Animate shift order card when it appears
  useEffect(() => {
    if (shiftOrder && shiftOrderRef.current) {
      gsap.from(shiftOrderRef.current, {
        scale: 0.95,
        opacity: 0,
        duration: 0.5,
        ease: 'power3.out',
      })
    }
  }, [shiftOrder])

  // Update selected route when ports change
  useEffect(() => {
    if (originPort && destinationPort) {
      const routes = getRoutesBetweenPorts(originPort.id, destinationPort.id)
      if (routes.length > 0) {
        setSelectedRoute(routes[0])
      } else {
        // Create a realistic great circle route if no predefined route exists
        // This follows the shortest path on a sphere (geodesic)
        const waypoints = generateGreatCircleRoute(
          originPort.coordinates.lat,
          originPort.coordinates.lng,
          destinationPort.coordinates.lat,
          destinationPort.coordinates.lng,
          8 // Generate 8 intermediate waypoints for smooth ocean curve
        )
        
        // Add port names to start and end
        waypoints[0].name = originPort.name
        waypoints[waypoints.length - 1].name = destinationPort.name
        
        // Calculate actual route distance
        const distance = calculateRouteDistance(waypoints)
        
        setSelectedRoute({
          id: `${originPort.id}-${destinationPort.id}`,
          name: `${originPort.city} to ${destinationPort.city}`,
          description: 'Great circle route (shortest ocean path)',
          originPortId: originPort.id,
          destinationPortId: destinationPort.id,
          waypoints: waypoints,
          distanceNm: Math.round(distance),
          typicalTransitDays: Math.ceil(distance / 400), // Assuming ~400 nm per day
          type: 'container',
        })
      }
    } else {
      setSelectedRoute(null)
    }
  }, [originPort, destinationPort])

  // Calculate emissions for a route with a specific fleet type
  const calculateEmissions = (distanceNm: number, fleetType: FleetType): EmissionsData => {
    const emissionFactor = FLEET_TYPES[fleetType].factor
    const emissionsKg = distanceNm * emissionFactor
    const emissionsPerNm = emissionFactor
    
    // Baseline is always diesel
    const baselineEmissionsKg = distanceNm * FLEET_TYPES.diesel.factor
    const savingsKg = baselineEmissionsKg - emissionsKg
    const savingsPercent = baselineEmissionsKg > 0 ? (savingsKg / baselineEmissionsKg) * 100 : 0
    
    return {
      fleetType,
      distanceNm,
      emissionsKg: Math.round(emissionsKg * 100) / 100,
      emissionsPerNm: Math.round(emissionsPerNm * 10000) / 10000,
      baselineEmissionsKg: Math.round(baselineEmissionsKg * 100) / 100,
      savingsKg: Math.round(savingsKg * 100) / 100,
      savingsPercent: Math.round(savingsPercent * 100) / 100,
    }
  }

  // Calculate route details (distance and transit time)
  const calculateRouteDetails = (route: ShippingRoute | null) => {
    if (!route) {
      setRouteDetails(null)
      return
    }

    const distanceNm = route.distanceNm
    const distanceKm = distanceNm * 1.852 // Convert NM to km
    
    // Calculate transit time based on average ship speed (20 knots)
    const averageSpeedKnots = 20
    const transitHours = distanceNm / averageSpeedKnots
    const transitDays = Math.floor(transitHours / 24)
    const remainingHours = Math.round(transitHours % 24)

    setRouteDetails({
      distanceNm,
      distanceKm: Math.round(distanceKm),
      transitDays,
      transitHours: remainingHours,
    })
  }

  // Generate alternative routes when storm is simulated
  const generateAlternativeRoutes = (primary: ShippingRoute, stormLat: number, stormLng: number): RouteOption[] => {
    const routes: RouteOption[] = []
    
    // Primary route (original) - marked as dangerous due to storm
    routes.push({
      id: 'primary',
      name: 'Primary Route (Storm Warning)',
      waypoints: primary.waypoints,
      distanceNm: primary.distanceNm,
      transitDays: primary.typicalTransitDays,
      type: 'primary',
      color: '#ef4444', // red - dangerous
    })
    
    // Alternative route (storm avoidance) - intelligently routes AROUND storm
    // Using the new storm avoidance algorithm
    const stormAvoidanceWaypoints = generateStormAvoidanceRoute(
      primary.waypoints,
      stormLat,
      stormLng,
      300, // Storm radius: 300 nautical miles
      200  // Safety margin: 200 nautical miles
    )
    
    // Calculate actual distance of the avoidance route
    const altDistance = Math.round(calculateRouteDistance(stormAvoidanceWaypoints))
    
    routes.push({
      id: 'alternative',
      name: 'Storm Avoidance Route',
      waypoints: stormAvoidanceWaypoints,
      distanceNm: altDistance,
      transitDays: Math.ceil((altDistance / primary.distanceNm) * primary.typicalTransitDays),
      type: 'alternative',
      color: '#f59e0b', // amber - safe alternative
    })
    
    // Eco-friendly route (optimized for emissions) - uses great circle route
    // This follows the shortest path on a sphere (geodesic)
    const origin = primary.waypoints[0]
    const destination = primary.waypoints[primary.waypoints.length - 1]
    const ecoWaypoints = generateGreatCircleRoute(
      origin.lat,
      origin.lng,
      destination.lat,
      destination.lng,
      8 // Generate 8 intermediate waypoints for smooth curve
    )
    
    // Add names to start and end points
    ecoWaypoints[0].name = origin.name
    ecoWaypoints[ecoWaypoints.length - 1].name = destination.name
    
    const ecoDistance = Math.round(calculateRouteDistance(ecoWaypoints))
    
    routes.push({
      id: 'eco',
      name: 'Eco-Optimized Route (Great Circle)',
      waypoints: ecoWaypoints,
      distanceNm: ecoDistance,
      transitDays: Math.ceil((ecoDistance / primary.distanceNm) * primary.typicalTransitDays),
      type: 'eco',
      color: '#10b981', // green
    })
    
    return routes
  }

  // Update emissions comparison when fleet type or routes change
  useEffect(() => {
    if (routeOptions.length > 0) {
      const emissions = routeOptions.map(route =>
        calculateEmissions(route.distanceNm, selectedFleetType)
      )
      setEmissionsComparison(emissions)
    }
  }, [routeOptions, selectedFleetType])

  // Update route details when selected route changes
  useEffect(() => {
    calculateRouteDetails(selectedRoute)
  }, [selectedRoute])

  // Handle storm simulation toggle
  const handleStormToggle = () => {
    const newState = !stormSimulationEnabled
    setStormSimulationEnabled(newState)
    
    if (newState && selectedRoute) {
      // Place storm at midpoint of route
      const midIndex = Math.floor(selectedRoute.waypoints.length / 2)
      const midWaypoint = selectedRoute.waypoints[midIndex]
      setStormLocation({ lat: midWaypoint.lat, lng: midWaypoint.lng })
      
      // Generate alternative routes
      const alternatives = generateAlternativeRoutes(selectedRoute, midWaypoint.lat, midWaypoint.lng)
      setRouteOptions(alternatives)
      
      addLog('monitor', 'warning', 'Storm simulation activated - generating alternative routes')
    } else {
      setStormLocation(null)
      setRouteOptions([])
      setEmissionsComparison([])
      addLog('monitor', 'info', 'Storm simulation deactivated')
    }
  }

  const addLog = (agent: 'monitor' | 'auditor' | 'orchestrator', level: AgentLog['level'], message: string) => {
    const log: AgentLog = {
      id: `${Date.now()}-${Math.random()}`,
      timestamp: new Date().toISOString(),
      agent,
      level,
      message,
    }
    setAgentLogs(prev => [...prev, log])
  }

  const handleOrchestrate = async () => {
    if (!originPort || !destinationPort) {
      setError('Please select both origin and destination ports')
      return
    }

    setIsLoading(true)
    setError(null)
    setShiftOrder(null)
    setAgentLogs([])

    try {
      const originStr = `${originPort.city},${originPort.country}`
      const destStr = `${destinationPort.city},${destinationPort.country}`
      
      addLog('orchestrator', 'info', `Starting orchestration workflow: ${originPort.name} → ${destinationPort.name}`)
      addLog('monitor', 'info', 'Initializing Weather Monitor Agent...')
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('monitor', 'info', `Checking weather conditions along route...`)
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('auditor', 'info', 'Waking up Auditor Agent on standby...')
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('orchestrator', 'info', 'Awaiting watsonx API resolution...')
      
      // Call the orchestrator API with origin and destination
      const response = await orchestratorAPI.orchestrate(originStr, destStr)
      
      if (response.status === 'error') {
        throw new Error(response.error || 'Orchestration failed')
      }

      // Log the actual results
      if (response.reroute_required) {
        addLog('monitor', 'warning', 'Severe weather confirmed. Reroute triggered.')
        addLog('auditor', 'success', `Vendor analysis complete: ${response.approved_vendor_id}`)
        addLog('orchestrator', 'success', 'Shift order generated successfully')
      } else {
        addLog('monitor', 'info', 'Weather conditions are clear')
        addLog('orchestrator', 'info', 'No reroute required')
      }

      setShiftOrder(response)
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to orchestrate'
      setError(errorMessage)
      addLog('orchestrator', 'error', `Error: ${errorMessage}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!chatInput.trim()) return

    const userMessage: ChatMessage = {
      id: `${Date.now()}-user`,
      role: 'user',
      content: chatInput,
      timestamp: new Date().toISOString(),
    }

    setChatMessages(prev => [...prev, userMessage])
    setChatInput('')
    setIsChatLoading(true)

    try {
      const response = await chatAPI.sendMessage(chatInput, shiftOrder)
      
      const assistantMessage: ChatMessage = {
        id: `${Date.now()}-assistant`,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
      }

      setChatMessages(prev => [...prev, assistantMessage])
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to get response'
      const errorMsg: ChatMessage = {
        id: `${Date.now()}-error`,
        role: 'assistant',
        content: `Error: ${errorMessage}`,
        timestamp: new Date().toISOString(),
      }
      setChatMessages(prev => [...prev, errorMsg])
    } finally {
      setIsChatLoading(false)
    }
  }

  const getLogIcon = (level: AgentLog['level']) => {
    switch (level) {
      case 'success': return '✓'
      case 'error': return '✗'
      case 'warning': return '⚠'
      default: return '→'
    }
  }

  const getLogColor = (level: AgentLog['level']) => {
    switch (level) {
      case 'success': return 'text-green-400'
      case 'error': return 'text-red-400'
      case 'warning': return 'text-yellow-400'
      default: return 'text-blue-400'
    }
  }

  const getAgentColor = (agent: AgentLog['agent']) => {
    switch (agent) {
      case 'monitor': return 'text-cyan-400'
      case 'auditor': return 'text-purple-400'
      case 'orchestrator': return 'text-orange-400'
    }
  }

  // Get route waypoints for map display
  const getRouteWaypoints = () => {
    if (selectedRoute) {
      return selectedRoute.waypoints.map(wp => [wp.lat, wp.lng] as [number, number])
    }
    return []
  }

  const routeWaypoints = getRouteWaypoints()

  return (
    <div className="min-h-screen bg-neutral-950 text-white">
      {/* Header */}
      <header className="border-b-4 border-white bg-neutral-900">
        <div className="container-brutal py-6">
          <div className="flex flex-wrap gap-3 mb-4">
            {onBack && (
              <button
                onClick={onBack}
                className="bg-white text-neutral-950 border-3 border-white px-4 py-2 font-black text-sm uppercase hover:bg-yellow-400 hover:border-yellow-400 transition-all hover:translate-x-[-2px] hover:translate-y-[-2px] shadow-[4px_4px_0px_0px_rgba(255,255,255,0.3)]"
              >
                ← BACK TO HOME
              </button>
            )}
            <a
              href="https://github.com/deeyeti/ibm-bob-hackathon"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white text-neutral-950 border-3 border-white px-4 py-2 font-black text-sm uppercase hover:bg-green-400 hover:border-green-400 transition-all hover:translate-x-[-2px] hover:translate-y-[-2px] shadow-[4px_4px_0px_0px_rgba(255,255,255,0.3)] inline-block"
            >
              📚 VIEW DOCUMENTATION
            </a>
          </div>
          <h1 className="text-4xl md:text-5xl font-black tracking-tight uppercase">
            ECO-SHIFT COMMAND CENTER
          </h1>
          <p className="text-neutral-400 font-mono text-sm mt-2">
            MULTI-AGENT LOGISTICS ORCHESTRATION SYSTEM
          </p>
        </div>
      </header>

      <div className="container-brutal py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Control Panel & Logs */}
          <div className="lg:col-span-2 space-y-6">
            {/* Control Panel */}
            <div className="border-4 border-white bg-neutral-900 p-6">
              <h2 className="text-2xl font-black uppercase mb-4 flex items-center gap-3">
                <span className="w-3 h-3 bg-green-400 animate-pulse" />
                CONTROL PANEL
              </h2>
              
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <PortSelector
                    label="ORIGIN PORT"
                    value={originPort}
                    onChange={setOriginPort}
                    placeholder="Search for origin port..."
                    className=""
                  />
                  <PortSelector
                    label="DESTINATION PORT"
                    value={destinationPort}
                    onChange={setDestinationPort}
                    placeholder="Search for destination port..."
                    className=""
                  />
                </div>

                {/* Route Info Display */}
                {selectedRoute && originPort && destinationPort && (
                  <div className="bg-neutral-950 border-2 border-neutral-700 p-4">
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <p className="text-xs font-mono text-neutral-500 mb-1">DISTANCE</p>
                        <p className="font-bold text-lg text-white">{selectedRoute.distanceNm.toLocaleString()} NM</p>
                      </div>
                      <div>
                        <p className="text-xs font-mono text-neutral-500 mb-1">TRANSIT TIME</p>
                        <p className="font-bold text-lg text-white">{selectedRoute.typicalTransitDays} days</p>
                      </div>
                      <div>
                        <p className="text-xs font-mono text-neutral-500 mb-1">ROUTE TYPE</p>
                        <p className="font-bold text-lg text-white uppercase">{selectedRoute.type}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Fleet Type Selector */}
                <div className="bg-neutral-950 border-2 border-neutral-700 p-4">
                  <p className="text-xs font-mono text-neutral-500 mb-2">FLEET TYPE</p>
                  <div className="grid grid-cols-2 gap-2">
                    {(Object.keys(FLEET_TYPES) as FleetType[]).map((type) => (
                      <button
                        key={type}
                        onClick={() => setSelectedFleetType(type)}
                        className={`px-3 py-2 font-bold text-sm uppercase border-2 transition-all ${
                          selectedFleetType === type
                            ? 'text-neutral-950 border-white'
                            : 'bg-neutral-900 text-white border-neutral-700 hover:border-white'
                        }`}
                        style={{
                          backgroundColor: selectedFleetType === type ? FLEET_TYPES[type].color : undefined,
                        }}
                      >
                        {FLEET_TYPES[type].name}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Storm Simulation Toggle */}
                <div className="bg-neutral-950 border-2 border-neutral-700 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs font-mono text-neutral-500 mb-1">STORM SIMULATION</p>
                      <p className="text-xs text-neutral-400">Test rerouting capabilities</p>
                    </div>
                    <button
                      onClick={handleStormToggle}
                      disabled={!selectedRoute}
                      className={`px-4 py-2 font-black text-sm uppercase border-2 transition-all ${
                        stormSimulationEnabled
                          ? 'bg-red-500 text-white border-red-500'
                          : 'bg-neutral-900 text-white border-neutral-700 hover:border-red-500'
                      } disabled:opacity-50 disabled:cursor-not-allowed`}
                    >
                      {stormSimulationEnabled ? '⚠ ACTIVE' : 'ACTIVATE'}
                    </button>
                  </div>
                </div>

                <button
                  onClick={handleOrchestrate}
                  disabled={isLoading}
                  className="w-full bg-white text-neutral-950 border-4 border-white px-8 py-4 font-black text-xl uppercase hover:bg-green-400 hover:border-green-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? '⟳ ORCHESTRATING...' : '▶ TRIGGER ORCHESTRATION'}
                </button>

                {error && (
                  <div className="border-3 border-red-400 bg-red-950 p-4">
                    <p className="font-mono text-red-400 text-sm">
                      <span className="font-black">ERROR:</span> {error}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Agent Activity Feed */}
            <div className="border-4 border-white bg-neutral-900 p-6">
              <h2 className="text-2xl font-black uppercase mb-4">
                AGENT ACTIVITY FEED
              </h2>
              
              <div className="bg-neutral-950 border-3 border-neutral-700 p-4 h-96 overflow-y-auto font-mono text-sm">
                {agentLogs.length === 0 ? (
                  <p className="text-neutral-600">Waiting for orchestration command...</p>
                ) : (
                  <div className="space-y-2">
                    {agentLogs.map((log) => (
                      <div key={log.id} className="flex gap-3">
                        <span className="text-neutral-600 shrink-0">
                          {new Date(log.timestamp).toLocaleTimeString()}
                        </span>
                        <span className={`${getAgentColor(log.agent)} font-bold shrink-0 uppercase`}>
                          [{log.agent}]
                        </span>
                        <span className={`${getLogColor(log.level)} shrink-0`}>
                          {getLogIcon(log.level)}
                        </span>
                        <span className="text-neutral-300">{log.message}</span>
                      </div>
                    ))}
                    <div ref={logsEndRef} />
                  </div>
                )}
              </div>

            {/* Route Comparison Panel */}
            {routeOptions.length > 0 && (
              <div className="border-4 border-green-400 bg-neutral-900 p-6">
                <h2 className="text-2xl font-black uppercase mb-4 text-green-400">
                  ROUTE COMPARISON
                </h2>
                
                <div className="space-y-4">
                  {routeOptions.map((route, index) => {
                    const emissions = emissionsComparison[index]
                    const isBest = emissions && emissions.emissionsKg === Math.min(...emissionsComparison.map(e => e.emissionsKg))
                    
                    return (
                      <div 
                        key={route.id}
                        className={`bg-neutral-950 border-2 p-4 ${
                          isBest ? 'border-green-400' : 'border-neutral-700'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center gap-2">
                            <div 
                              className="w-4 h-4 rounded-full"
                              style={{ backgroundColor: route.color }}
                            />
                            <h3 className="font-black text-lg uppercase">{route.name}</h3>
                            {isBest && (
                              <span className="bg-green-400 text-neutral-950 px-2 py-1 text-xs font-black uppercase">
                                BEST ECO
                              </span>
                            )}
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-3 text-sm">
                          <div>
                            <p className="text-neutral-500 text-xs mb-1">DISTANCE</p>
                            <p className="font-bold text-white">{route.distanceNm.toLocaleString()} NM</p>
                          </div>
                          <div>
                            <p className="text-neutral-500 text-xs mb-1">TRANSIT</p>
                            <p className="font-bold text-white">{route.transitDays} days</p>
                          </div>
                          {emissions && (
                            <>
                              <div>
                                <p className="text-neutral-500 text-xs mb-1">EMISSIONS</p>
                                <p className="font-bold text-white">{emissions.emissionsKg.toLocaleString()} kg CO2e</p>
                              </div>
                              <div>
                                <p className="text-neutral-500 text-xs mb-1">SAVINGS</p>
                                <p className={`font-bold ${emissions.savingsPercent > 0 ? 'text-green-400' : 'text-red-400'}`}>
                                  {emissions.savingsPercent > 0 ? '-' : '+'}{Math.abs(emissions.savingsPercent).toFixed(1)}%
                                </p>
                              </div>
                            </>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Emissions Comparison Visualization */}
            {emissionsComparison.length > 0 && (
              <div className="border-4 border-white bg-neutral-900 p-6">
                <h2 className="text-2xl font-black uppercase mb-4">
                  EMISSIONS ANALYSIS
                </h2>
                
                <div className="space-y-4">
                  {/* Fleet Type Info */}
                  <div className="bg-neutral-950 border-2 border-neutral-700 p-4">
                    <p className="text-xs font-mono text-neutral-500 mb-2">SELECTED FLEET</p>
                    <div className="flex items-center gap-3">
                      <div 
                        className="w-6 h-6 rounded"
                        style={{ backgroundColor: FLEET_TYPES[selectedFleetType].color }}
                      />
                      <p className="font-black text-xl uppercase">{FLEET_TYPES[selectedFleetType].name}</p>
                    </div>
                  </div>

                  {/* Emissions Bar Chart */}
                  <div className="bg-neutral-950 border-2 border-neutral-700 p-4">
                    <p className="text-xs font-mono text-neutral-500 mb-3">EMISSIONS COMPARISON (kg CO2e)</p>
                    <div className="space-y-3">
                      {emissionsComparison.map((emission, index) => {
                        const route = routeOptions[index]
                        const maxEmissions = Math.max(...emissionsComparison.map(e => e.emissionsKg))
                        const barWidth = (emission.emissionsKg / maxEmissions) * 100
                        
                        return (
                          <div key={route.id}>
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs font-mono text-neutral-400">{route.name}</span>
                              <span className="text-xs font-bold text-white">{emission.emissionsKg.toLocaleString()} kg</span>
                            </div>
                            <div className="w-full bg-neutral-800 h-6 relative">
                              <div 
                                className="h-full transition-all duration-500"
                                style={{ 
                                  width: `${barWidth}%`,
                                  backgroundColor: route.color
                                }}
                              />
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>

                  {/* Total Savings */}
                  {emissionsComparison.length > 1 && (
                    <div className="bg-green-950 border-2 border-green-400 p-4">
                      <p className="text-xs font-mono text-green-400 mb-2">POTENTIAL SAVINGS</p>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <p className="text-xs text-neutral-400 mb-1">Best Route Emissions</p>
                          <p className="font-black text-2xl text-white">
                            {Math.min(...emissionsComparison.map(e => e.emissionsKg)).toLocaleString()} kg
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-neutral-400 mb-1">vs Diesel Baseline</p>
                          <p className="font-black text-2xl text-green-400">
                            -{Math.max(...emissionsComparison.map(e => e.savingsPercent)).toFixed(1)}%
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
            </div>
          </div>

          {/* Right Column - Shift Order, Route Details & Map */}
          <div className="space-y-6">
            {/* Shift Order Card */}
            {shiftOrder && shiftOrder.reroute_required && (
              <div ref={shiftOrderRef} className="border-4 border-green-400 bg-neutral-900 p-6">
                <h2 className="text-2xl font-black uppercase mb-4 text-green-400">
                  ✓ SHIFT ORDER APPROVED
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-mono text-neutral-500 mb-1">WORKFLOW ID</p>
                    <p className="font-mono text-sm text-white break-all">{shiftOrder.workflow_id}</p>
                  </div>

                  <div className="border-t-2 border-neutral-700 pt-4">
                    <p className="text-xs font-mono text-neutral-500 mb-1">APPROVED VENDOR</p>
                    <p className="font-black text-2xl text-green-400">{shiftOrder.approved_vendor_id}</p>
                  </div>

                  <div>
                    <p className="text-xs font-mono text-neutral-500 mb-1">EMISSIONS SAVING</p>
                    <p className="font-bold text-lg text-white">{shiftOrder.emissions_saving}</p>
                  </div>

                  <div className="border-t-2 border-neutral-700 pt-4">
                    <p className="text-xs font-mono text-neutral-500 mb-2">AI JUSTIFICATION</p>
                    <p className="text-sm text-neutral-300 leading-relaxed">
                      {shiftOrder.justification}
                    </p>
                  </div>

                  <div className="border-t-2 border-neutral-700 pt-4">
                    <p className="text-xs font-mono text-neutral-500 mb-1">TIMESTAMP</p>
                    <p className="font-mono text-xs text-neutral-400">
                      {new Date(shiftOrder.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {shiftOrder && !shiftOrder.reroute_required && (
              <div ref={shiftOrderRef} className="border-4 border-blue-400 bg-neutral-900 p-6">
                <h2 className="text-2xl font-black uppercase mb-4 text-blue-400">
                  ℹ NO REROUTE REQUIRED
                </h2>
                <p className="text-neutral-300">
                  {shiftOrder.weather_status || 'Weather conditions are clear. Current routes are optimal.'}
                </p>
                <div className="mt-4 border-t-2 border-neutral-700 pt-4">
                  <p className="text-xs font-mono text-neutral-500 mb-1">WEATHER STATUS</p>
                  <p className="font-mono text-sm text-white">
                    {shiftOrder.weather_status || 'Clear'}
                  </p>
                </div>
              </div>
            )}

            {/* Show rerouting status when storm is active but orchestration hasn't been triggered */}
            {stormSimulationEnabled && !shiftOrder && (
              <div className="border-4 border-red-400 bg-neutral-900 p-6">
                <h2 className="text-2xl font-black uppercase mb-4 text-red-400">
                  ⚠ ACTIVELY REROUTING
                </h2>
                <p className="text-neutral-300">
                  Storm detected on primary route. Alternative routes are being evaluated.
                </p>
                <div className="mt-4 border-t-2 border-neutral-700 pt-4">
                  <p className="text-xs font-mono text-neutral-500 mb-1">REROUTE REASON</p>
                  <p className="font-mono text-sm text-white">Storm Simulation Active</p>
                </div>
              </div>
            )}

            {/* Route Details Card - Show when route is selected */}
            {routeDetails && (
              <div className="border-4 border-white bg-neutral-900 p-6">
                <h2 className="text-2xl font-black uppercase mb-4">
                  ROUTE DETAILS
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-mono text-neutral-500 mb-1">DISTANCE</p>
                    <p className="font-bold text-lg text-white">
                      {routeDetails.distanceNm.toLocaleString()} NM ({routeDetails.distanceKm.toLocaleString()} km)
                    </p>
                  </div>
                  <div>
                    <p className="text-xs font-mono text-neutral-500 mb-1">TRANSIT TIME</p>
                    <p className="font-bold text-lg text-white">
                      {routeDetails.transitDays} days, {routeDetails.transitHours} hours
                    </p>
                  </div>
                  {selectedRoute && (
                    <div>
                      <p className="text-xs font-mono text-neutral-500 mb-1">ROUTE TYPE</p>
                      <p className="font-bold text-lg text-white uppercase">{selectedRoute.type}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Live Map */}
            <div className="border-4 border-white bg-neutral-900 p-6">
              <h2 className="text-2xl font-black uppercase mb-4">
                LIVE MAP
              </h2>
              
              <div className="bg-neutral-950 border-3 border-neutral-700 aspect-square">
                <MapContainer
                  center={[20, 0]}
                  zoom={2}
                  style={{ height: '100%', width: '100%' }}
                  className="z-0"
                  worldCopyJump={true}
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  />
                  
                  {originPort && destinationPort && (
                    <>
                      {/* Origin Marker */}
                      <Marker position={[originPort.coordinates.lat, originPort.coordinates.lng]} />
                      
                      {/* Destination Marker */}
                      <Marker position={[destinationPort.coordinates.lat, destinationPort.coordinates.lng]} />
                      
                      {/* Multiple Routes Display */}
                      {routeOptions.length > 0 ? (
                        // Show all route options when storm simulation is active
                        routeOptions.map((route) => (
                          <GeodesicLine
                            key={route.id}
                            positions={route.waypoints.map(wp => [wp.lat, wp.lng] as [number, number])}
                            color={route.color}
                            weight={route.type === 'primary' ? 2 : 3}
                            opacity={route.type === 'primary' ? 0.5 : 0.8}
                          />
                        ))
                      ) : (
                        // Show single route when no storm simulation
                        routeWaypoints.length > 0 && (
                          <GeodesicLine
                            positions={routeWaypoints}
                            color={shiftOrder?.reroute_required ? "#00ff00" : "#3b82f6"}
                            weight={3}
                            opacity={0.8}
                          />
                        )
                      )}
                      
                      {/* Storm Marker and Danger Zone */}
                      {stormSimulationEnabled && stormLocation && (
                        <>
                          {/* Storm Danger Zone (Red Circle) */}
                          <Circle
                            center={[stormLocation.lat, stormLocation.lng]}
                            radius={500000} // 500km radius in meters
                            pathOptions={{
                              color: '#ef4444',
                              fillColor: '#ef4444',
                              fillOpacity: 0.2,
                              weight: 2,
                            }}
                          />
                          
                          {/* Storm Marker */}
                          <Marker
                            position={[stormLocation.lat, stormLocation.lng]}
                          >
                            <Popup>
                              <div className="text-center">
                                <p className="font-black text-red-600">⚠ SEVERE STORM</p>
                                <p className="text-xs">Danger Zone: 500km radius</p>
                              </div>
                            </Popup>
                          </Marker>
                        </>
                      )}
                    </>
                  )}
                </MapContainer>
              </div>
              
              {/* Map Legend */}
              {routeOptions.length > 0 && (
                <div className="mt-4 bg-neutral-950 border-2 border-neutral-700 p-3">
                  <p className="text-xs font-mono text-neutral-500 mb-2">ROUTE LEGEND</p>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {routeOptions.map((route) => (
                      <div key={route.id} className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: route.color }}
                        />
                        <span className="text-neutral-300">{route.name}</span>
                      </div>
                    ))}
                    {stormSimulationEnabled && (
                      <div className="flex items-center gap-2 col-span-2">
                        <div className="w-3 h-3 rounded-full bg-red-500" />
                        <span className="text-neutral-300">Storm Zone (500km)</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              <p className="text-xs font-mono text-neutral-500 mt-4 text-center">
                {originPort && destinationPort
                  ? `${originPort.code} (${originPort.city}) → ${destinationPort.code} (${destinationPort.city})`
                  : 'NO ROUTE SET'}
              </p>
              {selectedRoute && !stormSimulationEnabled && (
                <p className="text-xs font-mono text-neutral-400 mt-1 text-center">
                  {selectedRoute.name}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* AI Logistics Consultant Drawer */}
      <div className={`fixed bottom-4 right-4 z-50 transition-all duration-300 ${isChatOpen ? 'w-96 h-96' : 'w-auto h-auto'}`}>
        {!isChatOpen ? (
          <button
            onClick={() => setIsChatOpen(true)}
            className="bg-white text-neutral-950 border-4 border-white px-6 py-3 font-black text-sm uppercase hover:bg-green-400 hover:border-green-400 transition-all shadow-[4px_4px_0px_0px_rgba(255,255,255,0.3)]"
          >
            🤖 AI CONSULTANT
          </button>
        ) : (
          <div className="bg-neutral-900 border-4 border-white h-full flex flex-col">
            {/* Chat Header */}
            <div className="border-b-3 border-white p-4 flex justify-between items-center">
              <h3 className="font-black text-sm uppercase">AI LOGISTICS CONSULTANT</h3>
              <button
                onClick={() => setIsChatOpen(false)}
                className="text-white hover:text-red-400 font-black text-lg"
              >
                ✕
              </button>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 bg-neutral-950 font-mono text-sm">
              {chatMessages.length === 0 ? (
                <p className="text-neutral-600">Ask me about logistics optimization, emissions reduction, or routing decisions...</p>
              ) : (
                <div className="space-y-3">
                  {chatMessages.map((message) => (
                    <div key={message.id} className={`${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                      <div className={`inline-block max-w-[80%] p-2 border-2 ${
                        message.role === 'user' 
                          ? 'bg-green-400 text-neutral-950 border-green-400' 
                          : 'bg-neutral-800 text-white border-neutral-600'
                      }`}>
                        <p className="text-xs font-bold mb-1 uppercase">
                          {message.role === 'user' ? 'YOU' : 'AI CONSULTANT'}
                        </p>
                        <p className="text-sm leading-relaxed">{message.content}</p>
                      </div>
                    </div>
                  ))}
                  {isChatLoading && (
                    <div className="text-left">
                      <div className="inline-block bg-neutral-800 text-white border-2 border-neutral-600 p-2">
                        <p className="text-xs font-bold mb-1 uppercase">AI CONSULTANT</p>
                        <p className="text-sm">Thinking...</p>
                      </div>
                    </div>
                  )}
                  <div ref={chatEndRef} />
                </div>
              )}
            </div>

            {/* Chat Input */}
            <div className="border-t-3 border-white p-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask about logistics..."
                  className="flex-1 bg-neutral-950 border-2 border-white px-3 py-2 font-mono text-sm focus:outline-none focus:border-green-400 transition-colors"
                  disabled={isChatLoading}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isChatLoading || !chatInput.trim()}
                  className="bg-white text-neutral-950 border-2 border-white px-3 py-2 font-black text-sm hover:bg-green-400 hover:border-green-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  →
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Made with Bob