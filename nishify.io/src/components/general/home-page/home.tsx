"use client";
import React, { useEffect, useState } from "react";
import { Navbar } from "./utils/Navbar";
import { Hero } from "./utils/Hero";
import { Sponsors } from "./utils/Sponsors";
import { About } from "./utils/About";
import { HowItWorks } from "./utils/HowItWorks";
import { Features } from "./utils/Features";
import { Cta } from "./utils/Cta";
import { Services } from "./utils/Services";
import { FAQ } from "./utils/FAQ";
import { Testimonials } from "./utils/Testimonials";
import { Team } from "./utils/Team";
import { Pricing } from "./utils/Pricing";
import { Newsletter } from "./utils/Newsletter";
import { Footer } from "./utils/Footer";
import { ScrollToTop } from "./utils/ScrollToTop";
import { ProductsPage } from "./utils/Product";
import { CartProvider } from "./utils/cart-provider";

export const Home = () => {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  return (
    <div className="dark:bg-black/70">
      {isClient ? <Navbar /> : null}
      {/* <Navbar /> */}
      <Hero />
      <Sponsors />
      <About />
      <ProductsPage />
      <HowItWorks />
      <Features />
      <Services />
      <Cta />
      <Testimonials />
      <Team />
      <Pricing />
      <Newsletter />
      <FAQ />
      <Footer />
      <ScrollToTop />
    </div>
  );
};
