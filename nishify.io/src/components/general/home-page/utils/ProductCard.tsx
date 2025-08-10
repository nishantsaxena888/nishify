"use client";

import Image from "next/image";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Star, ShoppingCart } from "lucide-react";
import { type Product, useCart } from "./cart-provider";

interface ProductCardProps {
  product: Product;
  viewMode?: "grid" | "list";
}

export function ProductCard({ product, viewMode = "grid" }: ProductCardProps) {
  const { dispatch } = useCart();
  //   const { toast } = useToast();

  const addToCart = () => {
    dispatch({ type: "ADD_ITEM", payload: product });
    // toast({
    //   title: "Added to cart",
    //   description: `${product.name} has been added to your cart.`,
    // });
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${
          i < Math.floor(rating)
            ? "fill-yellow-400 text-yellow-400"
            : "text-gray-300"
        }`}
      />
    ));
  };

  if (viewMode === "list") {
    return (
      <Card className="overflow-hidden hover:shadow-lg transition-shadow py-0">
        <CardContent className="p-0">
          <div className="flex">
            <div className="relative w-48 h-48 flex-shrink-0">
              <Image
                src={product.image || "/placeholder.svg"}
                alt={product.name}
                fill
                className="object-cover"
              />
              {!product.inStock && (
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                  <Badge variant="secondary">Out of Stock</Badge>
                </div>
              )}
            </div>
            <div className="flex-1 px-6 py-3 flex flex-col justify-between">
              <div>
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-lg font-semibold ">{product.name}</h3>
                  <span className="text-xl font-bold text-primary">
                    ${product.price}
                  </span>
                </div>
                <p className="text-muted-foreground mb-3">
                  {product.description}
                </p>
                <div className="flex items-center space-x-4 mb-3">
                  <div className="flex items-center space-x-1">
                    {renderStars(product.rating)}
                    <span className="text-sm text-muted-foreground">
                      ({product.rating})
                    </span>
                  </div>
                  <Badge variant="outline">{product.brand}</Badge>
                </div>
              </div>
              <Button
                onClick={addToCart}
                disabled={!product.inStock}
                className="bg-primary hover:bg-primary w-fit"
              >
                <ShoppingCart className="h-4 w-4 mr-2" />
                Add to Cart
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow group pt-0 ">
      <CardContent className="p-0">
        <div className="relative aspect-square overflow-hidden">
          <Image
            src={product.image || "/placeholder.svg"}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
          />
          {!product.inStock && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <Badge variant="secondary">Out of Stock</Badge>
            </div>
          )}
        </div>
        <div className="pb-1 pt-5 px-3">
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-lg font-semibold  line-clamp-1">
              {product.name}
            </h3>
            <span className="text-lg font-bold text-primary">
              ${product.price}
            </span>
          </div>
          <p className="text-muted-foreground text-sm mb-3 line-clamp-2">
            {product.description}
          </p>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-1">
              {renderStars(product.rating)}
              <span className="text-sm text-muted-foreground">
                ({product.rating})
              </span>
            </div>
            <Badge variant="outline" className="text-xs">
              {product.brand}
            </Badge>
          </div>
          <Button
            onClick={addToCart}
            disabled={!product.inStock}
            className="w-full bg-primary hover:bg-opacity-50 "
          >
            <ShoppingCart className="h-4 w-4 mr-2" />
            Add to Cart
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
