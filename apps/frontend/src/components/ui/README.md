# UI Components

This directory contains reusable UI components that follow the brutalist design system.

## Component Guidelines

- All components should be typed with TypeScript
- Use Tailwind CSS utility classes
- Follow the brutalist design aesthetic (bold, high contrast, geometric)
- Include JSDoc comments for props
- Export components as default exports

## Example Component Structure

```tsx
interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'outline'
  onClick?: () => void
  disabled?: boolean
}

export default function Button({ 
  children, 
  variant = 'primary',
  onClick,
  disabled = false 
}: ButtonProps) {
  return (
    <button 
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}
```

## Planned Components

- Button
- Card
- Input
- Badge
- Modal
- Dropdown
- Tooltip
- Loading Spinner
- Progress Bar
- Alert/Notification