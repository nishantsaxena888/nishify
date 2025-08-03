'use client'

import dynamic from 'next/dynamic'

// ✅ Client-independent DynamicFormRenderer
const DynamicFormRenderer = dynamic(() => import('@/components/dynamic/dynamic-form'), {
  ssr: false,
})

export const componentMap: Record<string, any> = {
  'hero-banner': dynamic(() => import('@/components/dynamic/hero-banner')),
  'feature-list': dynamic(() => import('@/components/dynamic/feature-list')),
  'login-form': DynamicFormRenderer,
  'register-form': DynamicFormRenderer,
  'forgot-password-form': DynamicFormRenderer,
}

export function getDynamicComponent(type: string) {
  return componentMap[type] || null
}
