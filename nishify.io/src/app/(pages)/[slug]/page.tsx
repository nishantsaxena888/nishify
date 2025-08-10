/* eslint-disable @typescript-eslint/no-explicit-any */
import HomeClientWrapper from "@/components/dynamic/home-client-wrapper";
import login from "@/clients/pioneer_wholesale_inc/login.json";
import register from "@/clients/pioneer_wholesale_inc/register.json";
import forgot_password from "@/clients/pioneer_wholesale_inc/forgot-password.json";

export default function WebPage(prop: { params: { slug: string } }) {
  const DATA: any = {
    login: login,
    register: register,
    "forgot-password": forgot_password,
  };
  return <HomeClientWrapper sections={DATA[prop.params.slug].sections} />;
}
