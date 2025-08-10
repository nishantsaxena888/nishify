/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import HomeClientWrapper from "@/components/dynamic/home-client-wrapper";
import { cn } from "@/lib/utils";
import { GalleryVerticalEnd } from "lucide-react";
import React from "react";

import { Card, CardContent } from "@/components/ui/card";
import { useRouter } from "next/navigation";

const AuthTemplate = (prop: any) => {
  const { push } = useRouter();
  const submitHandler = (prop: any) => {
    push("/dashboard");
  };

  const formJson = [{ ...prop.template, onSubmit: submitHandler }];

  console.log(formJson);

  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
      <div className="absolute inset-0  h-full w-full items-center px-5 py-24 auth-bg"></div>

      <div className="flex w-full max-w-md flex-col gap-6 relative">
        <a href="#" className="flex items-center gap-2 self-center font-medium">
          <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <GalleryVerticalEnd className="size-4" />
          </div>
          {prop.company}
        </a>
        <div className={cn("flex flex-col gap-6")}>
          <Card>
            <CardContent className="py-7">
              <HomeClientWrapper sections={formJson} />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AuthTemplate;
