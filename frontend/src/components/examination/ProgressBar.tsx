"use client";

import { Progress } from "@/components/ui/progress";

interface ProgressBarProps {
  current: number; // 1-based current question index
  total: number;
}

export function ProgressBar({ current, total }: ProgressBarProps) {
  const percentage = total > 0 ? Math.round((current / total) * 100) : 0;

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-600 font-medium">
          Question <span className="text-primary font-bold">{current}</span> of {total}
        </span>
        <span className="text-gray-500 text-xs">{percentage}% Complete</span>
      </div>
      <Progress value={percentage} className="h-2" />
    </div>
  );
}
