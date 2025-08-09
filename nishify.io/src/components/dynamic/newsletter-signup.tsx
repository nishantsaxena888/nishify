"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

/* ---------- Types ---------- */
type TitleSegment = { text: string; className?: string };

type ApiConfig = {
  url?: string; // POST here if provided
  method?: "POST" | "GET"; // default POST
  headers?: Record<string, string>; // e.g. { "Content-Type": "application/json" }
  extraBody?: Record<string, unknown>; // extra payload to send along with { email }
};

type InputCfg = {
  name?: string; // default "email"
  placeholder?: string;
  ariaLabel?: string; // default "email"
  required?: boolean; // default true
  defaultValue?: string;
  className?: string;
};

type BtnCfg = {
  text: string;
  variant?:
    | "default"
    | "secondary"
    | "outline"
    | "destructive"
    | "ghost"
    | "link";
  size?: "default" | "sm" | "lg" | "icon";
  className?: string;
};

export type NewsletterSignupProps = {
  id?: string;

  title: TitleSegment[]; // inline pieces (lets you color one word)
  subtitle?: string;

  input?: InputCfg;
  button: BtnCfg;

  api?: ApiConfig; // optional — if absent, just logs to console
  successText?: string; // default "Subscribed!"
  errorText?: string; // default "Please enter a valid email."

  showTopDivider?: boolean;
  showBottomDivider?: boolean;

  // style overrides
  sectionClass?: string;
  containerClass?: string;
  titleClass?: string;
  subtitleClass?: string;
  formClass?: string;
};

/* ---------- Component ---------- */
export default function NewsletterSignup({
  id = "newsletter",
  title,
  subtitle,

  input,
  button,

  api,
  successText = "Subscribed!",
  errorText = "Please enter a valid email.",

  showTopDivider = true,
  showBottomDivider = true,

  sectionClass = "",
  containerClass = "container py-24 sm:py-32",
  titleClass = "text-center text-4xl md:text-5xl font-bold",
  subtitleClass = "text-xl text-muted-foreground text-center mt-4 mb-8",
  formClass = "flex flex-col w-full md:flex-row md:w-6/12 lg:w-4/12 mx-auto gap-4 md:gap-2",
}: NewsletterSignupProps) {
  const [email, setEmail] = useState(input?.defaultValue ?? "");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [msg, setMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMsg(null);

    const value = email.trim();
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    if (!isValid) {
      setStatus("error");
      setMsg(errorText);
      return;
    }

    if (!api?.url) {
      // no endpoint: just demo success
      setStatus("success");
      setMsg(successText);
      // eslint-disable-next-line no-console
      console.log("Newsletter demo submit:", { email: value });
      return;
    }

    try {
      setStatus("loading");
      const method = api.method ?? "POST";
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(api.headers ?? {}),
      };

      const body =
        method === "GET"
          ? undefined
          : JSON.stringify({ email: value, ...(api.extraBody ?? {}) });

      const url =
        method === "GET"
          ? new URL(
              api.url +
                (api.url.includes("?") ? "&" : "?") +
                new URLSearchParams({ email: value }).toString()
            ).toString()
          : api.url;

      const res = await fetch(url, { method, headers, body });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      setStatus("success");
      setMsg(successText);
      setEmail("");
    } catch (err) {
      setStatus("error");
      setMsg("Something went wrong. Please try again.");
      // eslint-disable-next-line no-console
      console.error("Newsletter submit failed:", err);
    }
  };

  return (
    <section id={id} className={sectionClass}>
      {showTopDivider && <hr className="w-11/12 mx-auto" />}

      <div className={containerClass}>
        <h3 className={titleClass}>
          {title.map((seg, i) => (
            <span key={i} className={seg.className}>
              {seg.text}
            </span>
          ))}
        </h3>

        {subtitle && <p className={subtitleClass}>{subtitle}</p>}

        <form className={formClass} onSubmit={handleSubmit}>
          <Input
            type="email"
            name={input?.name ?? "email"}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder={input?.placeholder}
            aria-label={input?.ariaLabel ?? "email"}
            required={input?.required ?? true}
            className={cn("bg-muted/50 dark:bg-muted/80", input?.className)}
            disabled={status === "loading"}
          />
          <Button
            type="submit"
            variant={button.variant ?? "default"}
            size={button.size ?? "default"}
            className={cn(button.className)}
            disabled={status === "loading"}
          >
            {status === "loading" ? "Submitting..." : button.text}
          </Button>
        </form>

        {msg && (
          <p
            className={cn(
              "mt-3 text-center text-sm",
              status === "success" ? "text-green-600" : "text-destructive"
            )}
          >
            {msg}
          </p>
        )}
      </div>

      {showBottomDivider && <hr className="w-11/12 mx-auto" />}
    </section>
  );
}
