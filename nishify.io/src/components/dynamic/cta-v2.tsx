"use client";

import Link from "next/link";
import { cn } from "@/lib/utils";
import { Button, buttonVariants } from "@/components/ui/button";

/* ================= Types ================= */
type TitleSegment = { text: string; className?: string };

type CtaButton = {
  text: string;
  href?: string; // if provided, renders as <Link> inside Button
  variant?:
    | "default"
    | "secondary"
    | "outline"
    | "destructive"
    | "ghost"
    | "link";
  size?: "default" | "sm" | "lg" | "icon";
  external?: boolean; // open in new tab for links
  className?: string; // extra classes
};

export type CtaBannerProps = {
  id?: string;

  title: TitleSegment[]; // e.g. ["All Your ", {text:"Ideas & Concepts ", className:"bg-gradient-to-b ... text-transparent bg-clip-text"}, "In One Interface"]
  subtitle?: string;

  buttons: CtaButton[]; // right-side buttons (1..n)

  /* layout/style overrides (content-free) */
  sectionClass?: string; // outer section classes
  containerClass?: string; // inner container/grid
  titleClass?: string; // h2 classes
  subtitleClass?: string; // paragraph classes
  buttonsWrapClass?: string; // wrapper of all buttons
};

/* ================= Component ================= */
export default function CtaV2({
  id = "cta",
  title,
  subtitle,
  buttons,

  sectionClass = "bg-muted/50 py-16 my-24 sm:my-32",
  containerClass = "container lg:grid lg:grid-cols-2 place-items-center",
  titleClass = "text-3xl md:text-4xl font-bold",
  subtitleClass = "text-muted-foreground text-xl mt-4 mb-8 lg:mb-0",
  buttonsWrapClass = "space-y-4 lg:space-y-0 lg:col-start-2 flex flex-col md:flex-row md:items-center md:gap-4",
}: CtaBannerProps) {
  return (
    <section id={id} className={sectionClass}>
      <div className={containerClass}>
        {/* Left: Title + Subtitle */}
        <div className="lg:col-start-1">
          <h2 className={titleClass}>
            {title.map((seg, i) => (
              <span key={i} className={seg.className}>
                {seg.text}
              </span>
            ))}
          </h2>
          {subtitle && <p className={subtitleClass}>{subtitle}</p>}
        </div>

        {/* Right: Buttons */}
        <div className={buttonsWrapClass}>
          {buttons.map((b, i) => {
            if (b.href) {
              return (
                <Button
                  key={i}
                  asChild
                  variant={b.variant ?? "default"}
                  size={b.size ?? "default"}
                  className={cn("w-full md:w-auto", b.className)}
                >
                  <Link
                    href={b.href}
                    target={b.external ? "_blank" : undefined}
                    rel={b.external ? "noreferrer noopener" : undefined}
                  >
                    {b.text}
                  </Link>
                </Button>
              );
            }
            // Non-link button (handler can be attached by parent via onClick when used directly)
            return (
              <button
                key={i}
                className={cn(
                  "w-full md:w-auto",
                  buttonVariants({
                    variant: b.variant ?? "default",
                    size: b.size ?? "default",
                  }),
                  b.className
                )}
              >
                {b.text}
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
