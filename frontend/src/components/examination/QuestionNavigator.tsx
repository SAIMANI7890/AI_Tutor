"use client";

import { cn } from "@/lib/utils";

interface QuestionNavigatorProps {
  total: number;
  currentIndex: number; // 0-based
  answers: Record<string, string>;
  questionIds: string[];
  onJump: (index: number) => void;
}

export function QuestionNavigator({
  total,
  currentIndex,
  answers,
  questionIds,
  onJump,
}: QuestionNavigatorProps) {
  return (
    <div className="p-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Question Navigator</h3>
      <div className="grid grid-cols-5 gap-2">
        {Array.from({ length: total }, (_, i) => {
          const qId = questionIds[i];
          const isAnswered = qId ? !!answers[qId] : false;
          const isCurrent = i === currentIndex;

          return (
            <button
              key={i}
              onClick={() => onJump(i)}
              aria-label={`Go to question ${i + 1}${isAnswered ? " (answered)" : ""}${isCurrent ? " (current)" : ""}`}
              aria-current={isCurrent ? "true" : undefined}
              className={cn(
                "h-9 w-9 rounded-lg text-sm font-semibold transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1",
                isCurrent && "bg-blue-600 text-white shadow-md scale-110",
                !isCurrent && isAnswered && "bg-emerald-500 text-white hover:bg-emerald-600",
                !isCurrent && !isAnswered && "bg-gray-100 text-gray-500 hover:bg-gray-200"
              )}
            >
              {i + 1}
            </button>
          );
        })}
      </div>

      {/* Legend */}
      <div className="mt-4 flex flex-col gap-1.5 text-xs text-gray-500">
        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded bg-emerald-500 inline-block" />
          <span>Answered</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded bg-blue-600 inline-block" />
          <span>Current</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded bg-gray-100 border border-gray-300 inline-block" />
          <span>Not answered</span>
        </div>
      </div>
    </div>
  );
}
