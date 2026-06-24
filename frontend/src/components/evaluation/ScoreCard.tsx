/**
 * Score Card Component
 * Displays evaluation score with visual progress indicator
 */

import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Trophy, TrendingUp } from "lucide-react";
import {
  calculatePercentage,
  getScoreStatus,
  getScoreStatusColor,
  getScoreStatusLabel,
} from "@/lib/evaluation-utils";

interface ScoreCardProps {
  marksAwarded: number;
  totalMarks: number;
  showBadge?: boolean;
  size?: "sm" | "md" | "lg";
}

export function ScoreCard({
  marksAwarded,
  totalMarks,
  showBadge = true,
  size = "md",
}: ScoreCardProps) {
  const percentage = calculatePercentage(marksAwarded, totalMarks);
  const status = getScoreStatus(percentage);
  const statusColor = getScoreStatusColor(status);
  const statusLabel = getScoreStatusLabel(status);

  const sizeClasses = {
    sm: "text-2xl",
    md: "text-4xl",
    lg: "text-6xl",
  };

  return (
    <Card className="border-2">
      <CardContent className="pt-6">
        <div className="space-y-4">
          {/* Score Display */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div
                className={`flex items-center justify-center w-12 h-12 rounded-full ${
                  status === "excellent"
                    ? "bg-green-100 text-green-600"
                    : status === "good"
                    ? "bg-blue-100 text-blue-600"
                    : "bg-amber-100 text-amber-600"
                }`}
              >
                <Trophy className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Your Score</p>
                <p className={`font-bold ${sizeClasses[size]}`}>
                  {marksAwarded} / {totalMarks}
                </p>
              </div>
            </div>
            {showBadge && (
              <Badge
                variant="outline"
                className={`${statusColor} border px-3 py-1 text-sm font-semibold`}
              >
                <TrendingUp className="w-4 h-4 mr-1" />
                {statusLabel}
              </Badge>
            )}
          </div>

          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Progress</span>
              <span className="font-semibold">{percentage}%</span>
            </div>
            <Progress
              value={percentage}
              className="h-3"
              indicatorClassName={
                status === "excellent"
                  ? "bg-green-600"
                  : status === "good"
                  ? "bg-blue-600"
                  : "bg-amber-600"
              }
            />
          </div>

          {/* Performance Message */}
          <p className="text-sm text-center text-muted-foreground">
            {status === "excellent" &&
              "Outstanding performance! Keep up the excellent work!"}
            {status === "good" &&
              "Good job! You're on the right track. Keep practicing!"}
            {status === "needs-improvement" &&
              "Keep trying! Review the feedback and practice more."}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
