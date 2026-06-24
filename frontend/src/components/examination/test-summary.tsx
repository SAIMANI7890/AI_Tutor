/**
 * Test Summary Component
 * Displays test completion summary before final submission
 */

"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  CheckCircle2, 
  Circle, 
  Send,
  AlertTriangle,
  Loader2
} from "lucide-react";
import type { Test } from "@/types/examination";

interface TestSummaryProps {
  test: Test;
  answeredQuestions: Set<number>;
  onSubmit: () => void;
  onReview: (questionIndex: number) => void;
  isSubmitting: boolean;
}

export function TestSummary({
  test,
  answeredQuestions,
  onSubmit,
  onReview,
  isSubmitting,
}: TestSummaryProps) {
  const totalQuestions = test.questions.length;
  const answeredCount = answeredQuestions.size;
  const unansweredCount = totalQuestions - answeredCount;
  const completionPercentage = (answeredCount / totalQuestions) * 100;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Test Summary</CardTitle>
        <CardDescription>
          Review your answers before final submission
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Progress Overview */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium">Overall Progress</span>
            <span className="text-muted-foreground">
              {answeredCount} / {totalQuestions} answered
            </span>
          </div>
          <Progress value={completionPercentage} className="h-3" />
          <div className="flex items-center justify-center">
            <span className="text-2xl font-bold text-primary">
              {Math.round(completionPercentage)}% Complete
            </span>
          </div>
        </div>

        {/* Statistics Grid */}
        <div className="grid grid-cols-2 gap-4">
          <Card className="bg-green-50 border-green-200">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="h-8 w-8 text-green-600" />
                <div>
                  <p className="text-2xl font-bold text-green-900">{answeredCount}</p>
                  <p className="text-sm text-green-700">Answered</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-orange-50 border-orange-200">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <Circle className="h-8 w-8 text-orange-600" />
                <div>
                  <p className="text-2xl font-bold text-orange-900">{unansweredCount}</p>
                  <p className="text-sm text-orange-700">Unanswered</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Unanswered Questions Warning */}
        {unansweredCount > 0 && (
          <Card className="bg-orange-50 border-orange-200">
            <CardContent className="pt-4">
              <div className="flex items-start gap-3">
                <AlertTriangle className="h-5 w-5 text-orange-600 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-orange-900 mb-2">
                    You have {unansweredCount} unanswered question{unansweredCount !== 1 && 's'}
                  </p>
                  <p className="text-sm text-orange-700 mb-3">
                    Consider reviewing these questions before submitting:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {test.questions.map((q, index) => {
                      if (!answeredQuestions.has(index)) {
                        return (
                          <Button
                            key={index}
                            variant="outline"
                            size="sm"
                            onClick={() => onReview(index)}
                            className="border-orange-300 hover:bg-orange-100"
                          >
                            Question {index + 1}
                          </Button>
                        );
                      }
                      return null;
                    })}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Question Status List */}
        <div className="space-y-3">
          <h3 className="font-semibold text-sm">Question Status</h3>
          <div className="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2">
            {test.questions.map((q, index) => {
              const isAnswered = answeredQuestions.has(index);
              return (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  onClick={() => onReview(index)}
                  className={`
                    aspect-square p-0 relative
                    ${isAnswered ? "border-green-500 bg-green-50 hover:bg-green-100" : "border-orange-300 bg-orange-50"}
                  `}
                >
                  <span className="font-medium">{index + 1}</span>
                  {isAnswered && (
                    <CheckCircle2 className="h-3 w-3 absolute -top-1 -right-1 text-green-600 bg-white rounded-full" />
                  )}
                </Button>
              );
            })}
          </div>
        </div>

        {/* Test Information */}
        <div className="space-y-2 p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Question Type:</span>
            <Badge variant="secondary">{test.question_type.replace("_", " ")}</Badge>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Categories:</span>
            <span className="font-medium">{test.selected_categories.join(", ")}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Total Questions:</span>
            <span className="font-medium">{totalQuestions}</span>
          </div>
        </div>

        {/* Submit Button */}
        <div className="space-y-3">
          {unansweredCount > 0 && (
            <p className="text-sm text-center text-muted-foreground">
              You can submit with unanswered questions, but consider reviewing them first
            </p>
          )}
          <Button
            onClick={onSubmit}
            disabled={isSubmitting}
            size="lg"
            className="w-full"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Submitting Test...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                Submit Test
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
