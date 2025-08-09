/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import Image from "next/image";
import { cn } from "@/lib/utils";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import * as Lucide from "lucide-react";
// If you have custom icons (MagnifierIcon, WalletIcon, ChartIcon, ...)
// exported from "./Icons", they’ll be picked up via the "custom" icon kind:
import * as CustomIcons from "./Icons";

/* ---------------- Types ---------------- */
type TitleSegment = { text: string; className?: string };

type LucideIconSpec = {
  kind: "lucide";
  name: keyof typeof Lucide; // e.g. "ChartBar", "Wallet", ...
  size?: number; // default 24
  className?: string;
};

type ImageIconSpec = {
  kind: "image";
  src: string;
  alt?: string;
  width?: number; // default 24
  height?: number; // default 24
  className?: string;
};

type CustomIconSpec = {
  kind: "custom";
  name: keyof typeof CustomIcons | string; // e.g. "MagnifierIcon"
  className?: string;
  // optional props passed to the custom icon component
  props?: Record<string, unknown>;
};

type IconSpec = LucideIconSpec | ImageIconSpec | CustomIconSpec;

type ServiceItem = {
  title: string;
  description: string;
  icon?: IconSpec;
  cardClass?: string; // per-card override
  titleClass?: string;
  descClass?: string;
};

type RightImage = {
  src: string;
  alt?: string;
  width?: number; // next/image intrinsic width
  height?: number; // next/image intrinsic height
  className?: string; // Tailwind sizing (w-[...])
};

export type ServicesSectionProps = {
  id?: string;

  heading: TitleSegment[]; // e.g. [{text:"Client-Centric ", className:"text-primary"}, {text:"Services"}]
  subtitle?: string;

  services: ServiceItem[]; // the 3 (or more) rows

  rightImage: RightImage; // the illustration on the right

  // layout/style overrides
  containerClass?: string;
  gridClass?: string;
  listClass?: string; // wrapper around cards column
  iconWrapClass?: string; // bg wrapper behind icon
  cardBaseClass?: string; // base class for all cards
};

/* ---------------- Component ---------------- */
export default function ServicesSection({
  id = "services",
  heading,
  subtitle,
  services,
  rightImage,

  containerClass = "container py-24 sm:py-32",
  gridClass = "grid lg:grid-cols-2 gap-8 place-items-center",
  listClass = "flex flex-col gap-8",
  iconWrapClass = "mt-1 bg-primary/20 p-1 rounded-2xl",
  cardBaseClass = "border rounded-2xl",
}: ServicesSectionProps) {
  return (
    <section id={id} className={containerClass}>
      <div className={gridClass}>
        {/* Left: title + subtitle + service list */}
        <div>
          <h2 className="text-3xl md:text-4xl font-bold">
            {heading.map((seg, i) => (
              <span key={i} className={seg.className}>
                {seg.text}
              </span>
            ))}
          </h2>

          {subtitle && (
            <p className="text-muted-foreground text-xl mt-4 mb-8">
              {subtitle}
            </p>
          )}

          <div className={listClass}>
            {services.map((s, i) => (
              <Card key={i} className={cn(cardBaseClass, s.cardClass)}>
                <CardHeader className="space-y-1 flex md:flex-row justify-start items-start gap-4">
                  <div className={iconWrapClass}>{renderIcon(s.icon)}</div>
                  <div>
                    <CardTitle className={cn(s.titleClass)}>
                      {s.title}
                    </CardTitle>
                    <CardDescription
                      className={cn("text-md mt-2", s.descClass)}
                    >
                      {s.description}
                    </CardDescription>
                  </div>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>

        {/* Right: image */}
        <Image
          src={rightImage.src}
          alt={rightImage.alt ?? "Services illustration"}
          width={rightImage.width ?? 600}
          height={rightImage.height ?? 600}
          className={cn(
            "w-[300px] md:w-[500px] lg:w-[600px] object-contain",
            rightImage.className
          )}
          priority
        />
      </div>
    </section>
  );
}

/* ---------------- Helpers ---------------- */
function renderIcon(icon?: IconSpec) {
  if (!icon) return null;

  if (icon.kind === "lucide") {
    const Ico = Lucide[icon.name] as React.ComponentType<{
      size?: number;
      className?: string;
    }>;
    if (!Ico) return null;
    return <Ico size={icon.size ?? 24} className={icon.className} />;
  }

  if (icon.kind === "image") {
    return (
      <Image
        src={icon.src}
        alt={icon.alt ?? "icon"}
        width={icon.width ?? 24}
        height={icon.height ?? 24}
        className={icon.className}
      />
    );
  }

  // custom
  const Any = (CustomIcons as any)[icon.name];
  if (Any) {
    return <Any className={icon.className} {...(icon.props ?? {})} />;
  }
  return null;
}
