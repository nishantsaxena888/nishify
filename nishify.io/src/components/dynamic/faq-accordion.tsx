/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { cn } from "@/lib/utils";

/* ------------ Types ------------ */
type TitleSegment = { text: string; className?: string };

type FaqItem = {
  id?: string; // optional stable id; falls back to index
  question: string;
  answer: string;
  itemClass?: string; // per-item override (optional)
};

type AccordionCfg = {
  type?: "single" | "multiple"; // default: "single"
  collapsible?: boolean; // default: true for "single"
  defaultValue?: string | string[]; // item id(s) to open initially
};

export type FaqAccordionProps = {
  id?: string;

  heading: TitleSegment[]; // inline segments for the H2
  subheading?: string;

  items: FaqItem[];

  contact?: {
    prefix?: string; // e.g., "Still have questions?"
    linkText: string; // e.g., "Contact us"
    href: string; // destination
  };

  accordion?: AccordionCfg;

  // style overrides (no content defaults)
  containerClass?: string;
  headingClass?: string;
  subheadingClass?: string;
  accordionClass?: string;
  triggerClass?: string;
  contentClass?: string;
  contactClass?: string;
};

/* ------------ Component ------------ */
export default function FaqAccordion({
  id = "faq",
  heading,
  subheading,
  items,
  contact,

  accordion = { type: "single", collapsible: true },

  containerClass = "container py-24 sm:py-32",
  headingClass = "text-3xl md:text-4xl font-bold mb-4",
  subheadingClass = "text-xl text-muted-foreground mb-6",
  accordionClass = "w-full",
  triggerClass = "text-left",
  contentClass = "",
  contactClass = "font-medium mt-4",
}: FaqAccordionProps) {
  const { type = "single", collapsible = true, defaultValue } = accordion;

  return (
    <section id={id} className={containerClass}>
      <h2 className={headingClass}>
        {heading.map((seg, i) => (
          <span key={i} className={seg.className}>
            {seg.text}
          </span>
        ))}
      </h2>

      {subheading ? <p className={subheadingClass}>{subheading}</p> : null}

      <Accordion
        type={type}
        collapsible={type === "single" ? collapsible : undefined}
        className={accordionClass}
        defaultValue={defaultValue as any}
      >
        {items.map((it, idx) => {
          const value = it.id ?? `item-${idx + 1}`;
          return (
            <AccordionItem key={value} value={value} className={it.itemClass}>
              <AccordionTrigger className={triggerClass}>
                {it.question}
              </AccordionTrigger>
              <AccordionContent className={contentClass}>
                {it.answer}
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>

      {contact ? (
        <h3 className={contactClass}>
          {contact.prefix ?? "Still have questions?"}{" "}
          <a
            rel="noreferrer noopener"
            href={contact.href}
            className="text-primary transition-all border-primary hover:border-b-2"
          >
            {contact.linkText}
          </a>
        </h3>
      ) : null}
    </section>
  );
}
