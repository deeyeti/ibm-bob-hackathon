import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

/**
 * GSAP Animation Utilities for Eco-Shift
 * 
 * Reusable animation functions using GreenSock Animation Platform (GSAP)
 */

// Register GSAP plugins
if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger)
}

// ============================================================================
// Basic Animations
// ============================================================================

/**
 * Fade in animation
 */
export const fadeIn = (element: HTMLElement | null, duration: number = 0.8) => {
  if (!element) return

  gsap.from(element, {
    opacity: 0,
    duration,
    ease: 'power3.out',
  })
}

/**
 * Fade in from bottom
 */
export const fadeInUp = (element: HTMLElement | null, duration: number = 0.8, delay: number = 0) => {
  if (!element) return

  gsap.from(element, {
    y: 50,
    opacity: 0,
    duration,
    delay,
    ease: 'power3.out',
  })
}

/**
 * Fade in from top
 */
export const fadeInDown = (element: HTMLElement | null, duration: number = 0.8, delay: number = 0) => {
  if (!element) return

  gsap.from(element, {
    y: -50,
    opacity: 0,
    duration,
    delay,
    ease: 'power3.out',
  })
}

/**
 * Fade in from left
 */
export const fadeInLeft = (element: HTMLElement | null, duration: number = 0.8, delay: number = 0) => {
  if (!element) return

  gsap.from(element, {
    x: -50,
    opacity: 0,
    duration,
    delay,
    ease: 'power3.out',
  })
}

/**
 * Fade in from right
 */
export const fadeInRight = (element: HTMLElement | null, duration: number = 0.8, delay: number = 0) => {
  if (!element) return

  gsap.from(element, {
    x: 50,
    opacity: 0,
    duration,
    delay,
    ease: 'power3.out',
  })
}

/**
 * Scale in animation
 */
export const scaleIn = (element: HTMLElement | null, duration: number = 0.5) => {
  if (!element) return

  gsap.from(element, {
    scale: 0.8,
    opacity: 0,
    duration,
    ease: 'back.out(1.7)',
  })
}

// ============================================================================
// Scroll Animations
// ============================================================================

/**
 * Animate element on scroll into view
 */
export const animateOnScroll = (
  element: HTMLElement | null,
  animation: gsap.TweenVars,
  triggerOptions?: ScrollTrigger.Vars
) => {
  if (!element) return

  gsap.from(element, {
    ...animation,
    scrollTrigger: {
      trigger: element,
      start: 'top 80%',
      end: 'bottom 20%',
      toggleActions: 'play none none reverse',
      ...triggerOptions,
    },
  })
}

/**
 * Parallax scroll effect
 */
export const parallaxScroll = (element: HTMLElement | null, speed: number = 0.5) => {
  if (!element) return

  gsap.to(element, {
    y: () => window.innerHeight * speed,
    ease: 'none',
    scrollTrigger: {
      trigger: element,
      start: 'top bottom',
      end: 'bottom top',
      scrub: true,
    },
  })
}

// ============================================================================
// Card Animations
// ============================================================================

/**
 * Stagger animation for multiple elements
 */
export const staggerFadeIn = (
  elements: HTMLElement[] | NodeListOf<Element>,
  duration: number = 0.8,
  stagger: number = 0.1
) => {
  if (!elements || elements.length === 0) return

  gsap.from(elements, {
    y: 50,
    opacity: 0,
    duration,
    stagger,
    ease: 'power3.out',
  })
}

/**
 * Card hover animation
 */
export const cardHover = (element: HTMLElement | null) => {
  if (!element) return

  const tl = gsap.timeline({ paused: true })

  tl.to(element, {
    y: -8,
    boxShadow: '12px 12px 0px 0px rgba(0, 0, 0, 1)',
    duration: 0.3,
    ease: 'power2.out',
  })

  element.addEventListener('mouseenter', () => tl.play())
  element.addEventListener('mouseleave', () => tl.reverse())
}

// ============================================================================
// Data Visualization Animations
// ============================================================================

/**
 * Animate number counter
 */
export const animateCounter = (
  element: HTMLElement | null,
  endValue: number,
  duration: number = 2,
  decimals: number = 0
) => {
  if (!element) return

  const obj = { value: 0 }

  gsap.to(obj, {
    value: endValue,
    duration,
    ease: 'power2.out',
    onUpdate: () => {
      element.textContent = obj.value.toFixed(decimals)
    },
  })
}

/**
 * Animate progress bar
 */
export const animateProgressBar = (
  element: HTMLElement | null,
  percentage: number,
  duration: number = 1.5
) => {
  if (!element) return

  gsap.from(element, {
    width: '0%',
    duration,
    ease: 'power2.out',
  })

  gsap.to(element, {
    width: `${percentage}%`,
    duration,
    ease: 'power2.out',
  })
}

/**
 * Animate chart bars
 */
export const animateChartBars = (
  bars: HTMLElement[] | NodeListOf<Element>,
  duration: number = 1,
  stagger: number = 0.1
) => {
  if (!bars || bars.length === 0) return

  gsap.from(bars, {
    scaleY: 0,
    transformOrigin: 'bottom',
    duration,
    stagger,
    ease: 'power3.out',
  })
}

// ============================================================================
// Page Transitions
// ============================================================================

/**
 * Page enter animation
 */
export const pageEnter = (element: HTMLElement | null) => {
  if (!element) return

  const tl = gsap.timeline()

  tl.from(element, {
    opacity: 0,
    duration: 0.5,
    ease: 'power2.out',
  })

  return tl
}

/**
 * Page exit animation
 */
export const pageExit = (element: HTMLElement | null) => {
  if (!element) return

  const tl = gsap.timeline()

  tl.to(element, {
    opacity: 0,
    duration: 0.3,
    ease: 'power2.in',
  })

  return tl
}

// ============================================================================
// Loading Animations
// ============================================================================

/**
 * Pulse animation for loading states
 */
export const pulse = (element: HTMLElement | null) => {
  if (!element) return

  gsap.to(element, {
    scale: 1.05,
    opacity: 0.7,
    duration: 0.8,
    repeat: -1,
    yoyo: true,
    ease: 'power1.inOut',
  })
}

/**
 * Rotate animation for loading spinners
 */
export const rotate = (element: HTMLElement | null, duration: number = 1) => {
  if (!element) return

  gsap.to(element, {
    rotation: 360,
    duration,
    repeat: -1,
    ease: 'none',
  })
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Kill all animations on an element
 */
export const killAnimations = (element: HTMLElement | null) => {
  if (!element) return
  gsap.killTweensOf(element)
}

/**
 * Create a timeline for complex animations
 */
export const createTimeline = (options?: gsap.TimelineVars) => {
  return gsap.timeline(options)
}

/**
 * Set default GSAP settings
 */
export const setDefaults = () => {
  gsap.defaults({
    ease: 'power3.out',
    duration: 0.8,
  })
}

// Initialize defaults
if (typeof window !== 'undefined') {
  setDefaults()
}

// Made with Bob
