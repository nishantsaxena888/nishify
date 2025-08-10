/* eslint-disable @typescript-eslint/no-explicit-any */
import HomeClientWrapper from "@/components/dynamic/home-client-wrapper";
import login from "@/clients/pioneer_wholesale_inc/login.json";
import register from "@/clients/pioneer_wholesale_inc/register.json";
import forgot_password from "@/clients/pioneer_wholesale_inc/forgot-password.json";

type PageData = { sections?: any[] };

export default async function WebPage({
  params,
}: {
  // Next 15: params may be a Promise
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params; // ✅ MUST await in Next 15

  const DATA: Record<string, PageData> = {
    login,
    register,
    "forgot-password": forgot_password,
  };

  // If slug not found, don't crash — show empty page or wire a fallback
  const page = DATA[slug];
  if (!page?.sections) {
    // Option A: empty wrapper (no 500s)
    return <HomeClientWrapper sections={[]} />;

    // Option B (recommended once you add 404 page):
    // import { notFound } from "next/navigation";
    // notFound();
  }

  return <HomeClientWrapper sections={page.sections} />;
}
