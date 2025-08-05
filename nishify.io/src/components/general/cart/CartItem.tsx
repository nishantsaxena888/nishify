"use client";

import Image from "next/image";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Trash2, Plus, Minus } from "lucide-react";
import {
  type CartItem as CartItemType,
  useCart,
} from "../home-page/utils/cart-provider";
// import {
//   type CartItem as CartItemType,
//   useCart,
// } from "@/components/cart-provider";

interface CartItemProps {
  item: CartItemType;
}

export function CartItem({ item }: CartItemProps) {
  const { dispatch } = useCart();

  const updateQuantity = (quantity: number) => {
    dispatch({ type: "UPDATE_QUANTITY", payload: { id: item.id, quantity } });
  };

  const removeItem = () => {
    dispatch({ type: "REMOVE_ITEM", payload: item.id });
  };

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center space-x-4">
          <div className="relative w-20 h-20 flex-shrink-0">
            <Image
              src={item.image || "/placeholder.svg"}
              alt={item.name}
              fill
              className="object-cover rounded-md"
            />
          </div>

          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold  truncate">{item.name}</h3>
            <p className="text-muted-foreground text-sm truncate max-w-[80%]">
              {item.description}
            </p>
            <p className="text-muted-foreground font-semibold">${item.price}</p>
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => updateQuantity(item.quantity - 1)}
              disabled={item.quantity <= 1}
            >
              <Minus className="h-4 w-4" />
            </Button>
            <Input
              type="number"
              value={item.quantity}
              onChange={(e) =>
                updateQuantity(Number.parseInt(e.target.value) || 1)
              }
              className="w-16 text-center"
              min="1"
            />
            <Button
              variant="outline"
              size="icon"
              onClick={() => updateQuantity(item.quantity + 1)}
            >
              <Plus className="h-4 w-4" />
            </Button>
          </div>

          <div className="text-right flex ">
            <p className="text-lg font-semibold">
              ${(item.price * item.quantity).toFixed(2)}
            </p>
            <Button
              variant="ghost"
              size="sm"
              onClick={removeItem}
              className="text-red-500 hover:text-red-700 hover:bg-red-50"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
