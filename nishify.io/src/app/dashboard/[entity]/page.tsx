// src/app/dashboard/[entity]/page.tsx
import AdminShell from '@/components/admin/AdminShell'

export default function Page({ params }: { params: { entity: string } }) {
  return <AdminShell entity={params.entity} />
}
