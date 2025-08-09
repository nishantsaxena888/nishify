"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";

/* ========= Types ========= */
type TitleSegment = { text: string; className?: string };

export type TestimonialItem = {
  image?: string; // avatar url (optional)
  name: string; // "John Doe"
  userName: string; // "@john_doe"
  comment: string; // the text
  cardClass?: string; // optional per-card override
};

export type TestimonialsMasonryProps = {
  id?: string;

  heading: TitleSegment[]; // rendered inline in one <h2>
  subtitle?: string;

  items: TestimonialItem[];

  // layout/style overrides (content-free)
  containerClass?: string;
  headingClass?: string;
  subtitleClass?: string;

  /** Masonry wrapper class (columns + gaps) */
  masonryClass?: string;

  /** Classes applied to each card for masonry (to avoid splitting) */
  masonryCardClass?: string;
};

/* ========= Helpers ========= */
function initials(name?: string) {
  if (!name) return "NA";
  return (
    name
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 2)
      .map((n) => n[0]?.toUpperCase() ?? "")
      .join("") || "NA"
  );
}

/* ========= Component ========= */
export default function TestimonialsMasonry({
  id = "testimonials",
  heading,
  subtitle,
  items,

  containerClass = "container py-24 sm:py-32",
  headingClass = "text-3xl md:text-4xl font-bold",
  subtitleClass = "text-xl text-muted-foreground pt-4 pb-8",

  // Masonry: columns on sm & lg, with vertical gaps
  masonryClass = "mx-auto columns-1 sm:columns-2 lg:columns-3 lg:gap-6 space-y-4 lg:space-y-6",
  masonryCardClass = "break-inside-avoid overflow-hidden",
}: TestimonialsMasonryProps) {
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

      <div className={masonryClass}>
        {items.map((t, i) => (
          <Card
            key={`${t.userName}-${i}`}
            className={cn("max-w-md", masonryCardClass, t.cardClass)}
          >
            <CardHeader className="flex flex-row items-center gap-4 pb-2">
              <Avatar>
                {t.image ? <AvatarImage alt={t.name} src={t.image} /> : null}
                <AvatarFallback>{initials(t.name)}</AvatarFallback>
              </Avatar>

              <div className="flex flex-col">
                <CardTitle className="text-lg">{t.name}</CardTitle>
                <CardDescription>{t.userName}</CardDescription>
              </div>
            </CardHeader>

            <CardContent>{t.comment}</CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
