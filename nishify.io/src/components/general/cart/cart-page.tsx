import React from "react";
import { Navbar } from "../home-page/utils/Navbar";
import CartList from "./cart-list";

export const CartPage = () => {
  return (
    <div className="dark:bg-black/70">
      <Navbar />
      <CartList />
    </div>
  );
};
