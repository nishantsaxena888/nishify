/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface Filters {
  category: string;
  brand: string;
  priceRange: number[];
  inStock: boolean;
  rating: number;
}

interface ProductFiltersProps {
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
}

export function ProductFilters({
  filters,
  onFiltersChange,
}: ProductFiltersProps) {
  const updateFilter = (key: keyof Filters, value: any) => {
    onFiltersChange({ ...filters, [key]: value });
  };

  const clearFilters = () => {
    onFiltersChange({
      category: "all",
      brand: "all",
      priceRange: [0, 500],
      inStock: false,
      rating: 0,
    });
  };

  return (
    <Card className="sticky top-20">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Filters</CardTitle>
          <Button variant="ghost" size="sm" onClick={clearFilters}>
            Clear All
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Category Filter */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Category</Label>
          <Select
            value={filters.category}
            onValueChange={(value) => updateFilter("category", value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              <SelectItem value="Electronics">Electronics</SelectItem>
              <SelectItem value="Accessories">Accessories</SelectItem>
              <SelectItem value="Clothing">Clothing</SelectItem>
              <SelectItem value="Home">Home</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Separator />

        {/* Brand Filter */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Brand</Label>
          <Select
            value={filters.brand}
            onValueChange={(value) => updateFilter("brand", value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="All Brands" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Brands</SelectItem>
              <SelectItem value="TechPro">TechPro</SelectItem>
              <SelectItem value="WearTech">WearTech</SelectItem>
              <SelectItem value="CarryAll">CarryAll</SelectItem>
              <SelectItem value="SoundWave">SoundWave</SelectItem>
              <SelectItem value="FitLife">FitLife</SelectItem>
              <SelectItem value="ProtectPro">ProtectPro</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Separator />

        {/* Price Range Filter */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">
            Price Range: ${filters.priceRange[0]} - ${filters.priceRange[1]}
          </Label>
          <Slider
            value={filters.priceRange}
            onValueChange={(value) => updateFilter("priceRange", value)}
            max={500}
            min={0}
            step={10}
            className="w-full"
          />
        </div>

        <Separator />

        {/* Stock Filter */}
        <div className="flex items-center space-x-2">
          <Checkbox
            id="inStock"
            checked={filters.inStock}
            onCheckedChange={(checked) => updateFilter("inStock", checked)}
          />
          <Label htmlFor="inStock" className="text-sm">
            In Stock Only
          </Label>
        </div>

        <Separator />

        {/* Rating Filter */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Minimum Rating</Label>
          <Select
            value={filters.rating.toString()}
            onValueChange={(value) =>
              updateFilter("rating", Number.parseFloat(value))
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="Any Rating" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="0">Any Rating</SelectItem>
              <SelectItem value="4">4+ Stars</SelectItem>
              <SelectItem value="4.5">4.5+ Stars</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>
  );
}
