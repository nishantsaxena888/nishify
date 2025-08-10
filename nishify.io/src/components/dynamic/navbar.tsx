"use client";

import { useState } from "react";
import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { buttonVariants } from "@/components/ui/button";
import { ThemeSwitcher } from "@/components/ThemeSwitcher";
import { ModeToggle } from "@/components/mode-toggle";
import { LogoIcon } from "./Icons";
import { GithubIcon, Menu } from "lucide-react";
import { HeaderCart } from "../general/home-page/utils/header-cart";

/* --------------------- Types --------------------- */
export type NavRoute = {
  href: string;
  label: string;
  target?: "_blank" | "_self";
};
export type Brand = { text: string; href?: string };

export type Actions = {
  showModeToggle?: boolean;
  showThemeSwitcher?: boolean;
  cartLink?: string; // if provided, show cart
  github?: { href: string; text?: string }; // shown inside mobile sheet
};

export type NavbarProps = {
  brand?: Brand;
  routes?: NavRoute[];
  actions?: Actions;
  sticky?: boolean;
  className?: string;
};

/* --------------------- Component --------------------- */
export default function Navbar({
  brand /* = { text: "ShadcnUI/React", href: "/" } */,
  routes /*  = [
    { href: "/home/#product", label: "Product" },
    { href: "/home/#features", label: "Features" },
    { href: "/home/#testimonials", label: "Testimonials" },
    { href: "/home/#pricing", label: "Pricing" },
    { href: "/home/#faq", label: "FAQ" },
  ] */,
  actions /*  = {
    showModeToggle: true,
    showThemeSwitcher: true,
    cartLink: "/cart",
    github: {
      href: "https://github.com/leoMirandaa/shadcn-landing-page.git",
      text: "Github",
    },
  } */,
  sticky = true,
  className = "",
}: NavbarProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header
      className={[
        sticky
          ? "sticky top-0 z-40 bg-white dark:bg-background border-b dark:border-b-slate-700"
          : "",
        className,
      ].join(" ")}
    >
      <NavigationMenu className="mx-auto">
        <NavigationMenuList className="container h-14 px-4 w-screen flex justify-between">
          {/* Brand */}
          <NavigationMenuItem className="font-bold flex">
            <Link
              href={brand?.href ?? "/"}
              className="ml-2 font-bold text-xl flex"
            >
              <LogoIcon />
              {brand?.text}
            </Link>
          </NavigationMenuItem>

          {/* Mobile actions + menu */}
          <span className="flex md:hidden items-center gap-1">
            {actions?.showModeToggle && <ModeToggle />}
            {actions?.showThemeSwitcher && <ThemeSwitcher />}
            {actions?.cartLink && <HeaderCart link={actions.cartLink} />}

            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger className="px-2">
                <Menu className="h-5 w-5"></Menu>
                <span className="sr-only">Menu Icon</span>
              </SheetTrigger>

              <SheetContent side="left">
                <SheetHeader>
                  <SheetTitle className="font-bold text-xl">
                    {brand?.text.replace("/", "/")}
                  </SheetTitle>
                </SheetHeader>

                <nav className="flex flex-col justify-center items-center gap-2 mt-4">
                  {routes?.map((r) => (
                    <a
                      key={r.href}
                      href={r.href}
                      target={r.target}
                      rel="noreferrer noopener"
                      onClick={() => setIsOpen(false)}
                      className={buttonVariants({ variant: "ghost" })}
                    >
                      {r.label}
                    </a>
                  ))}

                  {actions?.github && (
                    <a
                      href={actions.github.href}
                      target="_blank"
                      rel="noreferrer noopener"
                      className={`w-[110px] border ${buttonVariants({
                        variant: "secondary",
                      })}`}
                    >
                      <GithubIcon className="mr-2 w-5 h-5" />
                      {actions.github.text ?? "Github"}
                    </a>
                  )}
                </nav>
              </SheetContent>
            </Sheet>
          </span>

          {/* Desktop nav */}
          <nav className="hidden md:flex gap-2">
            {routes?.map((r) => (
              <a
                key={r.href}
                href={r.href}
                target={r.target}
                rel="noreferrer noopener"
                className={`text-[17px] ${buttonVariants({
                  variant: "ghost",
                })}`}
              >
                {r.label}
              </a>
            ))}
          </nav>

          {/* Desktop actions */}
          <div className="hidden md:flex gap-2">
            {actions?.showModeToggle && <ModeToggle />}
            {actions?.showThemeSwitcher && <ThemeSwitcher />}
            {actions?.cartLink && <HeaderCart link={actions.cartLink} />}
          </div>
        </NavigationMenuList>
      </NavigationMenu>
    </header>
  );
}
