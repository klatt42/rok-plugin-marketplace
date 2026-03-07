---
name: ui-animation
description: |
  Cinema-quality animation patterns for apps, dashboards, and landing pages.
  Covers Framer Motion spring physics, scroll-triggered reveals, glassmorphism
  nav, Lenis smooth scroll, data table animations, sidebar transitions, modal
  entrances, toast notifications, and reduced-motion accessibility. Extended
  from genesis-landing-page-pro with app-specific patterns.
triggers:
  - "animation patterns"
  - "framer motion"
  - "scroll triggered"
  - "glassmorphism"
  - "dashboard animations"
  - "app polish"
version: 1.0
author: ROK Agency
---

# UI Animation - Cinema-Quality Patterns (Extended)

## Animation Library Stack

| Library | Role | Install |
|---------|------|---------|
| Framer Motion | Component animations, spring physics | `npm i framer-motion` |
| Lenis | Smooth scroll physics | `npm i lenis` |
| GSAP + ScrollTrigger | Complex timeline sequences | `npm i gsap` (optional) |

## Foundation: Reduced Motion

ALWAYS add this to any file using animations:

```typescript
import { useReducedMotion } from 'framer-motion'

const prefersReducedMotion = useReducedMotion()

// Conditional animation props
const animateProps = prefersReducedMotion
  ? {}
  : { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 } }
```

## Page-Level Patterns

### Hero Entrance (Staggered Words)

```typescript
const heroWords = headline.split(' ')

<div className="overflow-hidden">
  {heroWords.map((word, i) => (
    <motion.span
      key={i}
      className="inline-block mr-3"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.6,
        delay: i * 0.08,
        ease: [0.22, 1, 0.36, 1],
      }}
    >
      {word}
    </motion.span>
  ))}
</div>
```

### Section Reveal (Scroll-Triggered)

```typescript
const ref = useRef(null)
const isInView = useInView(ref, { once: true, margin: '-100px' })

<motion.section
  ref={ref}
  initial={{ opacity: 0, y: 40 }}
  animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
  transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
>
```

### Feature Cards (Staggered Grid)

```typescript
const container = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
}

const card = {
  hidden: { opacity: 0, scale: 0.95, y: 20 },
  visible: { opacity: 1, scale: 1, y: 0, transition: { duration: 0.5 } }
}

<motion.div
  variants={container}
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
  className="grid grid-cols-1 md:grid-cols-3 gap-6"
>
  {features.map((f) => (
    <motion.div key={f.name} variants={card}>
      {/* card content */}
    </motion.div>
  ))}
</motion.div>
```

## App-Specific Patterns

### Dashboard Metric Cards (Counter Animation)

```typescript
const container = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
}

const metricCard = {
  hidden: { opacity: 0, y: 16, scale: 0.98 },
  visible: {
    opacity: 1, y: 0, scale: 1,
    transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] }
  }
}

<motion.div
  variants={container}
  initial="hidden"
  animate="visible"
  className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
>
  {metrics.map((m) => (
    <motion.div
      key={m.label}
      variants={metricCard}
      whileHover={{ y: -2, shadow: '0 8px 24px rgba(0,0,0,0.08)' }}
      className="p-6 rounded-xl bg-white border border-gray-100 shadow-sm"
    >
      {/* metric content */}
    </motion.div>
  ))}
</motion.div>
```

### Sidebar Navigation

```typescript
// Sidebar slide-in on mount
<motion.aside
  initial={{ x: -240, opacity: 0 }}
  animate={{ x: 0, opacity: 1 }}
  transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
  className="w-60 h-screen bg-gray-50 border-r border-gray-200"
>
  {/* Nav items with hover indicator */}
  {navItems.map((item) => (
    <motion.a
      key={item.href}
      href={item.href}
      whileHover={{ x: 4, backgroundColor: 'rgba(59,130,246,0.06)' }}
      transition={{ duration: 0.15 }}
      className="flex items-center gap-3 px-4 py-2.5 text-sm rounded-lg"
    >
      {item.icon}
      {item.label}
    </motion.a>
  ))}
</motion.aside>
```

### Data Table Rows

```typescript
// Table body with staggered row entrance
<motion.tbody
  initial="hidden"
  animate="visible"
  variants={{
    hidden: {},
    visible: { transition: { staggerChildren: 0.03 } }
  }}
>
  {rows.map((row) => (
    <motion.tr
      key={row.id}
      variants={{
        hidden: { opacity: 0, x: -8 },
        visible: { opacity: 1, x: 0, transition: { duration: 0.25 } }
      }}
      whileHover={{ backgroundColor: 'rgba(59,130,246,0.04)' }}
      transition={{ duration: 0.1 }}
      className="border-b border-gray-100"
    >
      {/* cells */}
    </motion.tr>
  ))}
</motion.tbody>
```

### Modal/Dialog Entrance

```typescript
<AnimatePresence>
  {isOpen && (
    <>
      {/* Backdrop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
        onClick={onClose}
      />
      {/* Modal */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 10 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 10 }}
        transition={{ type: 'spring', stiffness: 400, damping: 30 }}
        className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2
                   z-50 w-full max-w-lg bg-white rounded-2xl shadow-2xl p-6"
      >
        {children}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

### Toast Notification

```typescript
<AnimatePresence>
  {toasts.map((toast) => (
    <motion.div
      key={toast.id}
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -10, scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white
                 shadow-lg border border-gray-100"
    >
      {toast.icon}
      <span className="text-sm font-medium">{toast.message}</span>
    </motion.div>
  ))}
</AnimatePresence>
```

### Loading Skeleton Pulse

```typescript
// Shimmer skeleton for loading states
<div className="animate-pulse space-y-3">
  <div className="h-4 bg-gray-200 rounded-lg w-3/4" />
  <div className="h-4 bg-gray-200 rounded-lg w-1/2" />
  <div className="h-32 bg-gray-200 rounded-xl" />
</div>
```

### Tabs/Segment Control

```typescript
<div className="relative flex gap-1 p-1 rounded-lg bg-gray-100">
  {tabs.map((tab) => (
    <button
      key={tab.id}
      onClick={() => setActiveTab(tab.id)}
      className="relative z-10 px-4 py-2 text-sm font-medium rounded-md"
    >
      {activeTab === tab.id && (
        <motion.div
          layoutId="activeTab"
          className="absolute inset-0 bg-white rounded-md shadow-sm"
          transition={{ type: 'spring', stiffness: 400, damping: 30 }}
        />
      )}
      <span className="relative z-10">{tab.label}</span>
    </button>
  ))}
</div>
```

## Interactive Patterns

### Button Interactions

```typescript
<motion.button
  whileHover={{ scale: 1.02, y: -1 }}
  whileTap={{ scale: 0.97 }}
  transition={{ type: 'spring', stiffness: 400, damping: 17 }}
  className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold
             focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
>
```

### Card Hover (Lift + Shadow)

```typescript
<motion.div
  whileHover={{ y: -4, boxShadow: '0 20px 40px rgba(0,0,0,0.1)' }}
  transition={{ type: 'spring', stiffness: 300, damping: 20 }}
  className="p-6 rounded-xl bg-white border border-gray-100 shadow-sm"
>
```

### Link Underline Animation

```typescript
<a className="relative group">
  Link Text
  <span className="absolute bottom-0 left-0 h-px bg-blue-600
                   w-0 group-hover:w-full transition-all duration-300" />
</a>
```

## Navigation Patterns

### Glassmorphism Nav

```typescript
<motion.nav
  initial={{ y: -80, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
  className="sticky top-0 z-50 backdrop-blur-xl bg-white/80 dark:bg-gray-900/80
             border-b border-gray-200/50 dark:border-white/10"
>
  <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    <span className="font-bold text-xl">{productName}</span>
    <div className="flex items-center gap-4">
      {/* nav items */}
    </div>
  </div>
</motion.nav>
```

### Sticky CTA Bar

```typescript
const heroRef = useRef<HTMLDivElement>(null)
const [showStickyBar, setShowStickyBar] = useState(false)

useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => setShowStickyBar(!entry.isIntersecting),
    { threshold: 0 }
  )
  if (heroRef.current) observer.observe(heroRef.current)
  return () => observer.disconnect()
}, [])

<AnimatePresence>
  {showStickyBar && (
    <motion.div
      initial={{ y: 80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ y: 80, opacity: 0 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50
                 backdrop-blur-xl bg-gray-900/90 text-white
                 px-6 py-3 rounded-full shadow-2xl flex items-center gap-4"
    >
```

## Lenis Smooth Scroll

```typescript
'use client'
import Lenis from 'lenis'
import { useEffect } from 'react'

export function SmoothScrollProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    })
    function raf(time: number) {
      lenis.raf(time)
      requestAnimationFrame(raf)
    }
    requestAnimationFrame(raf)
    return () => lenis.destroy()
  }, [])
  return <>{children}</>
}
```

## Performance Rules

1. **`will-change: transform`** on actively animating elements only
2. **`AnimatePresence`** wraps all conditional renders
3. **`once: true`** on viewport triggers (no re-trigger on scroll up)
4. **`viewport={{ margin: '-80px' }}`** triggers before element reaches viewport
5. **Avoid `transition: all`** - specify exact properties
6. **Always define `exit`** when using `AnimatePresence`
7. **`layoutId`** for shared layout animations (tabs, toggles)
8. **Batch animations** - stagger children rather than individual triggers
