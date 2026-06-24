/**
 * Question Navigation Component
 * Navigation controls and question palette
 */

"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  ChevronLeft, 
  ChevronRight, 
  Save, 
  CheckCircle2,
  Circle,
  Loader2
} from "lucide-react";
import { cn } from "@/lib/utils";

interface QuestionNavigationProps {
  totalQuestions: number;
  currentQuestionIndex: number;
  answeredQuestions: Set<number>;
  onQuestionSelect: (index: number) => void;
  onPrevious: () => void;
  onNext: () => void;
  onSave: () => void;
  isSaving: boolean;
  canGoNext: boolean;
  canGoPrevious: boolean;
}

export function QuestionNavigation({
  totalQuestions,
  currentQuestionIndex,
  answeredQuestions,
  onQuestionSelect,
  onPrevious,
  onNext,
  onSave,
  isSaving,
  canGoNext,
  canGoPrevious,
}: QuestionNavigationProps) {
  const isCurrentAnswered = answeredQuestions.has(currentQuestionIndex);
  const answeredCount = answeredQuestions.size;
  const progressPercentage = (answeredCount / totalQuestions) * 100;

  return (
    <div className="space-y-4">
      {/* Progress Bar */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="font-medium">Progress</span>
              <span className="text-muted-foreground">
                {answeredCount} / {totalQuestions} completed
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-primary h-full transition-all duration-300"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>0%</span>
              <span className="font-semibold text-primary">
                {Math.round(progressPercentage)}%
              </span>
              <span>100%</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Navigation Buttons */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              onClick={onPrevious}
              disabled={!canGoPrevious}
              className="flex-1"
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              Previous
            </Button>
            <Button
              onClick={onSave}
              disabled={isSaving}
              className="flex-1"
              variant={isCurrentAnswered ? "secondary" : "default"}
            >
              {isSaving ? (
                <>
                  <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-1" />
                  Save Answer
                </>
              )}
            </Button>
            <Button
              onClick={onNext}
              disabled={!canGoNext}
              className="flex-1"
            >
              Next
              <ChevronRight className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Question Palette */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-sm">Question Palette</h3>
              <div className="flex items-center gap-3 text-xs">
                <div className="flex items-center gap-1">
                  <CheckCircle2 className="h-3 w-3 text-green-600" />
                  <span>Answered</span>
                </div>
                <div className="flex items-center gap-1">
                  <Circle className="h-3 w-3 text-gray-400" />
                  <span>Not Answered</span>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-5 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10 gap-2">
              {Array.from({ length: totalQuestions }, (_, i) => {
                const isAnswered = answeredQuestions.has(i);
                const isCurrent = i === currentQuestionIndex;

                return (
                  <Button
                    key={i}
                    variant={isCurrent ? "default" : "outline"}
                    size="sm"
                    onClick={() => onQuestionSelect(i)}
                    className={cn(
                      "w-full aspect-square p-0 relative",
                      isAnswered && !isCurrent && "border-green-500 bg-green-50 hover:bg-green-100",
                      isCurrent && isAnswered && "bg-green-600 hover:bg-green-700"
                    )}
                  >
                    <span className="font-medium">{i + 1}</span>
                    {isAnswered && !isCurrent && (
                      <CheckCircle2 className="h-3 w-3 absolute -top-1 -right-1 text-green-600 bg-white rounded-full" />
                    )}
                  </Button>
                );
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Legend */}
      <div className="flex items-center justify-center gap-4 text-xs text-muted-foreground">
        <div className="flex items-center gap-1">
          <Badge className="h-5 w-5 p-0 bg-primary" />
          <span>Current</span>
        </div>
        <div className="flex items-center gap-1">
          <Badge variant="outline" className="h-5 w-5 p-0 border-green-500" />
          <span>Answered</span>
        </div>
        <div className="flex items-center gap-1">
          <Badge variant="outline" className="h-5 w-5 p-0" />
          <span>Not Answered</span>
        </div>
      </div>
    </div>
  );
}
