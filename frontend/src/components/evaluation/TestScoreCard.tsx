/**
 * TestScoreCard – Overall score display
 */
"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Trophy, Target, Star } from "lucide-react";
import type { PerformanceLevel } from "@/types/evaluation";

interface TestScoreCardProps {
  totalAwarded: number;
  totalPossible: number;
  percentage: number;
  performanceLevel: PerformanceLevel;
  questionCount: number;
}

const levelConfig: Record<
  PerformanceLevel,
  { bg: string; border: string; badge: string; text: string; icon: string; indicator: string }
> = {
  Excellent: {
    bg: "bg-gradient-to-br from-emerald-50 to-green-50",
    border: "border-emerald-200",
    badge: "bg-emerald-100 text-emerald-800 border-emerald-300",
    text: "text-emerald-700",
    icon: "🏆",
    indicator: "bg-emerald-500",
  },
  Good: {
    bg: "bg-gradient-to-br from-blue-50 to-indigo-50",
    border: "border-blue-200",
    badge: "bg-blue-100 text-blue-800 border-blue-300",
    text: "text-blue-700",
    icon: "⭐",
    indicator: "bg-blue-500",
  },
  Average: {
    bg: "bg-gradient-to-br from-amber-50 to-yellow-50",
    border: "border-amber-200",
    badge: "bg-amber-100 text-amber-800 border-amber-300",
    text: "text-amber-700",
    icon: "📊",
    indicator: "bg-amber-500",
  },
  "Needs Improvement": {
    bg: "bg-gradient-to-br from-red-50 to-orange-50",
    border: "border-red-200",
    badge: "bg-red-100 text-red-800 border-red-300",
    text: "text-red-700",
    icon: "📚",
    indicator: "bg-red-500",
  },
};

export function TestScoreCard({
  totalAwarded,
  totalPossible,
  percentage,
  performanceLevel,
  questionCount,
}: TestScoreCardProps) {
  const cfg = levelConfig[performanceLevel] ?? levelConfig["Average"];

  return (
    <Card className={`${cfg.bg} ${cfg.border} border-2 shadow-md`}>
      <CardContent className="pt-6 pb-6">
        <div className="flex flex-col md:flex-row items-center gap-6">
          {/* Score circle */}
          <div className="flex flex-col items-center gap-1">
            <div className="text-5xl mb-1">{cfg.icon}</div>
            <div className="text-center">
              <p className={`text-4xl font-extrabold ${cfg.text}`}>
                {totalAwarded}
                <span className="text-2xl font-medium text-gray-500">
                  /{totalPossible}
                </span>
              </p>
              <p className="text-sm text-gray-500 mt-0.5">Total Score</p>
            </div>
          </div>

          {/* Divider */}
          <div className="hidden md:block w-px h-20 bg-gray-200" />
          <div className="md:hidden w-full h-px bg-gray-200" />

          {/* Percentage + level */}
          <div className="flex-1 w-full">
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl font-bold text-gray-800">
                {percentage}%
              </span>
              <Badge className={`${cfg.badge} border font-semibold px-3 py-1 text-sm`}>
                {performanceLevel}
              </Badge>
            </div>

            <Progress value={percentage} className="h-3 bg-gray-200 rounded-full" indicatorClassName={cfg.indicator} />

            <div className="flex justify-between mt-2 text-xs text-gray-500">
              <span className="flex items-center gap-1">
                <Target className="h-3 w-3" />
                {questionCount} questions evaluated
              </span>
              <span className="flex items-center gap-1">
                <Star className="h-3 w-3" />
                {totalPossible > 0 ? `${totalPossible / questionCount}/question` : "—"}
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
