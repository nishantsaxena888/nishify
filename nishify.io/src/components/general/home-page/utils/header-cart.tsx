"use client";

import Link from "next/link";
import { ShoppingCart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useCart } from "./cart-provider";

export function HeaderCart({ link }: { link: string }) {
  const { state } = useCart();

  return (
    <Link href={link}>
      <Button variant="ghost" size="icon" className="relative">
        <ShoppingCart className="h-5 w-5" />
        {state.itemCount > 0 && (
          <Badge className="absolute -top-2 -right-2 h-5 w-5 flex items-center justify-center p-0 bg-primary">
            {state.itemCount}
          </Badge>
        )}
      </Button>
    </Link>
  );
}
