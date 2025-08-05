"use client";

import { useState, useMemo } from "react";
import { ProductCard } from "./ProductCard";
import { Button } from "@/components/ui/button";
import { Grid, List } from "lucide-react";
import { ProductFilters } from "./ProductFilters";

// Mock product data
const products = [
  {
    id: "1",
    name: "Wireless Headphones",
    price: 199.99,
    image: "/assets/placeholder.svg?height=300&width=300",
    description:
      "Premium wireless headphones with noise cancellation and superior sound quality.",
    category: "Electronics",
    brand: "TechPro",
    rating: 4.5,
    inStock: true,
  },
  {
    id: "2",
    name: "Smart Watch",
    price: 299.99,
    image: "/assets/placeholder.svg?height=300&width=300",
    description: "Advanced smartwatch with health monitoring and GPS tracking.",
    category: "Electronics",
    brand: "WearTech",
    rating: 4.3,
    inStock: true,
  },
  {
    id: "3",
    name: "Laptop Backpack",
    price: 79.99,
    image: "/assets/placeholder.svg?height=300&width=300",
    description:
      "Durable laptop backpack with multiple compartments and water resistance.",
    category: "Accessories",
    brand: "CarryAll",
    rating: 4.7,
    inStock: true,
  },
  {
    id: "4",
    name: "Bluetooth Speaker",
    price: 89.99,
    image: "/assets/placeholder.svg?height=300&width=300",
    description:
      "Portable Bluetooth speaker with 360-degree sound and long battery life.",
    category: "Electronics",
    brand: "SoundWave",
    rating: 4.2,
    inStock: false,
  },
  {
    id: "5",
    name: "Fitness Tracker",
    price: 149.99,
    image: "/assets/placeholder.svg?height=300&width=300",
    description:
      "Advanced fitness tracker with heart rate monitoring and sleep tracking.",
    category: "Electronics",
    brand: "FitLife",
    rating: 4.4,
    inStock: true,
  },
  {
    id: "6",
    name: "Phone Case",
    price: 24.99,
    image: "/assets/placeholder.svg?height=300&width=300",
    description:
      "Protective phone case with shock absorption and wireless charging support.",
    category: "Accessories",
    brand: "ProtectPro",
    rating: 4.1,
    inStock: true,
  },
];

export function ProductsPage() {
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [filters, setFilters] = useState({
    category: "",
    brand: "",
    priceRange: [0, 500],
    inStock: false,
    rating: 0,
  });

  const filteredProducts = useMemo(() => {
    return products.filter((product) => {
      if (filters.category && product.category !== filters.category)
        return false;
      if (filters.brand && product.brand !== filters.brand) return false;
      if (
        product.price < filters.priceRange[0] ||
        product.price > filters.priceRange[1]
      )
        return false;
      if (filters.inStock && !product.inStock) return false;
      if (filters.rating && product.rating < filters.rating) return false;
      return true;
    });
  }, [filters]);

  return (
    <div className="min-h-screen" id="product">
      <div className="max-w-[90%] mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filters */}
          <div className="lg:w-64 flex-shrink-0">
            <ProductFilters filters={filters} onFiltersChange={setFilters} />
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold ">Products</h1>
                <p className="text-muted-foreground mt-1">
                  Showing {filteredProducts.length} of {products.length}{" "}
                  products
                </p>
              </div>

              <div className="flex items-center space-x-2">
                <Button
                  variant={viewMode === "grid" ? "default" : "outline"}
                  size="icon"
                  onClick={() => setViewMode("grid")}
                  className={
                    viewMode === "grid" ? "bg-primary hover:opacity-80" : ""
                  }
                >
                  <Grid className="h-4 w-4" />
                </Button>
                <Button
                  variant={viewMode === "list" ? "default" : "outline"}
                  size="icon"
                  onClick={() => setViewMode("list")}
                  className={
                    viewMode === "list" ? "bg-primary hover:opacity-80" : ""
                  }
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Products Grid */}
            <div
              className={
                viewMode === "grid"
                  ? "grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
                  : "space-y-4"
              }
            >
              {filteredProducts.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  viewMode={viewMode}
                />
              ))}
            </div>

            {filteredProducts.length === 0 && (
              <div className="text-center py-12">
                <p className="text-muted-foreground text-lg">
                  No products found matching your filters.
                </p>
                <Button
                  onClick={() =>
                    setFilters({
                      category: "",
                      brand: "",
                      priceRange: [0, 500],
                      inStock: false,
                      rating: 0,
                    })
                  }
                  className="mt-4 bg-primary hover:opacity-90"
                >
                  Clear Filters
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
