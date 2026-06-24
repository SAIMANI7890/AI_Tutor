"use client";

import { Skeleton } from "@/components/ui/skeleton";

export function ExamSkeletonLoader() {
  return (
    <div className="flex flex-col h-screen">
      {/* Header skeleton */}
      <div className="border-b bg-white px-4 py-4 space-y-3">
        <div className="flex items-center justify-between">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-20" />
        </div>
        <Skeleton className="h-2 w-full rounded-full" />
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Navigator skeleton */}
        <div className="w-56 border-r bg-white p-4 hidden lg:block space-y-3">
          <Skeleton className="h-4 w-32" />
          <div className="grid grid-cols-5 gap-2">
            {Array.from({ length: 10 }, (_, i) => (
              <Skeleton key={i} className="h-9 w-9 rounded-lg" />
            ))}
          </div>
        </div>

        {/* Question area skeleton */}
        <div className="flex-1 p-6 space-y-6">
          <div className="space-y-2">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-6 w-full" />
            <Skeleton className="h-6 w-3/4" />
          </div>
          <div className="space-y-3">
            {Array.from({ length: 4 }, (_, i) => (
              <Skeleton key={i} className="h-14 w-full rounded-xl" />
            ))}
          </div>
        </div>
      </div>

      {/* Footer skeleton */}
      <div className="border-t bg-white px-6 py-4 flex justify-between items-center">
        <Skeleton className="h-10 w-28" />
        <Skeleton className="h-10 w-36" />
        <Skeleton className="h-10 w-28" />
      </div>
    </div>
  );
}
