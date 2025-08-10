"use client";

import Image from "next/image";
import { cn } from "@/lib/utils";

/* ---------- Types ---------- */
type TitleSegment = { text: string; className?: string; gradient?: string[] }; // gradient still supported if ever needed
type StatItem = { quantity: string | number; description: string };
type Img = {
  src: string;
  alt?: string;
  width?: number;
  height?: number;
  className?: string;
};

export type AboutSectionProps = {
  id?: string;
  image: Img;
  titleSegments: TitleSegment[]; // ["About ", (gradient) "Company"] etc.
  description: string | string[]; // single paragraph or array of paragraphs
  stats: StatItem[];

  /* Optional style overrides (no content defaults) */
  containerClass?: string;
  panelClass?: string;
  innerClass?: string;
  titleClass?: string;
  descClass?: string;
  statsGridClass?: string;
  statQtyClass?: string;
  statDescClass?: string;
};

/* ---------- Helpers ---------- */
function gradientClass(g?: string[]) {
  if (!g?.length) return "";
  if (g.length === 2)
    return `bg-gradient-to-b from-[${g[0]}] to-[${g[1]}] text-transparent bg-clip-text`;
  if (g.length >= 3)
    return `bg-gradient-to-b from-[${g[0]}] via-[${g[1]}] to-[${g[2]}] text-transparent bg-clip-text`;
  return "";
}

/* ---------- Component ---------- */
export default function AboutSection({
  id = "about",
  image,
  titleSegments,
  description,
  stats,
  containerClass = "container py-24 sm:py-32",
  panelClass = "bg-muted/50 border rounded-lg py-12",
  innerClass = "px-6 flex flex-col-reverse md:flex-row gap-8 md:gap-12",
  titleClass = "text-3xl md:text-4xl font-bold",
  descClass = "text-xl text-muted-foreground mt-4",
  statsGridClass = "grid grid-cols-2 lg:grid-cols-4 gap-8",
  statQtyClass = "text-3xl sm:text-4xl font-bold",
  statDescClass = "text-xl text-muted-foreground",
}: AboutSectionProps) {
  return (
    <section id={id} className={containerClass}>
      <div className={panelClass}>
        <div className={innerClass}>
          {/* Left image */}
          <Image
            src={image.src}
            alt={image.alt ?? ""}
            width={image.width ?? 500}
            height={image.height ?? 500}
            className={cn(
              "w-[300px] object-contain rounded-lg",
              image.className
            )}
            priority
          />

          {/* Right content */}
          <div className="flex flex-col justify-between">
            {/* Title + description */}
            <div className="pb-6">
              <h2 className={titleClass}>
                {titleSegments.map((seg, i) => (
                  <span
                    key={i}
                    className={cn(seg.className, gradientClass(seg.gradient))}
                  >
                    {seg.text}
                  </span>
                ))}
              </h2>

              {Array.isArray(description) ? (
                description.map((p, i) => (
                  <p key={i} className={cn(descClass, i > 0 && "mt-3")}>
                    {p}
                  </p>
                ))
              ) : (
                <p className={descClass}>{description}</p>
              )}
            </div>

            {/* Statistics */}
            <section aria-label="statistics">
              <div className={statsGridClass}>
                {stats.map(({ quantity, description }) => (
                  <div key={description} className="space-y-2 text-center">
                    <h3 className={statQtyClass}>{String(quantity)}</h3>
                    <p className={statDescClass}>{description}</p>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </div>
      </div>
    </section>
  );
}
