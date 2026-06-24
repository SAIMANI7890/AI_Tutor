/**
 * Evaluation Loading Skeleton
 * Loading state with progress messages
 */

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Loader2 } from "lucide-react";
import { useEffect, useState } from "react";

const LOADING_MESSAGES = [
  "Analyzing your answer...",
  "Retrieving textbook content...",
  "Generating model answer...",
  "Evaluating correctness...",
  "Preparing feedback...",
];

export function EvaluationLoadingSkeleton() {
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Loading Message */}
      <Card className="border-blue-200 bg-blue-50/50">
        <CardContent className="pt-6">
          <div className="flex items-center justify-center gap-3 py-8">
            <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
            <p className="text-lg font-medium text-blue-700 animate-pulse">
              {LOADING_MESSAGES[messageIndex]}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Score Skeleton */}
      <Card>
        <CardHeader className="space-y-4">
          <Skeleton className="h-8 w-48" />
          <Skeleton className="h-24 w-full" />
        </CardHeader>
      </Card>

      {/* Feedback Skeleton */}
      <Card>
        <CardHeader className="space-y-3">
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-20 w-full" />
        </CardHeader>
      </Card>

      {/* Two Column Skeletons */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader className="space-y-3">
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-16 w-full" />
            <Skeleton className="h-16 w-full" />
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="space-y-3">
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-16 w-full" />
            <Skeleton className="h-16 w-full" />
          </CardHeader>
        </Card>
      </div>

      {/* Model Answer Skeleton */}
      <Card>
        <CardHeader className="space-y-3">
          <Skeleton className="h-6 w-40" />
          <Skeleton className="h-32 w-full" />
        </CardHeader>
      </Card>
    </div>
  );
}
