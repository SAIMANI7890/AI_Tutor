/**
 * Social Studies Navigation Component
 * Navigation menu for Social Studies features
 */

"use client";

import { usePathname, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { MessageSquare, Calendar, FileCheck, Home, ClipboardCheck } from "lucide-react";
import { cn } from "@/lib/utils";

export function SocialNav() {
  const pathname = usePathname();
  const router = useRouter();

  const navItems = [
    {
      name: "Dashboard",
      href: "/dashboard",
      icon: Home,
    },
    {
      name: "AI Tutor Chat",
      href: "/dashboard/social/chat",
      icon: MessageSquare,
    },
    {
      name: "Study Planner",
      href: "/dashboard/social/study-plan",
      icon: Calendar,
    },
    {
      name: "Examinations",
      href: "/dashboard/social/examination",
      icon: FileCheck,
    },
    {
      name: "Evaluation",
      href: "/dashboard/social/evaluation",
      icon: ClipboardCheck,
    },
  ];

  return (
    <nav className="bg-white border-b shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center gap-2 overflow-x-auto py-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");

            return (
              <Button
                key={item.href}
                variant={isActive ? "default" : "ghost"}
                size="sm"
                onClick={() => router.push(item.href)}
                className={cn(
                  "flex items-center gap-2 whitespace-nowrap",
                  isActive && "shadow-sm"
                )}
              >
                <Icon className="h-4 w-4" />
                <span className="hidden sm:inline">{item.name}</span>
              </Button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
