"use client";

import { Skeleton } from "@/components/ui/skeleton";

export function HistorySkeletonLoader() {
  return (
    <div className="space-y-3">
      {/* Filter bar skeleton */}
      <div className="flex gap-3 mb-6 flex-wrap">
        <Skeleton className="h-10 w-40" />
        <Skeleton className="h-10 w-40" />
        <Skeleton className="h-10 w-56" />
      </div>
      {/* Table rows */}
      {Array.from({ length: 5 }, (_, i) => (
        <div
          key={i}
          className="flex items-center gap-4 bg-white rounded-xl border px-5 py-4"
        >
          <Skeleton className="h-10 w-10 rounded-lg flex-shrink-0" />
          <div className="flex-1 space-y-2">
            <Skeleton className="h-4 w-40" />
            <Skeleton className="h-3 w-56" />
          </div>
          <Skeleton className="h-6 w-24 rounded-full" />
          <Skeleton className="h-3 w-20" />
          <Skeleton className="h-9 w-24 rounded-lg" />
        </div>
      ))}
    </div>
  );
}
