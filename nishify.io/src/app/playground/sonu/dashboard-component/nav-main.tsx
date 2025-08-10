"use client";

import { type LucideIcon } from "lucide-react";

import { Collapsible, CollapsibleContent } from "@/components/ui/collapsible";
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
} from "@/components/ui/sidebar";
import { MenuCollapsible } from "./menu-collapsible";
import { usePathname } from "next/navigation";
import Link from "next/link";

type NavItem = {
  title: string;
  url: string;
  icon?: LucideIcon;
  isActive?: boolean;
  items?: NavItem[];
};

export function NavMain({ items }: { items: NavItem[] }) {
  const pathName = usePathname();
  const activeMenu = (url: string) => {
    return pathName === url ? true : false;
  };

  const renderItems = (menuItems: NavItem[]) => {
    return menuItems.map((item) => {
      const hasChildren = item.items && item.items.length > 0;

      if (!hasChildren) {
        // ✅ Simple item (no dropdown)
        return (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton
              asChild
              tooltip={item.title}
              isActive={activeMenu(item.url)}
            >
              <Link href={item.url}>
                {item.icon && <item.icon />}
                <span>{item.title}</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        );
      }

      // ✅ Item with nested children → Collapsible
      return (
        <Collapsible
          key={item.title}
          asChild
          defaultOpen={item.isActive}
          className="group/collapsible"
        >
          <SidebarMenuItem>
            <MenuCollapsible
              title={item.title}
              defaultOpen={item.isActive || false}
            >
              {item.icon && <item.icon />}
              <span>{item.title}</span>
            </MenuCollapsible>

            <CollapsibleContent>
              <SidebarMenuSub className="!mr-0 !pr-[2px]">
                {renderItems(item?.items as NavItem[])}
              </SidebarMenuSub>
            </CollapsibleContent>
          </SidebarMenuItem>
        </Collapsible>
      );
    });
  };

  return (
    <SidebarGroup>
      <SidebarGroupLabel>Platform</SidebarGroupLabel>
      <SidebarMenu>{renderItems(items)}</SidebarMenu>
    </SidebarGroup>
  );
}
