import { useState, useEffect } from 'react'
import { agentsAPI } from '@/lib/api'
import type { Agent, AsyncState } from '@/types'

/**
 * Custom hook for managing agents data
 * 
 * Provides methods to fetch, start, and stop agents with loading states
 */
export function useAgents() {
  const [state, setState] = useState<AsyncState<Agent[]>>({
    data: null,
    loading: false,
    error: null,
  })

  /**
   * Fetch all agents
   */
  const fetchAgents = async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }))

    try {
      const data = await agentsAPI.getAll()
      setState({ data, loading: false, error: null })
    } catch (error: any) {
      setState({
        data: null,
        loading: false,
        error: error.message || 'Failed to fetch agents',
      })
    }
  }

  /**
   * Start an agent
   */
  const startAgent = async (agentId: string) => {
    try {
      await agentsAPI.start(agentId)
      // Refresh agents list
      await fetchAgents()
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  }

  /**
   * Stop an agent
   */
  const stopAgent = async (agentId: string) => {
    try {
      await agentsAPI.stop(agentId)
      // Refresh agents list
      await fetchAgents()
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  }

  /**
   * Fetch agents on mount
   */
  useEffect(() => {
    fetchAgents()
  }, [])

  return {
    agents: state.data,
    loading: state.loading,
    error: state.error,
    refetch: fetchAgents,
    startAgent,
    stopAgent,
  }
}

// Made with Bob
