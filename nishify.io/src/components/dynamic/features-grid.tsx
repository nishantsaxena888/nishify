"use client";

import Image from "next/image";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

/* =================== Types =================== */
type TitleSegment = { text: string; className?: string };

type Chip = {
  label: string;
  href?: string;
  className?: string; // extra classes per chip (optional)
};

type FeatureImage = {
  src: string; // e.g. "/assets/growth.png"
  alt?: string;
  width?: number; // default 300
  height?: number; // default 300
  className?: string; // tailwind classes for the <Image>
};

type FeatureItem = {
  title: string;
  description: string;
  image: FeatureImage;
  cardClass?: string; // optional per-card override
  titleClass?: string; // optional
  descClass?: string; // optional
};

export type FeaturesGridProps = {
  id?: string;

  heading: TitleSegment[]; // renders inline as one <h2>
  subtitle?: string;

  chips?: Chip[]; // row of chips under heading

  features: FeatureItem[]; // cards

  /* Layout/style overrides (optional) */
  containerClass?: string;
  headingClass?: string;
  subtitleClass?: string;
  chipsWrapClass?: string;
  chipBadgeClass?: string;
  gridClass?: string;
};

/* =================== Component =================== */
export default function FeaturesGrid({
  id = "features",
  heading,
  subtitle,

  chips = [],
  features,

  containerClass = "container py-24 sm:py-32 space-y-8",
  headingClass = "text-3xl lg:text-4xl font-bold md:text-center",
  subtitleClass = "md:w-3/4 mx-auto text-xl text-muted-foreground md:text-center",
  chipsWrapClass = "flex flex-wrap md:justify-center gap-4",
  chipBadgeClass = "text-sm",
  gridClass = "grid md:grid-cols-2 lg:grid-cols-3 gap-8",
}: FeaturesGridProps) {
  return (
    <section id={id} className={containerClass}>
      {/* Heading */}
      <h2 className={headingClass}>
        {heading.map((seg, i) => (
          <span key={i} className={seg.className}>
            {seg.text}
          </span>
        ))}
      </h2>

      {subtitle && <p className={subtitleClass}>{subtitle}</p>}

      {/* Chips */}
      {chips.length > 0 && (
        <div className={chipsWrapClass}>
          {chips.map((c, i) =>
            c.href ? (
              <a key={i} href={c.href}>
                <Badge
                  variant="secondary"
                  className={cn(chipBadgeClass, c.className)}
                >
                  {c.label}
                </Badge>
              </a>
            ) : (
              <Badge
                key={i}
                variant="secondary"
                className={cn(chipBadgeClass, c.className)}
              >
                {c.label}
              </Badge>
            )
          )}
        </div>
      )}

      {/* Cards */}
      <div className={gridClass}>
        {features.map((f, i) => (
          <Card key={i} className={cn("bg-background/50", f.cardClass)}>
            <CardHeader>
              <CardTitle className={cn(f.titleClass)}>{f.title}</CardTitle>
            </CardHeader>

            <CardContent className={cn(f.descClass)}>
              {f.description}
            </CardContent>

            <CardFooter>
              <Image
                src={f.image.src}
                alt={f.image.alt ?? "feature image"}
                width={f.image.width ?? 300}
                height={f.image.height ?? 300}
                className={cn(
                  "w-[200px] lg:w-[300px] mx-auto",
                  f.image.className
                )}
                priority={i === 0}
              />
            </CardFooter>
          </Card>
        ))}
      </div>
    </section>
  );
}
