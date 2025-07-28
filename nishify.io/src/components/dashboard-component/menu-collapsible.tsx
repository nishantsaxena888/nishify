import React from "react";
import { CollapsibleTrigger } from "../ui/collapsible";
import { SidebarMenuButton } from "../ui/sidebar";
import { ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

export const MenuCollapsible = ({
  title,
  children,
  defaultOpen,
}: {
  title: string;
  children: React.ReactNode;
  defaultOpen: boolean;
}) => {
  const [open, setOpen] = React.useState(defaultOpen);
  return (
    <CollapsibleTrigger asChild>
      <SidebarMenuButton tooltip={title} onClick={() => setOpen(!open)}>
        {children}
        <ChevronRight
          className={cn(
            "ml-auto transition-transform duration-200",
            open ? "rotate-90" : "rotate-0"
          )}
        />
      </SidebarMenuButton>
    </CollapsibleTrigger>
  );
};
