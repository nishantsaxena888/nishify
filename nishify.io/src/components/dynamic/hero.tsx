"use client";

import Link from "next/link";

import { Button, buttonVariants } from "@/components/ui/button";
import { Github } from "lucide-react";
import {
  FeatureCard,
  PricingCard,
  TeamCard,
  TestimonialCard,
} from "./dynamic-components/ui-card";

/** ---------- Types (props are optional; defaults match your current UI) ---------- */
type TitleSegment = { text: string; gradient?: string[] }; // supports 2 or 3 stops
type TitleLine = { segments: TitleSegment[] };

type Cta = {
  text: string;
  link: string;
  variant: "solid" | "outline";
  icon?: "github";
  external?: boolean;
};

type TestimonialCard = {
  type: "testimonial";
  avatarUrl: string;
  name: string;
  handle: string;
  quote: string;
  className?: string;
};

type TeamCard = {
  type: "team";
  avatarUrl: string;
  name: string;
  role: string;
  quote: string;
  links?: { github?: string; twitter?: string; linkedin?: string };
  className?: string;
};

type PricingCard = {
  type: "pricing";
  tier: string;
  price: string;
  frequency: string;
  description: string;
  popular?: boolean;
  benefits: string[];
  ctaText: string;
  className?: string;
};

type FeatureCard = {
  type: "feature";
  title: string;
  description: string;
  className?: string;
};

type HeroCardConfig = TestimonialCard | TeamCard | PricingCard | FeatureCard;

type Props = {
  /** Left */
  titleLine1?: TitleLine; // rendered inside <h1 class="inline">
  middleText?: string; // the “ for ” between the lines
  titleLine2?: TitleLine; // rendered inside <h2 class="inline">
  subtitle?: string;
  ctas?: Cta[];

  /** Right */
  cards?: HeroCardConfig[];
  cardsContainerSize?: string; // wrapper size; defaults to your 700x500
};

/** ---------- Helpers ---------- */
function gradientClass(gradient?: string[]) {
  if (!gradient?.length) return "";
  if (gradient.length === 2) {
    return `bg-gradient-to-r from-[${gradient[0]}] to-[${gradient[1]}] text-transparent bg-clip-text`;
  }
  if (gradient.length >= 3) {
    return `bg-gradient-to-r from-[${gradient[0]}] via-[${gradient[1]}] to-[${gradient[2]}] text-transparent bg-clip-text`;
  }
  return "";
}

/** ---------- Component ---------- */
export default function Hero({
  titleLine1,
  middleText = " for ",
  titleLine2,
  subtitle,
  ctas,
  cards,
}: Props) {
  return (
    <section className="container grid lg:grid-cols-2 place-items-center py-20 md:py-32 gap-10">
      <div className="text-center lg:text-start space-y-6">
        <main className="text-5xl md:text-6xl font-bold">
          <h1 className="inline">
            {titleLine1?.segments.map((seg, i) => (
              <span key={i} className={`inline ${gradientClass(seg.gradient)}`}>
                {seg.text}
              </span>
            ))}
          </h1>
          {middleText}
          <h2 className="inline">
            {titleLine2?.segments.map((seg, i) => (
              <span key={i} className={`inline ${gradientClass(seg.gradient)}`}>
                {seg.text}
              </span>
            ))}
          </h2>
        </main>

        <p className="text-xl text-muted-foreground md:w-10/12 mx-auto lg:mx-0">
          {subtitle}
        </p>

        <div className="space-y-4 md:space-y-0 md:space-x-4">
          {ctas?.map((cta, ci) => {
            const content = (
              <>
                {cta.text}
                {cta.icon === "github" && <Github className="ml-2 w-5 h-5" />}
              </>
            );

            if (cta.variant === "solid") {
              return (
                <Button key={ci} asChild className="w-full md:w-1/3">
                  <Link
                    href={cta.link}
                    target={cta.external ? "_blank" : undefined}
                    rel={cta.external ? "noreferrer noopener" : undefined}
                  >
                    {content}
                  </Link>
                </Button>
              );
            }

            return (
              <Link
                key={ci}
                href={cta.link}
                className={`w-full md:w-1/3 ${buttonVariants({
                  variant: "outline",
                })}`}
                target={cta.external ? "_blank" : undefined}
                rel={cta.external ? "noreferrer noopener" : undefined}
              >
                {content}
              </Link>
            );
          })}
        </div>
      </div>

      {/* Hero cards sections */}
      <div className="hidden lg:flex flex-row flex-wrap gap-8 relative w-[700px] h-[500px]">
        {cards?.map((card, ci) => {
          return (
            <div key={ci} className={card.className}>
              {card.type === "testimonial" && <TestimonialCard {...card} />}
              {card.type === "pricing" && <PricingCard {...card} />}
              {card.type === "team" && <TeamCard {...card} />}
              {card.type === "feature" && <FeatureCard {...card} />}
            </div>
          );
        })}
      </div>
      {/* Shadow effect */}
      <div className="shadow"></div>
    </section>
  );
}
