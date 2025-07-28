/* eslint-disable react-hooks/exhaustive-deps */
"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { Palette } from "lucide-react";

const themes = [
  { label: "Amberland (Light)", theme: "amberland", mode: "light" },
  { label: "Amberland (Dark)", theme: "amberland", mode: "dark" },
  { label: "Emeraldline (Light)", theme: "emeraldline", mode: "light" },
  { label: "Emeraldline (Dark)", theme: "emeraldline", mode: "dark" },
  { label: "Default (Light)", theme: "default", mode: "light" },
  { label: "Default (Dark)", theme: "default", mode: "dark" },
];

export function ThemeSwitcher() {
  const [mounted, setMounted] = useState(false);
  const [theme, setTheme] = useState("amberland");
  const [mode, setMode] = useState<"light" | "dark">("light");
  const { theme: currentTheme, setTheme: setGlobalTheme } = useTheme();

  // 1. Initial read from localStorage
  useEffect(() => {
    const storedTheme = localStorage.getItem("brand-theme") || "amberland";
    const storedMode =
      (localStorage.getItem("color-mode") as "light" | "dark") || "light";
    setTheme(storedTheme);
    setMode(storedMode);
    setMounted(true);
  }, []);

  useEffect(() => {
    if (currentTheme !== theme) {
      setMode(currentTheme as "light" | "dark");
    }
  }, [currentTheme]);

  // 2. Apply classes
  useEffect(() => {
    if (!mounted) return;

    document.body.classList.remove(
      "theme-amberland",
      "theme-emeraldline",
      "theme-default",
      "light",
      "dark"
    );

    document.body.classList.add(`theme-${theme}`, mode);

    console.log(`Applied: theme-${theme} ${mode}`);
    localStorage.setItem("brand-theme", theme);
    localStorage.setItem("color-mode", mode);
  }, [theme, mode, mounted]);

  const handleClick = (t: string, m: "light" | "dark") => {
    setTheme(t);
    setMode(m);
    setGlobalTheme(m);
  };

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline">
            <Palette />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56" align="start">
          <DropdownMenuLabel className="font-bold">
            Change Theme
          </DropdownMenuLabel>
          <DropdownMenuSeparator />

          <DropdownMenuGroup className="space-y-1">
            {themes.map(({ label, theme: t, mode: m }) => (
              <DropdownMenuItem asChild key={`${t}-${m}`}>
                <Button
                  variant={theme === t && mode === m ? "default" : "ghost"}
                  onClick={() => handleClick(t, m as "light" | "dark")}
                  className="w-full justify-start "
                >
                  {label}
                </Button>
              </DropdownMenuItem>
            ))}
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </>
  );
}
