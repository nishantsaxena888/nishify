'use client'

import dynamic from 'next/dynamic'

// 👇 Directly define your component map (can be generated later if needed)
export const componentMap: Record<string, any> = {
  'hero-banner': dynamic(() => import('@/components/dynamic/hero-banner')),
  'feature-list': dynamic(() => import('@/components/dynamic/feature-list')),
  'login-form': dynamic(() => import('@/components/dynamic/login-form'), {
    ssr: false
  }),
}

export function getDynamicComponent(type: string) {
  return componentMap[type] || null
}
