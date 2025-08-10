"use client";

import * as Lucide from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { cn } from "@/lib/utils";

/** ---------- Types ---------- */
type LucideIconSpec = {
  kind: "lucide";
  /** Exact export name from `lucide-react` e.g. "Radar", "Github", "Building2" */
  name: keyof typeof Lucide;
  size?: number; // default 28
  className?: string; // optional tailwind classes
};

type ImageIconSpec = {
  kind: "image";
  src: string;
  alt?: string;
  width?: number; // default 28
  height?: number; // default 28
  className?: string;
};

type SponsorItem = {
  label: string;
  href?: string; // optional link
  icon?: LucideIconSpec | ImageIconSpec;
  className?: string; // per-item wrapper classes
};

export type SponsorsProps = {
  id?: string;
  title: string;
  /** Tailwind classes to control layout/spacing (optional, sensible defaults below) */
  wrapperClass?: string;
  titleClass?: string;
  itemsClass?: string;
  items: SponsorItem[];
};

/** ---------- Component ---------- */
export default function Sponsors({
  id = "sponsors",
  title,
  wrapperClass = "container pt-24 sm:py-32",
  titleClass = "text-center text-md lg:text-xl font-bold mb-8 text-primary",
  itemsClass = "flex flex-wrap justify-center items-center gap-4 md:gap-8",
  items,
}: SponsorsProps) {
  return (
    <section id={id} className={wrapperClass}>
      <h2 className={titleClass}>{title}</h2>

      <div className={itemsClass}>
        {items.map((item, idx) => {
          const content = (
            <div
              className={cn(
                "flex items-center gap-2 text-muted-foreground/60",
                item.className
              )}
            >
              {renderIcon(item.icon)}
              <span className="text-xl font-bold">{item.label}</span>
            </div>
          );

          return item.href ? (
            <Link
              key={`${item.label}-${idx}`}
              href={item.href}
              target="_blank"
              rel="noreferrer noopener"
              aria-label={item.label}
            >
              {content}
            </Link>
          ) : (
            <div key={`${item.label}-${idx}`}>{content}</div>
          );
        })}
      </div>
    </section>
  );
}

/** ---------- Helpers ---------- */
function renderIcon(icon?: SponsorItem["icon"]) {
  if (!icon) return null;

  if (icon.kind === "lucide") {
    const { name, size = 28, className } = icon;
    const LucideIcon = Lucide[name] as React.ComponentType<{
      className?: string;
      size?: number;
    }>;
    if (!LucideIcon) return null;
    return <LucideIcon size={size} className={className} />;
  }

  // image icon
  const { src, alt = "logo", width = 28, height = 28, className } = icon;
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      className={className}
    />
  );
}
