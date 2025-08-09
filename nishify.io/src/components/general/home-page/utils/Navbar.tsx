"use client";
import { useState } from "react";
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

import { GithubIcon, Menu } from "lucide-react";
import { LogoIcon } from "./Icons";
import Link from "next/link";
// import { ModeToggle } from "./mode-toggle";
import { buttonVariants } from "@/components/ui/button";
import { ThemeSwitcher } from "@/components/ThemeSwitcher";
import { ModeToggle } from "@/components/mode-toggle";
import { HeaderCart } from "./header-cart";

interface RouteProps {
  href: string;
  label: string;
}

const routeList: RouteProps[] = [
  {
    href: "/home/#product",
    label: "Product",
  },
  {
    href: "/home/#features",
    label: "Features",
  },
  {
    href: "/home/#testimonials",
    label: "Testimonials",
  },
  {
    href: "/home/#pricing",
    label: "Pricing",
  },
  {
    href: "/home/#faq",
    label: "FAQ",
  },
];

export const Navbar = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  return (
    <header className="sticky border-b-[1px] top-0 z-40 w-full bg-white dark:border-b-slate-700 dark:bg-background">
      <NavigationMenu className="mx-auto">
        <NavigationMenuList className="container h-14 px-4 w-screen flex justify-between ">
          <NavigationMenuItem className="font-bold flex">
            <Link
              rel="noreferrer noopener"
              href="/"
              className="ml-2 font-bold text-xl flex"
            >
              <LogoIcon />
              ShadcnUI/React
            </Link>
          </NavigationMenuItem>

          {/* mobile */}
          <span className="flex md:hidden">
            <ModeToggle />
            <ThemeSwitcher />
            <HeaderCart link="/cart" />

            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger className="px-2">
                <Menu
                  className="flex md:hidden h-5 w-5"
                  onClick={() => setIsOpen(true)}
                >
                  <span className="sr-only">Menu Icon</span>
                </Menu>
              </SheetTrigger>

              <SheetContent side={"left"}>
                <SheetHeader>
                  <SheetTitle className="font-bold text-xl">
                    Shadcn/React
                  </SheetTitle>
                </SheetHeader>
                <nav className="flex flex-col justify-center items-center gap-2 mt-4">
                  {routeList.map(({ href, label }: RouteProps) => (
                    <a
                      rel="noreferrer noopener"
                      key={label}
                      href={href}
                      onClick={() => setIsOpen(false)}
                      className={buttonVariants({ variant: "ghost" })}
                    >
                      {label}
                    </a>
                  ))}
                  <a
                    rel="noreferrer noopener"
                    href="https://github.com/leoMirandaa/shadcn-landing-page.git"
                    target="_blank"
                    className={`w-[110px] border ${buttonVariants({
                      variant: "secondary",
                    })}`}
                  >
                    <GithubIcon className="mr-2 w-5 h-5" />
                    Github
                  </a>
                </nav>
              </SheetContent>
            </Sheet>
          </span>

          {/* desktop */}
          <nav className="hidden md:flex gap-2">
            {routeList.map((route: RouteProps, i) => (
              <a
                rel="noreferrer noopener"
                href={route.href}
                key={i}
                className={`text-[17px] ${buttonVariants({
                  variant: "ghost",
                })}`}
              >
                {route.label}
              </a>
            ))}
          </nav>

          <div className="hidden md:flex gap-2">
            <ModeToggle />
            <ThemeSwitcher />
            <HeaderCart link="/cart" />
          </div>
        </NavigationMenuList>
      </NavigationMenu>
    </header>
  );
};
