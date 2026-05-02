# Eco-Shift Frontend

Next.js 14 frontend application for the Eco-Shift supply chain orchestrator, built for the IBM Bob Hackathon.

## 🚀 Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS (Brutalist Design)
- **Animations:** GSAP (GreenSock Animation Platform)
- **HTTP Client:** Axios
- **Date Handling:** date-fns

## 📁 Project Structure

```
apps/frontend/
├── src/
│   ├── app/                    # Next.js 14 App Router
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Homepage
│   ├── components/             # React components
│   │   ├── ui/                 # Reusable UI components
│   │   ├── dashboard/          # Dashboard-specific components
│   │   ├── charts/             # Data visualization components
│   │   └── animations/         # GSAP animation components
│   ├── lib/                    # Utilities and API clients
│   │   └── api.ts              # Backend API client
│   ├── hooks/                  # Custom React hooks
│   ├── styles/                 # Global styles
│   │   └── globals.css         # Tailwind + custom styles
│   └── types/                  # TypeScript type definitions
├── public/                     # Static assets
├── tests/                      # Test files
├── .env.example                # Environment variables template
├── next.config.js              # Next.js configuration
├── tailwind.config.ts          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies
```

## 🛠️ Setup Instructions

### Prerequisites

- Node.js 18+ and npm/pnpm/yarn
- Backend API running on `http://localhost:8000` (see `apps/backend/README.md`)

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd apps/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   pnpm install
   # or
   yarn install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local` and configure:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BACKEND_URL=http://localhost:8000
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📜 Available Scripts

```bash
# Development
npm run dev          # Start development server (port 3000)

# Production
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript type checking
npm run format       # Format code with Prettier
```

## 🎨 Design System

### Brutalist Design Aesthetic

The frontend uses a **brutalist design** approach with:

- **Bold Typography:** Large, impactful headings with heavy font weights
- **High Contrast:** Strong black borders and shadows
- **Geometric Shapes:** Clean, rectangular layouts
- **Hard Shadows:** `shadow-brutal-*` utilities for depth
- **Minimal Colors:** Focus on black, white, and accent colors

### Custom Tailwind Classes

```tsx
// Buttons
<button className="btn-primary">Primary Action</button>
<button className="btn-secondary">Secondary Action</button>
<button className="btn-outline">Outline Button</button>

// Cards
<div className="card">Card with shadow</div>
<div className="card-flat">Flat card</div>

// Inputs
<input className="input" type="text" />

// Badges
<span className="badge badge-success">Success</span>
<span className="badge badge-warning">Warning</span>
<span className="badge badge-error">Error</span>

// Backgrounds
<div className="bg-grid">Grid pattern background</div>
<div className="bg-noise">Noise texture background</div>
```

### Typography Scale

```tsx
<h1 className="text-display-xl">Extra Large Display</h1>
<h1 className="text-display-lg">Large Display</h1>
<h2 className="text-display-md">Medium Display</h2>
<h3 className="text-display-sm">Small Display</h3>
```

## 🔌 API Integration

### API Client Usage

The API client is located at `src/lib/api.ts` and provides type-safe methods for backend communication.

```typescript
import { agentsAPI, weatherAPI, emissionsAPI } from '@/lib/api'

// Get all agents
const agents = await agentsAPI.getAll()

// Get current weather
const weather = await weatherAPI.getCurrent()

// Get emissions data
const emissions = await emissionsAPI.getScope3()
```

### Available API Methods

- **Agents:** `agentsAPI.getAll()`, `agentsAPI.start()`, `agentsAPI.stop()`
- **Weather:** `weatherAPI.getCurrent()`, `weatherAPI.getForecast()`, `weatherAPI.getAlerts()`
- **Vendors:** `vendorsAPI.getAll()`, `vendorsAPI.create()`, `vendorsAPI.update()`, `vendorsAPI.delete()`
- **Emissions:** `emissionsAPI.getScope3()`, `emissionsAPI.getAnalysis()`, `emissionsAPI.calculate()`
- **Fleets:** `fleetsAPI.getAll()`, `fleetsAPI.getPrioritized()`, `fleetsAPI.getScore()`

## 🎬 GSAP Animations

### Basic Animation Example

```typescript
'use client'

import { useEffect, useRef } from 'react'
import gsap from 'gsap'

export default function AnimatedComponent() {
  const elementRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(elementRef.current, {
        y: 50,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out',
      })
    })

    return () => ctx.revert()
  }, [])

  return <div ref={elementRef}>Animated Content</div>
}
```

### Animation Utilities

Create reusable animations in `src/lib/animations.ts`:

```typescript
import gsap from 'gsap'

export const fadeInUp = (element: HTMLElement) => {
  gsap.from(element, {
    y: 50,
    opacity: 0,
    duration: 0.8,
    ease: 'power3.out'
  })
}
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

## 🚢 Deployment

### Build for Production

```bash
npm run build
```

### Environment Variables for Production

Ensure these are set in your production environment:

```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
BACKEND_URL=https://your-api-domain.com
```

### Deploy to Vercel (Recommended)

1. Push your code to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy

## 📝 Development Guidelines

### Component Structure

```typescript
'use client' // Only if using client-side features

import { useState } from 'react'

interface ComponentProps {
  title: string
  // ... other props
}

export default function Component({ title }: ComponentProps) {
  const [state, setState] = useState()

  return (
    <div className="card">
      <h2>{title}</h2>
      {/* Component content */}
    </div>
  )
}
```

### Path Aliases

Use TypeScript path aliases for cleaner imports:

```typescript
import Component from '@/components/ui/Component'
import { api } from '@/lib/api'
import useCustomHook from '@/hooks/useCustomHook'
```

### Code Style

- Use TypeScript for all files
- Follow ESLint rules
- Format with Prettier
- Use functional components with hooks
- Prefer named exports for utilities, default exports for components

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
npx kill-port 3000

# Or use a different port
PORT=3001 npm run dev
```

### TypeScript Errors

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues

1. Verify backend is running on `http://localhost:8000`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Check browser console for CORS errors
4. Verify backend CORS settings allow `http://localhost:3000`

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [GSAP Documentation](https://greensock.com/docs/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run linting and type checking
4. Submit a pull request

## 📄 License

This project is part of the IBM Bob Hackathon submission.

---

**Built with ❤️ for sustainable supply chains**