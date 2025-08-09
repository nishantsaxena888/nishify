/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import Link from "next/link";
import Image from "next/image";
import { cn } from "@/lib/utils";
// If you have custom SVG icons (e.g., LogoIcon) export them from "@/components/Icons"
import * as CustomIcons from "./Icons";
import * as Lucide from "lucide-react";
import { ScrollToTop } from "./dynamic-components/ScrollToTop";

/* ================= Types ================= */
type BrandIcon =
  | { kind: "custom"; name: keyof typeof CustomIcons; className?: string }
  | {
      kind: "lucide";
      name: keyof typeof Lucide;
      className?: string;
      size?: number;
    }
  | {
      kind: "image";
      src: string;
      alt?: string;
      width?: number;
      height?: number;
      className?: string;
    };

type Brand = {
  text?: string; // "ShadcnUI/React"
  href?: string; // "/"
  icon?: BrandIcon; // optional icon shown before the text
  className?: string;
};

type FooterLink = {
  label: string;
  href: string;
  external?: boolean;
  className?: string;
};

type FooterColumn = {
  title: string;
  links: FooterLink[];
  className?: string;
};

type Copyright = {
  prefix?: string; // "© 2024 Landing page made by "
  author?: { label: string; href: string; external?: boolean };
  year?: number | "auto"; // default "auto"
  className?: string;
};

export type FooterSectionProps = {
  id?: string;

  brand?: Brand;
  columns: FooterColumn[];

  copyright?: Copyright;

  showTopDivider?: boolean;

  // style overrides (content-free)
  sectionClass?: string;
  gridClass?: string;
  brandWrapClass?: string;
  titleClass?: string;
  linkClass?: string;
};

/* ================= Component ================= */
export default function FooterSection({
  id = "footer",
  brand,
  columns,
  copyright,

  showTopDivider = true,

  sectionClass = "",
  gridClass = "container py-20 grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-x-12 gap-y-8",
  brandWrapClass = "col-span-full xl:col-span-2",
  titleClass = "font-bold text-lg",
  linkClass = "opacity-60 hover:opacity-100",
}: FooterSectionProps) {
  const year =
    copyright?.year === "auto" || copyright?.year == null
      ? new Date().getFullYear()
      : copyright?.year;

  return (
    <>
      <footer id={id}>
        {showTopDivider && <hr className="w-11/12 mx-auto" />}

        <section className={gridClass}>
          {/* Brand */}
          {brand ? (
            <div className={brandWrapClass}>
              {brand.href ? (
                <Link
                  href={brand.href}
                  className={cn(
                    "font-bold text-xl flex items-center gap-2",
                    brand.className
                  )}
                >
                  {renderIcon(brand.icon)}
                  {brand.text}
                </Link>
              ) : (
                <div
                  className={cn(
                    "font-bold text-xl flex items-center gap-2",
                    brand.className
                  )}
                >
                  {renderIcon(brand.icon)}
                  {brand.text}
                </div>
              )}
            </div>
          ) : null}

          {/* Columns */}
          {columns.map((col, i) => (
            <div
              key={`${col.title}-${i}`}
              className={cn("flex flex-col gap-2", col.className)}
            >
              <h3 className={titleClass}>{col.title}</h3>
              {col.links.map((l, j) =>
                l.external ? (
                  <a
                    key={`${l.label}-${j}`}
                    href={l.href}
                    rel="noreferrer noopener"
                    target="_blank"
                    className={cn(linkClass, l.className)}
                  >
                    {l.label}
                  </a>
                ) : (
                  <Link
                    key={`${l.label}-${j}`}
                    href={l.href}
                    className={cn(linkClass, l.className)}
                  >
                    {l.label}
                  </Link>
                )
              )}
            </div>
          ))}
        </section>

        {/* Copyright */}
        {(copyright?.prefix || copyright?.author) && (
          <section className="container pb-14 text-center">
            <h3 className={copyright?.className}>
              © {year} {copyright?.prefix}
              {copyright?.author ? (
                <a
                  href={copyright.author.href}
                  rel="noreferrer noopener"
                  target={copyright.author.external ? "_blank" : undefined}
                  className="text-primary transition-all border-primary hover:border-b-2"
                >
                  {copyright.author.label}
                </a>
              ) : null}
            </h3>
          </section>
        )}
      </footer>
      <ScrollToTop />
    </>
  );
}

/* ================= Helpers ================= */
function renderIcon(icon?: BrandIcon) {
  if (!icon) return null;

  if (icon.kind === "lucide") {
    const Ico = Lucide[icon.name] as React.ComponentType<{
      className?: string;
      size?: number;
    }>;
    if (!Ico) return null;
    return <Ico size={icon.size ?? 22} className={icon.className} />;
  }
  if (icon.kind === "image") {
    return (
      <Image
        src={icon.src}
        alt={icon.alt ?? "logo"}
        width={icon.width ?? 22}
        height={icon.height ?? 22}
        className={icon.className}
      />
    );
  }
  // custom
  const Any = (CustomIcons as any)[icon.name];
  if (!Any) return null;
  return <Any className={icon.className} />;
}
