'use client'

import { useEffect } from 'react'

export function ThemeRegistry({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const brand = localStorage.getItem('brand-theme') || 'amberland'
    const mode = localStorage.getItem('color-mode') || 'light'

    document.body.classList.add(`theme-${brand}`, mode)
  }, [])

  return <>{children}</>
}
