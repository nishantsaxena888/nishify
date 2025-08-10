import { ForgotPassword } from "@/components/auth-component/forgot-password";
import { Login } from "@/components/auth-component/login";
import { Register } from "@/components/auth-component/register";
import { ResetPassword } from "@/components/auth-component/reset-password";
import PrivacyPolicy from "@/components/general/privacy-policy";
import TermsOfService from "@/components/general/terms-of-service";
import React, { Fragment } from "react";
import { notFound } from "next/navigation";
import { Home } from "@/components/general/home-page/home";
import { CartPage } from "@/components/general/cart/cart-page";
import { CartProvider } from "@/components/general/home-page/utils/cart-provider";
import { CheckoutPage } from "@/components/general/checkout/checkout-page";

const Pages = (prop: { params: { slug: string } }) => {
  const NAVIGATION = [
    { component: Login, href: "login" },
    { component: Register, href: "register" },
    { component: ForgotPassword, href: "forgot-password" },
    { component: ResetPassword, href: "reset-password" },
    { component: TermsOfService, href: "terms-of-service" },
    { component: PrivacyPolicy, href: "privacy-policy" },
    { component: Home, href: "home" },
    { component: CartPage, href: "cart" },
    { component: CheckoutPage, href: "checkout" },
  ];

  const currentPage = NAVIGATION.find((item) => item.href === prop.params.slug);

  if (!currentPage) {
    notFound();
  }

  const Page = currentPage.component;

  if (NAVIGATION.some((item) => item.href === prop.params.slug)) {
    return <Page />;
  }
};

export default Pages;
