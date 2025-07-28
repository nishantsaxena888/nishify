import { Login } from "@/components/auth-component/login";
import { Register } from "@/components/auth-component/register";
import { FormExample } from "@/components/dashboard-component/admin-pages/form-example";
import { ListExample } from "@/components/dashboard-component/admin-pages/list-example";
import { DashboardTemplate } from "@/components/dashboard-component/dashboard-template";
import React, { Fragment } from "react";

const AuthPages = (prop: { params: { slug: string } }) => {
  return (
    <Fragment>
      {prop.params.slug === "login" ? <Login /> : null}
      {prop.params.slug === "register" ? <Register /> : null}
    </Fragment>
  );
};
export default AuthPages;
