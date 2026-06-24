"use client";

import { Check, Loader2, AlertCircle } from "lucide-react";
import type { SaveStatus } from "@/hooks/useExam";
import { cn } from "@/lib/utils";

interface SaveIndicatorProps {
  status: SaveStatus;
}

export function SaveIndicator({ status }: SaveIndicatorProps) {
  if (status === "idle") return null;

  return (
    <div
      className={cn(
        "flex items-center gap-1.5 text-xs font-medium transition-all duration-300",
        status === "saving" && "text-blue-500",
        status === "saved" && "text-emerald-600",
        status === "error" && "text-red-500"
      )}
      role="status"
      aria-live="polite"
    >
      {status === "saving" && (
        <>
          <Loader2 className="h-3 w-3 animate-spin" />
          <span>Saving…</span>
        </>
      )}
      {status === "saved" && (
        <>
          <Check className="h-3 w-3" />
          <span>Saved</span>
        </>
      )}
      {status === "error" && (
        <>
          <AlertCircle className="h-3 w-3" />
          <span>Failed to save</span>
        </>
      )}
    </div>
  );
}
