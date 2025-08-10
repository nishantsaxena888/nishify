// src/app/dashboard/[entity]/page.tsx
import AdminShell from "@/components/admin/AdminShell";

export default async function Page({
  params,
}: {
  params: Promise<{ entity: string }>;
}) {
  const { entity } = await params; // Next App Router: params is async
  return <AdminShell entity={entity} />;
}
