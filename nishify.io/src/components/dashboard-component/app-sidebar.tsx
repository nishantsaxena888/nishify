"use client";

import * as React from "react";
import {
  AudioWaveform,
  BadgePercent,
  ChartLine,
  Command,
  Component,
  Frame,
  GalleryVerticalEnd,
  Group,
  Map,
  MonitorCog,
  PieChart,
  Settings,
  Settings2,
  ShoppingCart,
  Users,
} from "lucide-react";

import { NavMain } from "@/components/dashboard-component/nav-main";
import { NavUser } from "@/components/dashboard-component/nav-user";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";
import { TeamSwitcher } from "./team-switcher";
import { NavProjects } from "./nav-projects";

// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "Pioneer Wholesale Inc",
      logo: GalleryVerticalEnd,
      plan: "",
    },
    // {
    //   name: "Acme Corp.",
    //   logo: AudioWaveform,
    //   plan: "Startup",
    // },
    // {
    //   name: "Evil Corp.",
    //   logo: Command,
    //   plan: "Free",
    // },
  ],
  navMain: [
    {
      title: "Customer Special Pricing",
      url: "/playground",
      icon: BadgePercent,
      isActive: true,
      items: [],
    },
    {
      title: "Generic Groups",
      url: "#",
      icon: Group,
      isActive: true,
      items: [],
    },
    {
      title: "Access Control",
      url: "#",
      icon: Settings,
      isActive: true,
      items: [],
    },
    {
      title: "Generic Users",
      url: "#",
      icon: Users,
      isActive: true,
      items: [],
    },
    {
      title: "Configurations",
      url: "#",
      icon: MonitorCog,
      isActive: false,
      items: [],
    },
    {
      title: "Purchase",
      url: "#",
      icon: ShoppingCart,
      isActive: false,
      items: [
        {
          title: "Search Inventory",
          url: "#",
        },
        {
          title: "Add Inventory",
          url: "#",
        },

        {
          title: "Purchase",
          url: "#",
          items: [
            {
              title: "Purchase History",
              url: "#",
            },
            {
              title: "Create Purchase Order",
              url: "#",
            },
          ],
        },
        {
          title: "Receiving Inventory",
          url: "#",
          items: [
            {
              title: "Good Inwards",
              url: "#",
            },
            {
              title: "Create Good Inwards",
              url: "#",
            },
          ],
        },
      ],
    },
    {
      title: "Sales Invoice",
      url: "#",
      icon: ChartLine,
      isActive: false,
      items: [
        {
          title: "Invoice List",
          url: "#",
        },
        {
          title: "Create Invoice",
          url: "#",
        },
      ],
    },
    {
      title: "Master",
      url: "#",
      icon: Component,
      isActive: false,
      items: [
        {
          title: "Item",
          url: "#",
          items: [
            {
              title: "Search Item",
              url: "#",
            },
            {
              title: "Add Item",
              url: "#",
            },
            {
              title: "Brand",
              url: "#",
            },
            {
              title: "Item Category",
              url: "#",
            },
            {
              title: "Item Sub Category",
              url: "#",
            },
          ],
        },
        {
          title: "Customer",
          url: "#",
          items: [
            {
              title: "Search Customer",
              url: "#",
            },
            {
              title: "Add Customer",
              url: "#",
            },
            {
              title: "Customer Group",
              url: "#",
            },
            {
              title: "Customer Type",
              url: "#",
            },
          ],
        },
        {
          title: "Vendor",
          url: "#",
          items: [
            {
              title: "Search Vendor",
              url: "#",
            },
            {
              title: "Add Vendor",
              url: "#",
            },
          ],
        },
        {
          title: "Tax",
          url: "#",
          items: [],
        },
      ],
    },
    {
      title: "Settings",
      url: "#",
      icon: Settings2,
      isActive: false,
      items: [
        {
          title: "Department",
          url: "#",
        },
        {
          title: "System",
          url: "#",
        },
        {
          title: "Product Promotion",
          url: "#",
        },
        {
          title: "Payment Terms",
          url: "#",
        },
        {
          title: "State",
          url: "#",
        },
        {
          title: "Pricing Model",
          url: "#",
        },
        {
          title: "Salesman",
          url: "#",
        },
        {
          title: "Company",
          url: "#",
        },
      ],
    },
  ],
  projects: [
    {
      name: "List",
      url: "/dashboard/table",
      icon: Frame,
    },
    {
      name: "Forms",
      url: "/dashboard/forms",
      icon: PieChart,
    },
    {
      name: "Travel",
      url: "/dashboard/component",
      icon: Map,
    },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavProjects projects={data.projects} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
