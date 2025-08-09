/* eslint-disable @typescript-eslint/no-explicit-any */
import { Button, buttonVariants } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Check, Github, Globe, Linkedin, Twitter, XIcon } from "lucide-react";
import { LightBulbIcon } from "./Icons";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Fragment, useMemo } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

type TestimonialCardProps = {
  type: string;
  avatarUrl: string;
  name: string;
  handle: string;
  quote: string;
};

type TeamCardProps = {
  type: string;
  avatarUrl: string;
  name: string;
  role: string;
  quote: string;
  links?: any;
};

export const TestimonialCard = (prop: TestimonialCardProps) => {
  const initial = useMemo(() => prop?.name[0], [prop?.name]);
  return (
    <Fragment>
      <Card className="absolute w-[340px] -top-[15px] drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader className="flex flex-row items-center gap-4 pb-2">
          <Avatar>
            {prop?.avatarUrl ? null : initial}
            <AvatarImage alt={prop?.name} src={prop?.avatarUrl || ""} />
            <AvatarFallback>{initial}</AvatarFallback>
          </Avatar>

          <div className="flex flex-col">
            <CardTitle className="text-lg">{prop?.name}</CardTitle>
            <CardDescription>{prop?.handle}</CardDescription>
          </div>
        </CardHeader>

        <CardContent>{prop.quote}</CardContent>
      </Card>
    </Fragment>
  );
};

const ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  github: (p) => <Github className={`w-5 h-5 ${p.className ?? ""}`} />,
  linkedin: (p) => <Linkedin className={`w-5 h-5 ${p.className ?? ""}`} />,
  twitter: (p) => <Twitter className={`w-5 h-5 ${p.className ?? ""}`} />,
  x: (p) => <XIcon className={`w-5 h-5 ${p.className ?? ""}`} />,
  globe: (p) => <Globe className={`w-5 h-5 ${p.className ?? ""}`} />,
};

export const TeamCard = (prop: TeamCardProps) => {
  return (
    <>
      {/* Team */}
      <Card className="absolute right-[20px] top-4 w-80 flex flex-col justify-center items-center drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader className="mt-8 flex justify-center items-center pb-2">
          <img
            width={150}
            height={150}
            src={prop?.avatarUrl}
            alt="user avatar"
            className="absolute grayscale-[0%] -top-12 rounded-full w-24 h-24 aspect-square object-cover"
          />
          <CardTitle className="text-center">{prop?.name}</CardTitle>
          <CardDescription className="font-normal text-primary">
            {prop?.role}
          </CardDescription>
        </CardHeader>

        <CardContent className="text-center pb-2">
          <p>{prop?.quote}</p>
        </CardContent>

        <CardFooter>
          <div>
            {prop?.links?.map(
              (icons: { icon: string; href: string }, index: number) => {
                const Icon = ICONS[icons.icon] ?? ICONS.globe;
                return (
                  <Fragment key={index}>
                    <a
                      rel="noreferrer noopener"
                      href={icons?.href}
                      target="_blank"
                      className={buttonVariants({
                        variant: "ghost",
                        size: "sm",
                      })}
                    >
                      <span className="sr-only">{icons?.icon}</span>
                      <Icon />
                    </a>
                  </Fragment>
                );
              }
            )}
          </div>
        </CardFooter>
      </Card>
    </>
  );
};

export const PricingCard = (prop: {
  tier: string;
  price: string;
  frequency: string;
  description: string;
  ctaText: string;
  ctaLink?: string;
  popular?: boolean;
  benefits?: string[];
}) => {
  return (
    <>
      <Card className="absolute top-[150px] left-[50px] w-72  drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader>
          <CardTitle className="flex item-center justify-between">
            {prop.tier}
            {prop?.popular ? (
              <Badge variant="secondary" className="text-sm text-primary">
                Most popular
              </Badge>
            ) : null}
          </CardTitle>
          <div>
            <span className="text-3xl font-bold">{prop.price}</span>
            {prop?.frequency ? (
              <span className="text-muted-foreground"> /{prop.frequency}</span>
            ) : null}
          </div>

          <CardDescription>{prop.description}</CardDescription>
        </CardHeader>

        <CardContent>
          <Button className="w-full" asChild>
            <Link href={prop?.ctaLink || "#"}>{prop.ctaText}</Link>
          </Button>
        </CardContent>

        <hr className="w-4/5 m-auto mb-4" />

        <CardFooter className="flex">
          <div className="space-y-4">
            {prop?.benefits?.map((benefit: string) => (
              <span key={benefit} className="flex">
                <Check className="text-green-500" />{" "}
                <h3 className="ml-2">{benefit}</h3>
              </span>
            ))}
          </div>
        </CardFooter>
      </Card>
    </>
  );
};

export const FeatureCard = (prop: { title: string; description: string }) => {
  return (
    <>
      <Card className="absolute w-[350px] -right-[10px] bottom-[35px]  drop-shadow-xl shadow-black/10 dark:shadow-white/10">
        <CardHeader className="space-y-1 flex md:flex-row justify-start items-start gap-4">
          <div className="mt-1 bg-primary/20 p-1 rounded-2xl">
            <LightBulbIcon />
          </div>
          <div>
            <CardTitle>{prop.title}</CardTitle>
            <CardDescription className="text-md mt-2">
              {prop.description}
            </CardDescription>
          </div>
        </CardHeader>
      </Card>
    </>
  );
};

export type PriceCardProps = {
  title: string;
  popular?: boolean; // highlights card + shows badge
  popularLabel?: string; // default: "Most popular"

  /** price line */
  price: number | string; // 0 | "29"
  currency?: string; // default: "$"
  period?: string; // default: "month"

  description?: string;

  /** CTA button */
  button: {
    text: string;
    href?: string; // if provided, Button becomes a link
    variant?:
      | "default"
      | "secondary"
      | "outline"
      | "destructive"
      | "ghost"
      | "link";
  };

  /** bullets */
  benefits: string[];

  /** style overrides */
  className?: string;
};

export default function PriceCard({
  title,
  popular,
  popularLabel = "Most popular",
  price,
  currency = "$",
  period = "month",
  description,
  button,
  benefits,
  className,
}: PriceCardProps) {
  return (
    <Card
      className={cn(
        popular ? "drop-shadow-xl shadow-black/10 dark:shadow-white/10" : "",
        className
      )}
    >
      <CardHeader>
        <CardTitle className="flex item-center justify-between">
          {title}
          {popular ? (
            <Badge variant="secondary" className="text-sm text-primary">
              {popularLabel}
            </Badge>
          ) : null}
        </CardTitle>

        <div>
          <span className="text-3xl font-bold">
            {typeof price === "number"
              ? `${currency}${price}`
              : `${currency}${price}`}
          </span>
          <span className="text-muted-foreground"> /{period}</span>
        </div>

        {description ? <CardDescription>{description}</CardDescription> : null}
      </CardHeader>

      <CardContent>
        {button.href ? (
          <Button
            asChild
            className="w-full"
            variant={button.variant ?? "default"}
          >
            <Link href={button.href}>{button.text}</Link>
          </Button>
        ) : (
          <Button className="w-full" variant={button.variant ?? "default"}>
            {button.text}
          </Button>
        )}
      </CardContent>

      <hr className="w-4/5 m-auto mb-4" />

      <CardFooter className="flex">
        <div className="space-y-4">
          {benefits.map((benefit) => (
            <span key={benefit} className="flex">
              <Check className="text-green-500" />
              <h3 className="ml-2">{benefit}</h3>
            </span>
          ))}
        </div>
      </CardFooter>
    </Card>
  );
}
