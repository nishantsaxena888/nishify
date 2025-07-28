import React from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ChevronLeft } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { DropdownInput } from "@/components/form/input/dropdown-input";
import { MultiSelectDropdownInput } from "@/components/form/input/multi-select-dropdown-input";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { DatePickerDemo } from "@/app/playground/DatePickerDemo";

export const FormExample = () => {
  return (
    <div className={cn("px-5")}>
      <div className="flex flex-col mb-3 mt-2 md:flex-row justify-between">
        <CardTitle className="text-xl">Create Customer</CardTitle>
        <Button type="button" variant={"ghost"}>
          <ChevronLeft /> Back
        </Button>
      </div>
      <form>
        <Card className="max-h-[73dvh] overflow-y-auto">
          <CardContent>
            <Accordion type="single" className="w-full" defaultValue="item-1">
              <AccordionItem value="item-1">
                <AccordionTrigger className="text-md">
                  Account Information
                </AccordionTrigger>
                <AccordionContent className="flex  flex-col gap-4 text-balance">
                  <div className="grid gap-6 py-10 border-t  ">
                    <div className="grid gap-6 md:grid-cols-3 grid-cols-1">
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="email">Customer Code</Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Customer name <span className="text-red-500">*</span>
                        </Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Contact person name{" "}
                          <span className="text-red-500">*</span>
                        </Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Phone <span className="text-red-500">*</span>
                        </Label>
                        <Input type="tel" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">Email</Label>
                        <Input type="email" />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">fax</Label>
                        <Input type="tel" />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Boro</Label>
                        <Input type="number" />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Credit limit</Label>
                        <Input type="number" />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Product Promotion</Label>
                        <RadioGroup
                          defaultValue="no"
                          className="flex gap-2 pt-2"
                        >
                          <div className="flex items-center gap-3">
                            <RadioGroupItem value="yes" id="r1" />
                            <Label htmlFor="r1">Yes</Label>
                          </div>
                          <div className="flex items-center gap-3">
                            <RadioGroupItem value="no" id="r2" />
                            <Label htmlFor="r2">No</Label>
                          </div>
                        </RadioGroup>
                      </div>
                      <div className="flex flex-col gap-3 row-span-2">
                        <Label htmlFor="customer-fax">Customer Notes</Label>
                        <Textarea className="h-[100px]" />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Is inactive</Label>
                        <Switch />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Is msa include</Label>
                        <Switch />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">
                          Is sales tax applicable
                        </Label>
                        <Switch />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">
                          Send email on invoice creation
                        </Label>
                        <Switch />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Calculate interest</Label>
                        <Switch />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Self checkout tax</Label>
                        <Switch />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">
                          Cash and carry customer code
                        </Label>
                        <Switch />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Salesman</Label>
                        <DropdownInput
                          list={[
                            {
                              label: "Salesman 1",
                              value: "salesman-1",
                            },
                            {
                              label: "Salesman 2",
                              value: "salesman-2",
                            },
                            {
                              label: "Salesman 3",
                              value: "salesman-3",
                            },
                            {
                              label: "Salesman 4",
                              value: "salesman-4",
                            },
                          ]}
                          labelBind="label"
                          valueBind="value"
                          placeholder="Select salesman"
                          searchPlaceholder="Search salesman"
                        />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Customer type</Label>
                        <DropdownInput
                          list={[
                            {
                              label: "Salesman 1",
                              value: "salesman-1",
                            },
                            {
                              label: "Salesman 2",
                              value: "salesman-2",
                            },
                            {
                              label: "Salesman 3",
                              value: "salesman-3",
                            },
                            {
                              label: "Salesman 4",
                              value: "salesman-4",
                            },
                          ]}
                          labelBind="label"
                          valueBind="value"
                          placeholder="Select salesman"
                          searchPlaceholder="Search salesman"
                        />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Customer type</Label>
                        <DropdownInput
                          list={[
                            {
                              label: "Salesman 1",
                              value: "salesman-1",
                            },
                            {
                              label: "Salesman 2",
                              value: "salesman-2",
                            },
                            {
                              label: "Salesman 3",
                              value: "salesman-3",
                            },
                            {
                              label: "Salesman 4",
                              value: "salesman-4",
                            },
                          ]}
                          labelBind="label"
                          valueBind="value"
                          placeholder="Select salesman"
                          searchPlaceholder="Search salesman"
                        />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Payment terms</Label>
                        <DropdownInput
                          list={[
                            {
                              label: "Salesman 1",
                              value: "salesman-1",
                            },
                            {
                              label: "Salesman 2",
                              value: "salesman-2",
                            },
                            {
                              label: "Salesman 3",
                              value: "salesman-3",
                            },
                            {
                              label: "Salesman 4",
                              value: "salesman-4",
                            },
                          ]}
                          labelBind="label"
                          valueBind="value"
                          placeholder="Select salesman"
                          searchPlaceholder="Search salesman"
                        />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Customer group</Label>
                        <DropdownInput
                          list={[
                            {
                              label: "Salesman 1",
                              value: "salesman-1",
                            },
                            {
                              label: "Salesman 2",
                              value: "salesman-2",
                            },
                            {
                              label: "Salesman 3",
                              value: "salesman-3",
                            },
                            {
                              label: "Salesman 4",
                              value: "salesman-4",
                            },
                          ]}
                          labelBind="label"
                          valueBind="value"
                          placeholder="Select salesman"
                          searchPlaceholder="Search salesman"
                        />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Company</Label>
                        <MultiSelectDropdownInput
                          list={[
                            {
                              label: "Company 1",
                              value: "salesman-1",
                            },
                            {
                              label: "Company 2",
                              value: "salesman-2",
                            },
                            {
                              label: "Company 3",
                              value: "salesman-3",
                            },
                            {
                              label: "Company 4",
                              value: "salesman-4",
                            },
                            {
                              label: "Company 5",
                              value: "salesman-5",
                            },
                            {
                              label: "Company 6",
                              value: "salesman-6",
                            },
                          ]}
                          labelBind="label"
                          valueBind="value"
                          placeholder="Select Company"
                          searchPlaceholder="Search Company"
                        />
                      </div>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-2">
                <AccordionTrigger className="text-md">
                  Pricing & Tax
                </AccordionTrigger>
                <AccordionContent className="flex flex-col gap-4 text-balance">
                  <div className="grid gap-6 py-10 border-t pt-4 ">
                    <div className="grid gap-6 md:grid-cols-3 grid-cols-1">
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="email">Liquor license no</Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Tax id <span className="text-red-500">*</span>
                        </Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Tax appeal</Label>
                        <RadioGroup
                          defaultValue="no"
                          className="flex gap-2 pt-2"
                        >
                          <div className="flex items-center gap-3">
                            <RadioGroupItem value="yes" id="r1" />
                            <Label htmlFor="r1">Yes</Label>
                          </div>
                          <div className="flex items-center gap-3">
                            <RadioGroupItem value="no" id="r2" />
                            <Label htmlFor="r2">No</Label>
                          </div>
                        </RadioGroup>
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Pricing model name</Label>
                        <DropdownInput
                          list={[
                            {
                              label: "Salesman 1",
                              value: "salesman-1",
                            },
                            {
                              label: "Salesman 2",
                              value: "salesman-2",
                            },
                            {
                              label: "Salesman 3",
                              value: "salesman-3",
                            },
                            {
                              label: "Salesman 4",
                              value: "salesman-4",
                            },
                          ]}
                          labelBind="label"
                          valueBind="value"
                          placeholder="Select salesman"
                          searchPlaceholder="Search salesman"
                        />
                      </div>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-3">
                <AccordionTrigger className="text-md">
                  Shipping & Billing Address
                </AccordionTrigger>
                <AccordionContent className="flex flex-col gap-4 text-balance">
                  <div className="grid gap-6 py-10 border-t  ">
                    <div className="grid gap-6 md:grid-cols-3 grid-cols-1">
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="email">Address type</Label>
                        <RadioGroup
                          defaultValue="no"
                          className="flex gap-2 pt-2"
                        >
                          <div className="flex items-center gap-3">
                            <RadioGroupItem value="Shipping" id="r1" />
                            <Label htmlFor="r1">Shipping</Label>
                          </div>
                          <div className="flex items-center gap-3">
                            <RadioGroupItem value="Billing" id="r2" />
                            <Label htmlFor="r2">Billing</Label>
                          </div>
                        </RadioGroup>
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Street address <span className="text-red-500">*</span>
                        </Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          State
                          <span className="text-red-500">*</span>
                        </Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">City </Label>
                        <Input type="tel" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Zip code <span className="text-red-500">*</span>
                        </Label>
                        <Input type="email" />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-fax">Address title</Label>
                        <Input type="text" />
                      </div>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-4">
                <AccordionTrigger className="text-md">
                  Sec Information
                </AccordionTrigger>
                <AccordionContent className="flex flex-col gap-4 text-balance">
                  <div className="grid gap-6 pt-10 border-t  ">
                    <div className="grid gap-6 md:grid-cols-3 grid-cols-1">
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="email">Cigar license number</Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Federal license number{" "}
                          <span className="text-red-500">*</span>
                        </Label>
                        <Input type="text" required />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Federal expiry date
                          <span className="text-red-500">*</span>
                        </Label>
                        <DatePickerDemo />
                      </div>
                      <div className="flex flex-col gap-3">
                        <Label htmlFor="customer-name">
                          Credentials for customer portal{" "}
                          <span className="text-red-500">*</span>
                        </Label>
                        <Switch />
                      </div>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </CardContent>
        </Card>
        <div className="bg-inherit sticky z-[1] bottom-0 flex items-center justify-start gap-2 border-t px-4 pt-4 pb-2">
          <Button type="submit" className="w-[120px]">
            Submit
          </Button>
          <Button type="submit" variant={"outline"} className="w-[120px]">
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
};
