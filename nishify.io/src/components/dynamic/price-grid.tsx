"use client";

import dynamic from "next/dynamic";
import { cn } from "@/lib/utils";
import PriceCard, { PriceCardProps } from "./dynamic-components/ui-card";

type TitleSegment = { text: string; className?: string };

export type PricingGridProps = {
  id?: string;

  heading: TitleSegment[]; // inline pieces for the H2
  subheading?: string;

  plans: PriceCardProps[]; // each plan -> PriceCard

  // layout / style overrides
  containerClass?: string;
  headingClass?: string;
  subheadingClass?: string;
  gridClass?: string;
};

export default function PricingGrid({
  id = "pricing",
  heading,
  subheading,
  plans,

  containerClass = "container py-24 sm:py-32",
  headingClass = "text-3xl md:text-4xl font-bold text-center",
  subheadingClass = "text-xl text-center text-muted-foreground pt-4 pb-8",
  gridClass = "grid md:grid-cols-2 lg:grid-cols-3 gap-8",
}: PricingGridProps) {
  return (
    <section id={id} className={containerClass}>
      <h2 className={headingClass}>
        {heading.map((seg, i) => (
          <span key={i} className={seg.className}>
            {seg.text}
          </span>
        ))}
      </h2>

      {subheading ? <h3 className={subheadingClass}>{subheading}</h3> : null}

      <div className={cn(gridClass)}>
        {plans.map((p, idx) => (
          <PriceCard key={`${p.title}-${idx}`} {...p} />
        ))}
      </div>
    </section>
  );
}
