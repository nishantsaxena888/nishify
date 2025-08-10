/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

export function MultiSelectDropdownInput({
  list,
  labelBind,
  valueBind,
  placeholder,
  searchPlaceholder,
}: {
  list: any[];
  labelBind: string;
  valueBind: string;
  placeholder: string;
  searchPlaceholder?: string;
}) {
  const [open, setOpen] = React.useState(false);
  const [selectedValues, setSelectedValues] = React.useState<string[]>([]);

  const toggleValue = (val: string) => {
    setSelectedValues((prev) =>
      prev.includes(val) ? prev.filter((v) => v !== val) : [...prev, val]
    );
  };

  const selectedLabels = list
    .filter((item) => selectedValues.includes(item[valueBind]))
    .map((item) => item[labelBind])
    .join(", ");

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between "
        >
          {selectedValues.length > 0 ? (
            <span className="line-clamp-1">{selectedLabels}</span>
          ) : (
            placeholder
          )}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0" align="start">
        <Command>
          <CommandInput
            placeholder={searchPlaceholder || "Search"}
            className="h-9"
          />
          <CommandList>
            <CommandEmpty>No item found.</CommandEmpty>
            <CommandGroup>
              {list.map((item: any) => {
                const val = item[valueBind];
                const isSelected = selectedValues.includes(val);

                return (
                  <CommandItem
                    key={val}
                    value={val}
                    onSelect={() => toggleValue(val)}
                  >
                    {item[labelBind]}
                    <Check
                      className={cn(
                        "ml-auto",
                        isSelected ? "opacity-100" : "opacity-0"
                      )}
                    />
                  </CommandItem>
                );
              })}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
