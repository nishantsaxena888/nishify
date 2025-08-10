"use client";

import { cn } from "@/lib/utils";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { buttonVariants } from "@/components/ui/button";
import {
  Facebook,
  Instagram,
  Linkedin,
  Twitter,
  Github,
  Globe,
  Dribbble,
  Youtube,
} from "lucide-react";

/* -------------------- Types -------------------- */
type TitleSegment = { text: string; className?: string };

type SocialLink = {
  icon:
    | "linkedin"
    | "facebook"
    | "instagram"
    | "twitter"
    | "github"
    | "globe"
    | "dribbble"
    | "youtube";
  href: string;
  label?: string; // a11y
};

type Member = {
  imageUrl: string;
  name: string;
  position: string;
  bio?: string;
  socials?: SocialLink[];
  cardClass?: string;
};

export type TeamSectionProps = {
  id?: string;

  heading: TitleSegment[]; // e.g. [{text:"Our Dedicated ", className:"text-primary"}, {text:"Crew"}]
  subtitle?: string;

  members: Member[];

  // layout/style overrides (no content defaults)
  containerClass?: string;
  headingClass?: string;
  subtitleClass?: string;
  gridClass?: string;
  cardBaseClass?: string;
  avatarClass?: string;
  positionClass?: string;
};

/* -------------------- Component -------------------- */
export default function TeamSection({
  id = "team",
  heading,
  subtitle,
  members,

  containerClass = "container py-24 sm:py-32",
  headingClass = "text-3xl md:text-4xl font-bold",
  subtitleClass = "mt-4 mb-10 text-xl text-muted-foreground",
  gridClass = "grid md:grid-cols-2 lg:grid-cols-4 gap-8 gap-y-10",
  cardBaseClass = "bg-muted/50 relative mt-8 flex flex-col justify-center items-center rounded-2xl",
  avatarClass = "absolute -top-12 rounded-full w-24 h-24 aspect-square object-cover",
  positionClass = "text-primary",
}: TeamSectionProps) {
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
        {members.map((m, i) => (
          <Card
            key={`${m.name}-${i}`}
            className={cn(cardBaseClass, m.cardClass)}
          >
            <CardHeader className="mt-8 flex justify-center items-center pb-2">
              <img
                src={m.imageUrl}
                alt={`${m.name} ${m.position}`}
                className={avatarClass}
              />
              <CardTitle className="text-center">{m.name}</CardTitle>
              <CardDescription className={positionClass}>
                {m.position}
              </CardDescription>
            </CardHeader>

            {m.bio && (
              <CardContent className="text-center pb-2">
                <p>{m.bio}</p>
              </CardContent>
            )}

            {m.socials?.length ? (
              <CardFooter className="flex gap-1">
                {m.socials.map((s, idx) => (
                  <a
                    key={`${s.icon}-${idx}`}
                    href={s.href}
                    target="_blank"
                    rel="noreferrer noopener"
                    aria-label={s.label ?? s.icon}
                    className={buttonVariants({ variant: "ghost", size: "sm" })}
                  >
                    {renderSocialIcon(s.icon)}
                  </a>
                ))}
              </CardFooter>
            ) : null}
          </Card>
        ))}
      </div>
    </section>
  );
}

/* -------------------- Helpers -------------------- */
function renderSocialIcon(icon: SocialLink["icon"]) {
  const map = {
    linkedin: Linkedin,
    facebook: Facebook,
    instagram: Instagram,
    twitter: Twitter,
    github: Github,
    globe: Globe,
    dribbble: Dribbble,
    youtube: Youtube,
  } as const;

  const Ico = map[icon] ?? Globe;
  return <Ico size={20} />;
}
