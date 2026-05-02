'use client'

import { useEffect, useRef } from 'react'
import gsap from 'gsap'

export default function Home() {
  const heroRef = useRef<HTMLDivElement>(null)
  const titleRef = useRef<HTMLHeadingElement>(null)
  const subtitleRef = useRef<HTMLParagraphElement>(null)

  useEffect(() => {
    // GSAP animations on mount
    const ctx = gsap.context(() => {
      gsap.from(titleRef.current, {
        y: 50,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out',
      })

      gsap.from(subtitleRef.current, {
        y: 30,
        opacity: 0,
        duration: 0.8,
        delay: 0.2,
        ease: 'power3.out',
      })
    }, heroRef)

    return () => ctx.revert()
  }, [])

  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section ref={heroRef} className="container-brutal py-20 md:py-32">
        <div className="max-w-4xl">
          {/* Badge */}
          <div className="mb-8 inline-block">
            <span className="badge badge-success">
              IBM Bob Hackathon 2024
            </span>
          </div>

          {/* Title */}
          <h1 
            ref={titleRef}
            className="text-display-lg md:text-display-xl mb-6 font-display"
          >
            Eco-Shift
          </h1>

          {/* Subtitle */}
          <p 
            ref={subtitleRef}
            className="text-2xl md:text-3xl font-bold text-neutral-700 mb-8 max-w-2xl"
          >
            AI-Powered Supply Chain Orchestrator for Sustainable Logistics
          </p>

          {/* Description */}
          <div className="card max-w-2xl mb-12">
            <p className="text-lg text-neutral-600 mb-4">
              Multi-agent system leveraging IBM watsonx.ai and BeeAI framework to optimize 
              supply chain operations, track Scope 3 emissions, and prioritize sustainable 
              transportation solutions.
            </p>
            <div className="divider-brutal" />
            <div className="flex flex-wrap gap-3">
              <span className="badge bg-neutral-900 text-white">IBM watsonx.ai</span>
              <span className="badge bg-neutral-900 text-white">BeeAI Framework</span>
              <span className="badge bg-neutral-900 text-white">Next.js 14</span>
              <span className="badge bg-neutral-900 text-white">Python FastAPI</span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-wrap gap-4">
            <button className="btn-primary">
              Launch Dashboard
            </button>
            <button className="btn-outline">
              View Documentation
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container-brutal py-20 bg-white">
        <h2 className="text-display-sm mb-12 font-display">Key Features</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Feature 1 */}
          <div className="card">
            <div className="text-4xl mb-4">🌦️</div>
            <h3 className="text-2xl font-bold mb-3">Weather Monitoring</h3>
            <p className="text-neutral-600">
              Real-time weather tracking with OpenWeather API integration for 
              proactive supply chain adjustments.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="card">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-2xl font-bold mb-3">Emissions Tracking</h3>
            <p className="text-neutral-600">
              Comprehensive Scope 3 emissions calculation and analysis for 
              sustainable decision-making.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="card">
            <div className="text-4xl mb-4">🚛</div>
            <h3 className="text-2xl font-bold mb-3">Fleet Prioritization</h3>
            <p className="text-neutral-600">
              Intelligent prioritization of hydrogen-fueled and eco-friendly 
              transportation options.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="card">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-2xl font-bold mb-3">AI Agents</h3>
            <p className="text-neutral-600">
              Multi-agent orchestration using BeeAI framework for autonomous 
              supply chain management.
            </p>
          </div>

          {/* Feature 5 */}
          <div className="card">
            <div className="text-4xl mb-4">💡</div>
            <h3 className="text-2xl font-bold mb-3">Smart Recommendations</h3>
            <p className="text-neutral-600">
              AI-powered insights using IBM watsonx.ai Granite-3.0-8b model 
              for optimization strategies.
            </p>
          </div>

          {/* Feature 6 */}
          <div className="card">
            <div className="text-4xl mb-4">📈</div>
            <h3 className="text-2xl font-bold mb-3">Real-time Analytics</h3>
            <p className="text-neutral-600">
              Live dashboard with interactive visualizations and performance 
              metrics tracking.
            </p>
          </div>
        </div>
      </section>

      {/* Status Section */}
      <section className="container-brutal py-20">
        <div className="card-flat bg-primary-100 border-primary-500">
          <h2 className="text-display-sm mb-6 font-display">System Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="text-sm font-mono text-neutral-600 mb-2">FRONTEND</div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-primary-500 rounded-full animate-pulse" />
                <span className="font-bold">Ready</span>
              </div>
            </div>
            <div>
              <div className="text-sm font-mono text-neutral-600 mb-2">BACKEND</div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                <span className="font-bold">Pending Setup</span>
              </div>
            </div>
            <div>
              <div className="text-sm font-mono text-neutral-600 mb-2">AGENTS</div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                <span className="font-bold">Pending Setup</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="container-brutal py-12 border-t-3 border-neutral-900">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="font-mono text-sm text-neutral-600">
            © 2024 Eco-Shift. Built for IBM Bob Hackathon.
          </p>
          <div className="flex gap-4">
            <a href="#" className="font-mono text-sm hover:text-primary-600 transition-colors">
              GitHub
            </a>
            <a href="#" className="font-mono text-sm hover:text-primary-600 transition-colors">
              Documentation
            </a>
            <a href="#" className="font-mono text-sm hover:text-primary-600 transition-colors">
              API
            </a>
          </div>
        </div>
      </footer>
    </main>
  )
}

// Made with Bob
