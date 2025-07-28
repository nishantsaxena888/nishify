import { FormExample } from "@/components/dashboard-component/admin-pages/form-example";
import { ListExample } from "@/components/dashboard-component/admin-pages/list-example";
import { DashboardTemplate } from "@/components/dashboard-component/dashboard-template";
import React from "react";

const AdminPages = (prop: { params: { slug: string } }) => {
  return (
    <DashboardTemplate name={prop.params.slug}>
      {prop.params.slug === "forms" ? <FormExample /> : null}
      {prop.params.slug === "table" ? <ListExample /> : null}
    </DashboardTemplate>
  );
};
export default AdminPages;
