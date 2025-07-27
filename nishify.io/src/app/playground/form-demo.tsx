"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { ExampleCombobox } from "./ExampleCombobox";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { Toggle } from "@/components/ui/toggle";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";

export default function ProductForm() {
  return (
    <form className="space-y-4 max-w-md">
      <div>
        <Label htmlFor="name">Product Name</Label>
        <Input id="name" placeholder="Enter product name" />
      </div>
      <div>
        <Label htmlFor="price">Price</Label>
        <Input id="price" type="number" placeholder="Enter price" />
      </div>
      <div>
        <Label htmlFor="checkbox">Checkbox</Label>
        <Checkbox id="checkbox" />
      </div>
      <div>
        <Label htmlFor="combo-box">Combo box</Label>
        <ExampleCombobox />
      </div>
      <div>
        <Label htmlFor="switch">Switch</Label>
        <Switch id="switch" />
      </div>
      <div>
        <Label htmlFor="textarea">Textarea</Label>
        <Textarea id="textarea" />
      </div>
      <div>
        <Label htmlFor="toggle">Toggle</Label>
        <Toggle>Toggle</Toggle>
      </div>
      <div>
        <Label htmlFor="single">ToggleGroup</Label>
        <br />
        <ToggleGroup variant="outline" type="multiple">
          <ToggleGroupItem value="a">A</ToggleGroupItem>
          <ToggleGroupItem value="b">B</ToggleGroupItem>
          <ToggleGroupItem value="c">C</ToggleGroupItem>
        </ToggleGroup>{" "}
      </div>
      <div>
        <Label htmlFor="price mb-1">Radio group</Label>
        <RadioGroup defaultValue="option-one">
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="option-one" id="option-one" />
            <Label htmlFor="option-one">Option One</Label>
          </div>
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="option-two" id="option-two" />
            <Label htmlFor="option-two">Option Two</Label>
          </div>
        </RadioGroup>
      </div>
      <Button type="submit">Submit</Button>
    </form>
  );
}
