"use client";
import { cn } from "@/lib/utils";
import { GalleryVerticalEnd } from "lucide-react";
import React from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { useRouter } from "next/navigation";

export const Login = () => {
  const { push } = useRouter();
  const submitHandler = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    push("/dashboard");
  };
  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
      <div className="absolute inset-0  h-full w-full items-center px-5 py-24 auth-bg"></div>

      <div className="flex w-full max-w-sm flex-col gap-6 relative">
        <a href="#" className="flex items-center gap-2 self-center font-medium">
          <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <GalleryVerticalEnd className="size-4" />
          </div>
          Acme Inc.
        </a>
        <div className={cn("flex flex-col gap-6")}>
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-xl">Welcome back</CardTitle>
              <CardDescription>
                Login with your Apple or Google account
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={submitHandler}>
                <div className="grid gap-6">
                  <div className="flex flex-col gap-4">
                    <Button variant="outline" className="w-full">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
                          fill="currentColor"
                        />
                      </svg>
                      Login with Google
                    </Button>
                  </div>
                  <div className="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t">
                    <span className="bg-card text-muted-foreground relative z-10 px-2">
                      Or continue with
                    </span>
                  </div>
                  <div className="grid gap-6">
                    <div className="grid gap-3">
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        placeholder="m@example.com"
                      />
                    </div>
                    <div className="grid gap-3">
                      <div className="flex items-center">
                        <Label htmlFor="password">Password</Label>
                        <Link
                          href="/forgot-password"
                          className="ml-auto text-sm underline-offset-4 hover:underline"
                        >
                          Forgot your password?
                        </Link>
                      </div>
                      <Input id="password" type="password" />
                    </div>
                    <Button type="submit" className="w-full">
                      Login
                    </Button>
                  </div>
                  <div className="text-center text-sm">
                    Don&apos;t have an account?{" "}
                    <Link
                      href="/register"
                      className="underline underline-offset-4"
                    >
                      Sign up
                    </Link>
                  </div>
                </div>
              </form>
            </CardContent>
          </Card>
          <div className="text-muted-foreground *:[a]:hover:text-primary text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
            By clicking continue, you agree to our{" "}
            <Link href="/terms-of-service">Terms of Service</Link> and{" "}
            <Link href="/privacy-policy">Privacy Policy</Link>.
          </div>
        </div>
      </div>
    </div>
  );
};
