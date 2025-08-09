/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import dynamic from "next/dynamic";

// ✅ Client-independent DynamicFormRenderer
const DynamicFormRenderer = dynamic(
  () => import("@/components/dynamic/dynamic-form"),
  {
    ssr: false,
  }
);

export const componentMap: Record<string, any> = {
  hero: dynamic(() => import("@/components/dynamic/hero")),
  navbar: dynamic(() => import("@/components/dynamic/navbar")),
  sponsors: dynamic(() => import("@/components/dynamic/sponsors")),
  about: dynamic(() => import("@/components/dynamic/about-section")),
  "how-it-works": dynamic(
    () => import("@/components/dynamic/how-It-works-section")
  ),
  "features-grid": dynamic(() => import("@/components/dynamic/features-grid")),
  services: dynamic(() => import("@/components/dynamic/services-section")),
  "cta-banner": dynamic(() => import("@/components/dynamic/cta-v2")),
  "testimonials-masonry": dynamic(
    () => import("@/components/dynamic/testimonials-masonry")
  ),
  "team-section": dynamic(() => import("@/components/dynamic/team-section")),
  "pricing-grid": dynamic(() => import("@/components/dynamic/price-grid")),
  "hero-banner": dynamic(() => import("@/components/dynamic/hero-banner")),
  "feature-list": dynamic(() => import("@/components/dynamic/feature-list")),
  "newsletter-signup": dynamic(
    () => import("@/components/dynamic/newsletter-signup")
  ),
  "faq-accordion": dynamic(() => import("@/components/dynamic/faq-accordion")),
  "footer-section": dynamic(() => import("@/components/dynamic/footer")),
  "login-form": DynamicFormRenderer,
  "register-form": DynamicFormRenderer,
  "forgot-password-form": DynamicFormRenderer,
};

export function getDynamicComponent(type: string) {
  return componentMap[type] || null;
}
