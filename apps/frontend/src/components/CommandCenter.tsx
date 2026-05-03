'use client'

import { useState, useEffect, useRef } from 'react'
import { orchestratorAPI } from '@/lib/api'
import { OrchestratorResponse, AgentLog } from '@/types'
import gsap from 'gsap'

interface CommandCenterProps {
  onBack?: () => void
}

export default function CommandCenter({ onBack }: CommandCenterProps) {
  const [targetLocation, setTargetLocation] = useState('New York,US')
  const [isLoading, setIsLoading] = useState(false)
  const [shiftOrder, setShiftOrder] = useState<OrchestratorResponse | null>(null)
  const [agentLogs, setAgentLogs] = useState<AgentLog[]>([])
  const [error, setError] = useState<string | null>(null)
  
  const logsEndRef = useRef<HTMLDivElement>(null)
  const shiftOrderRef = useRef<HTMLDivElement>(null)

  // Auto-scroll logs to bottom
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [agentLogs])

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
    if (!targetLocation.trim()) {
      setError('Please enter a target location')
      return
    }

    setIsLoading(true)
    setError(null)
    setShiftOrder(null)
    setAgentLogs([])

    try {
      addLog('orchestrator', 'info', `Starting orchestration workflow for ${targetLocation}`)
      addLog('monitor', 'info', 'Initializing Weather Monitor Agent...')
      
      // Generic loading sequence that doesn't presume the weather
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('monitor', 'info', `Checking live weather conditions for ${targetLocation}...`)
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('auditor', 'info', 'Waking up Auditor Agent on standby...')
      
      await new Promise(resolve => setTimeout(resolve, 500))
      addLog('orchestrator', 'info', 'Awaiting watsonx API resolution...')
      
      // Call the orchestrator API
      const response = await orchestratorAPI.orchestrate(targetLocation)
      
      if (response.status === 'error') {
        throw new Error(response.error || 'Orchestration failed')
      }

      // NOW we log the actual truth based on the backend data
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
                <div>
                  <label className="block text-sm font-mono font-bold mb-2 text-neutral-400">
                    TARGET LOCATION
                  </label>
                  <input
                    type="text"
                    value={targetLocation}
                    onChange={(e) => setTargetLocation(e.target.value)}
                    placeholder="e.g., New York,US"
                    className="w-full bg-neutral-950 border-3 border-white px-4 py-3 font-mono text-lg focus:outline-none focus:border-green-400 transition-colors"
                    disabled={isLoading}
                  />
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

          {/* Right Column - Shift Order & Map */}
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

            {/* Live Map Placeholder */}
            <div className="border-4 border-white bg-neutral-900 p-6">
              <h2 className="text-2xl font-black uppercase mb-4">
                LIVE MAP
              </h2>
              
              <div className="bg-neutral-950 border-3 border-neutral-700 aspect-square flex items-center justify-center">
                <svg
                  viewBox="0 0 200 200"
                  className="w-full h-full p-8"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  {/* Grid */}
                  <line x1="0" y1="50" x2="200" y2="50" className="stroke-neutral-700" />
                  <line x1="0" y1="100" x2="200" y2="100" className="stroke-neutral-700" />
                  <line x1="0" y1="150" x2="200" y2="150" className="stroke-neutral-700" />
                  <line x1="50" y1="0" x2="50" y2="200" className="stroke-neutral-700" />
                  <line x1="100" y1="0" x2="100" y2="200" className="stroke-neutral-700" />
                  <line x1="150" y1="0" x2="150" y2="200" className="stroke-neutral-700" />
                  
                  {/* Location markers */}
                  <circle cx="60" cy="80" r="8" className="fill-green-400 stroke-green-400" />
                  <circle cx="140" cy="120" r="8" className="fill-red-400 stroke-red-400" />
                  
                  {/* Route line */}
                  <path
                    d="M 60 80 Q 100 60, 140 120"
                    className="stroke-blue-400 stroke-2 fill-none"
                    strokeDasharray="5,5"
                  />
                  
                  {/* Labels */}
                  <text x="60" y="70" className="fill-green-400 text-xs font-mono" textAnchor="middle">
                    ORIGIN
                  </text>
                  <text x="140" y="140" className="fill-red-400 text-xs font-mono" textAnchor="middle">
                    TARGET
                  </text>
                </svg>
              </div>
              
              <p className="text-xs font-mono text-neutral-500 mt-4 text-center">
                {targetLocation || 'NO LOCATION SET'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Made with Bob