import React from "react";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Button } from "../ui/button";
import Link from "next/link";

export const Register = () => {
  return (
    <div className="flex pb-8 lg:h-screen lg:pb-0">
      <div className="hidden w-1/2 bg-gray-100 lg:block">
        <img
          alt="shadcn/ui login page"
          loading="lazy"
          width="1000"
          height="1000"
          decoding="async"
          data-nimg="1"
          className="h-full w-full object-cover"
          style={{ color: "transparent" }}
          src="https://bundui-images.netlify.app/extra/image4.jpg"
        />
      </div>
      <div className="flex w-full items-center justify-center lg:w-1/2">
        <div className="w-full max-w-md space-y-8 px-4">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-bold">Create New Account</h2>
          </div>
          <form className="mt-8 space-y-6">
            <div className="space-y-4">
              <div>
                <Label
                  data-slot="label"
                  className="flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50 sr-only"
                  htmlFor="first_name"
                >
                  First name
                </Label>
                <Input
                  type="text"
                  data-slot="input"
                  id="first_name"
                  required
                  placeholder="First name"
                  name="first_name"
                />
              </div>
              <div>
                <label
                  data-slot="label"
                  className="flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50 sr-only"
                  htmlFor="last_name"
                >
                  Last name
                </label>
                <Input
                  type="text"
                  data-slot="input"
                  id="last_name"
                  required
                  placeholder="Last name"
                  name="last_name"
                />
              </div>
              <div>
                <label
                  data-slot="label"
                  className="flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50 sr-only"
                  htmlFor="email"
                >
                  Email address
                </label>
                <Input
                  type="email"
                  data-slot="input"
                  id="email"
                  autoComplete="email"
                  required
                  placeholder="Email address"
                  name="email"
                />
              </div>
              <div>
                <label
                  data-slot="label"
                  className="flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50 sr-only"
                  htmlFor="password"
                >
                  Password
                </label>
                <Input
                  type="password"
                  data-slot="input"
                  id="password"
                  autoComplete="current-password"
                  required
                  placeholder="Password"
                  name="password"
                />
              </div>
            </div>
            <div>
              <Button data-slot="button" className="w-full" type="submit">
                Register
              </Button>
            </div>
          </form>
          <div className="mt-6">
            <div className="flex items-center gap-3">
              <div className="w-full border-t"></div>
              <span className="text-muted-foreground shrink-0 text-sm">
                Already have an account
              </span>
              <div className="w-full border-t"></div>
            </div>
            <div className="mt-6 grid  gap-3">
              <Button type="button" variant={"outline"}>
                <svg viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  ></path>
                  <path
                    fill="currentColor"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  ></path>
                  <path
                    fill="currentColor"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  ></path>
                  <path
                    fill="currentColor"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  ></path>
                </svg>
                Google
              </Button>
            </div>
            <div className="mt-6 text-center text-sm">
              <span className="pr-1">{`Don't have an account?`}</span>
              <Link className="underline" href="/auth/login">
                Login
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
