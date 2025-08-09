"use client";

import * as Lucide from "lucide-react";
import Image from "next/image";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

/* ===================== Types ===================== */
type TitleSegment = { text: string; className?: string };

type LucideIconSpec = {
  kind: "lucide";
  name: keyof typeof Lucide; // e.g. "Medal" | "Map" | "Plane" | "Gift"
  size?: number; // default 32
  className?: string;
};
type ImageIconSpec = {
  kind: "image";
  src: string;
  alt?: string;
  width?: number; // default 32
  height?: number; // default 32
  className?: string;
};

type Feature = {
  title: string;
  description: string;
  icon?: LucideIconSpec | ImageIconSpec;
  cardClass?: string;
  titleClass?: string; // extra class on CardTitle wrapper
  titleBadgeClass?: string; // e.g. "bg-primary/30 px-2 rounded"
  descClass?: string;
};

export type HowItWorksSectionProps = {
  id?: string;
  heading: TitleSegment[]; // rendered inline in one <h2>
  subtitle?: string;

  features: Feature[];

  // layout overrides (optional)
  containerClass?: string;
  headingClass?: string;
  subtitleClass?: string;
  gridClass?: string;
};

/* ===================== Component ===================== */
export default function HowItWorksSection({
  id = "how-it-works",
  heading,
  subtitle,

  features,

  containerClass = "container text-center py-24 sm:py-32",
  headingClass = "text-3xl md:text-4xl font-bold",
  subtitleClass = "md:w-3/4 mx-auto mt-4 mb-12 text-xl text-muted-foreground",
  gridClass = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8",
}: HowItWorksSectionProps) {
  return (
    <section id={id} className={containerClass}>
      <h2 className={headingClass}>
        {heading.map((seg, i) => (
          <span key={i} className={seg.className}>
            {seg.text}
          </span>
        ))}
      </h2>

      {subtitle && <p className={subtitleClass}>{subtitle}</p>}

      <div className={gridClass}>
        {features.map((f, i) => (
          <Card
            key={i}
            className={cn("bg-muted/50 border rounded-2xl", f.cardClass)}
          >
            <CardHeader>
              <CardTitle
                className={cn("grid gap-3 place-items-center", f.titleClass)}
              >
                {renderIcon(f.icon)}
                {f.titleBadgeClass ? (
                  <span className={f.titleBadgeClass}>{f.title}</span>
                ) : (
                  f.title
                )}
              </CardTitle>
            </CardHeader>
            <CardContent className={cn("text-center", f.descClass)}>
              {f.description}
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

/* ===================== Helpers ===================== */
function renderIcon(icon?: LucideIconSpec | ImageIconSpec) {
  if (!icon) return null;

  if (icon.kind === "lucide") {
    const Ico = Lucide[icon.name] as React.ComponentType<{
      size?: number;
      className?: string;
    }>;
    if (!Ico) return null;
    return <Ico size={icon.size ?? 32} className={icon.className} />;
  }

  return (
    <Image
      src={icon.src}
      alt={icon.alt ?? "icon"}
      width={icon.width ?? 32}
      height={icon.height ?? 32}
      className={icon.className}
    />
  );
}
