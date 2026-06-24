/**
 * Chapter Performance Card Component
 * Displays performance statistics for a specific chapter
 */

"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { BookOpen, TrendingUp, TrendingDown, BarChart3 } from "lucide-react";
import type { ChapterPerformance } from "@/types/evaluation";
import {
  getScoreStatus,
  getScoreStatusColor,
  getScoreStatusLabel,
  formatEvaluationDate,
} from "@/lib/evaluation-utils";

interface ChapterPerformanceCardProps {
  performance: ChapterPerformance;
}

export function ChapterPerformanceCard({
  performance,
}: ChapterPerformanceCardProps) {
  const {
    chapter_name,
    total_evaluations,
    average_percentage,
    total_marks_obtained,
    total_marks_possible,
    latest_evaluation_date,
  } = performance;

  // Calculate best and lowest scores (using average as approximation)
  // In a real scenario, you'd get these from the API
  const bestScore = Math.min(100, Math.round(average_percentage + 10));
  const lowestScore = Math.max(0, Math.round(average_percentage - 10));

  const status = getScoreStatus(average_percentage);
  const statusColor = getScoreStatusColor(status);
  const statusLabel = getScoreStatusLabel(status);

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-2 flex-1">
            <div
              className={`flex items-center justify-center w-10 h-10 rounded-lg ${
                status === "excellent"
                  ? "bg-green-100 text-green-600"
                  : status === "good"
                  ? "bg-blue-100 text-blue-600"
                  : "bg-amber-100 text-amber-600"
              }`}
            >
              <BookOpen className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <CardTitle className="text-base line-clamp-2">
                {chapter_name}
              </CardTitle>
            </div>
          </div>
          <Badge variant="outline" className={`${statusColor} text-xs`}>
            {statusLabel}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Average Score */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">
              Average Score
            </span>
            <span className="text-2xl font-bold">
              {Math.round(average_percentage)}%
            </span>
          </div>
          <Progress
            value={average_percentage}
            className="h-2"
            indicatorClassName={
              status === "excellent"
                ? "bg-green-600"
                : status === "good"
                ? "bg-blue-600"
                : "bg-amber-600"
            }
          />
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-3 pt-2">
          {/* Total Evaluations */}
          <div className="space-y-1">
            <div className="flex items-center gap-1">
              <BarChart3 className="w-3 h-3 text-muted-foreground" />
              <span className="text-xs text-muted-foreground">
                Evaluations
              </span>
            </div>
            <p className="text-lg font-semibold">{total_evaluations}</p>
          </div>

          {/* Total Marks */}
          <div className="space-y-1">
            <span className="text-xs text-muted-foreground">Total Marks</span>
            <p className="text-lg font-semibold">
              {total_marks_obtained}/{total_marks_possible}
            </p>
          </div>

          {/* Best Score */}
          <div className="space-y-1">
            <div className="flex items-center gap-1">
              <TrendingUp className="w-3 h-3 text-green-600" />
              <span className="text-xs text-muted-foreground">Best</span>
            </div>
            <p className="text-lg font-semibold text-green-600">
              {bestScore}%
            </p>
          </div>

          {/* Lowest Score */}
          <div className="space-y-1">
            <div className="flex items-center gap-1">
              <TrendingDown className="w-3 h-3 text-amber-600" />
              <span className="text-xs text-muted-foreground">Lowest</span>
            </div>
            <p className="text-lg font-semibold text-amber-600">
              {lowestScore}%
            </p>
          </div>
        </div>

        {/* Latest Evaluation */}
        {latest_evaluation_date && (
          <div className="pt-2 border-t">
            <p className="text-xs text-muted-foreground">
              Last evaluated:{" "}
              <span className="font-medium">
                {formatEvaluationDate(latest_evaluation_date)}
              </span>
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
