'use client'

import { useState, useEffect, useRef } from 'react'
import dynamic from 'next/dynamic'
import { orchestratorAPI, chatAPI } from '@/lib/api'
import { OrchestratorResponse, AgentLog, ChatMessage } from '@/types'
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

export default function CommandCenter({ onBack }: CommandCenterProps) {
  // Logistics state
  const [originPort, setOriginPort] = useState('Shanghai,CN')
  const [destinationPort, setDestinationPort] = useState('Los Angeles,US')
  const [isLoading, setIsLoading] = useState(false)
  const [shiftOrder, setShiftOrder] = useState<OrchestratorResponse | null>(null)
  const [agentLogs, setAgentLogs] = useState<AgentLog[]>([])
  const [error, setError] = useState<string | null>(null)
  
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
    if (!originPort.trim() || !destinationPort.trim()) {
      setError('Please enter both origin and destination ports')
      return
    }

    setIsLoading(true)
    setError(null)
    setShiftOrder(null)
    setAgentLogs([])

    try {
      addLog('orchestrator', 'info', `Starting orchestration workflow: ${originPort} → ${destinationPort}`)
      addLog('monitor', 'info', 'Initializing Weather Monitor Agent...')
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('monitor', 'info', `Checking weather conditions along route...`)
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('auditor', 'info', 'Waking up Auditor Agent on standby...')
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('orchestrator', 'info', 'Awaiting watsonx API resolution...')
      
      // Call the orchestrator API with origin and destination
      const response = await orchestratorAPI.orchestrate(originPort, destinationPort)
      
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

  // Get coordinates for map (mock data for now, will come from API)
  const getRouteCoordinates = () => {
    if (shiftOrder?.route_details?.origin_coords && shiftOrder?.route_details?.destination_coords) {
      return {
        origin: shiftOrder.route_details.origin_coords,
        destination: shiftOrder.route_details.destination_coords,
      }
    }
    // Default mock coordinates
    return {
      origin: [31.2304, 121.4737] as [number, number], // Shanghai
      destination: [34.0522, -118.2437] as [number, number], // Los Angeles
    }
  }

  const routeCoords = getRouteCoordinates()

  return (
    <div className="min-h-screen bg-neutral-950 text-white">
      {/* Header */}
      <header className="border-b-4 border-white bg-neutral-900">
        <div className="container-brutal py-6">
          {onBack && (
            <button
              onClick={onBack}
              className="mb-4 bg-white text-neutral-950 border-3 border-white px-4 py-2 font-black text-sm uppercase hover:bg-yellow-400 hover:border-yellow-400 transition-all hover:translate-x-[-2px] hover:translate-y-[-2px] shadow-[4px_4px_0px_0px_rgba(255,255,255,0.3)]"
            >
              ← BACK TO HOME
            </button>
          )}
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
                  <div>
                    <label className="block text-sm font-mono font-bold mb-2 text-neutral-400">
                      ORIGIN PORT
                    </label>
                    <input
                      type="text"
                      value={originPort}
                      onChange={(e) => setOriginPort(e.target.value)}
                      placeholder="e.g., Shanghai,CN"
                      className="w-full bg-neutral-950 border-3 border-white px-4 py-3 font-mono text-lg focus:outline-none focus:border-green-400 transition-colors"
                      disabled={isLoading}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-mono font-bold mb-2 text-neutral-400">
                      DESTINATION PORT
                    </label>
                    <input
                      type="text"
                      value={destinationPort}
                      onChange={(e) => setDestinationPort(e.target.value)}
                      placeholder="e.g., Los Angeles,US"
                      className="w-full bg-neutral-950 border-3 border-white px-4 py-3 font-mono text-lg focus:outline-none focus:border-green-400 transition-colors"
                      disabled={isLoading}
                    />
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
                  Weather conditions are clear. Current routes are optimal.
                </p>
                <div className="mt-4 border-t-2 border-neutral-700 pt-4">
                  <p className="text-xs font-mono text-neutral-500 mb-1">WEATHER STATUS</p>
                  <p className="font-mono text-sm text-white">{shiftOrder.weather_status}</p>
                </div>
              </div>
            )}

            {/* Route Details Card */}
            {shiftOrder?.route_details && (
              <div className="border-4 border-white bg-neutral-900 p-6">
                <h2 className="text-2xl font-black uppercase mb-4">
                  ROUTE DETAILS
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-mono text-neutral-500 mb-1">DISTANCE</p>
                    <p className="font-bold text-lg text-white">{shiftOrder.route_details.distance} km</p>
                  </div>
                  <div>
                    <p className="text-xs font-mono text-neutral-500 mb-1">ESTIMATED TIME OF ARRIVAL</p>
                    <p className="font-bold text-lg text-white">{shiftOrder.route_details.eta}</p>
                  </div>
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
                  
                  {shiftOrder && (
                    <>
                      {/* Origin Marker */}
                      <Marker position={routeCoords.origin} />
                      
                      {/* Destination Marker */}
                      <Marker position={routeCoords.destination} />
                      
                      {/* Geodesic Route Line - Curved path for global shipping */}
                      <GeodesicLine
                        positions={[routeCoords.origin, routeCoords.destination]}
                        color="#00ff00"
                        weight={3}
                        opacity={0.8}
                      />
                    </>
                  )}
                </MapContainer>
              </div>
              
              <p className="text-xs font-mono text-neutral-500 mt-4 text-center">
                {originPort && destinationPort ? `${originPort} → ${destinationPort}` : 'NO ROUTE SET'}
              </p>
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