/**
 * Submitted Test Card Component
 * Shows a submitted test with long answer questions that can be evaluated
 */

"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  FileCheck, 
  Calendar, 
  CheckCircle2, 
  Clock,
  BookOpen 
} from "lucide-react";
import type { SubmittedTestForEvaluation } from "@/types/evaluation";
import { formatEvaluationDate } from "@/lib/evaluation-utils";

interface SubmittedTestCardProps {
  test: SubmittedTestForEvaluation;
  onEvaluate: (testId: string, questionId: string, questionSummary: string, studentAnswer: string) => void;
  isEvaluating?: string | null;
}

export function SubmittedTestCard({
  test,
  onEvaluate,
  isEvaluating,
}: SubmittedTestCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-3 flex-1">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-blue-100 text-blue-600 flex-shrink-0">
              <FileCheck className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <CardTitle className="text-lg">{test.test_name}</CardTitle>
              <div className="flex flex-wrap items-center gap-3 mt-2 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <BookOpen className="w-4 h-4" />
                  <span>{test.category}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  <span>{formatEvaluationDate(test.created_at)}</span>
                </div>
                <Badge variant="outline" className="text-green-600 bg-green-50 border-green-200">
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  Submitted
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <Separator />

        {/* Long Answer Questions */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm flex items-center gap-2">
            <Clock className="w-4 h-4" />
            Long Answer Questions ({test.long_answers.length})
          </h4>

          <div className="space-y-3">
            {test.long_answers.map((longAnswer) => {
              const isAlreadyEvaluated = longAnswer.evaluation_id !== null;
              const isCurrentlyEvaluating = isEvaluating === `${test.test_id}-${longAnswer.question_id}`;

              return (
                <Card key={longAnswer.question_id} className="bg-muted/30">
                  <CardContent className="pt-4">
                    <div className="space-y-3">
                      {/* Question */}
                      <div>
                        <p className="text-sm font-medium text-muted-foreground mb-1">
                          Question {longAnswer.question_number}
                        </p>
                        <p className="text-sm">{longAnswer.question_summary}</p>
                      </div>

                      {/* Student Answer Preview */}
                      <div>
                        <p className="text-xs text-muted-foreground mb-1">Your Answer:</p>
                        <p className="text-sm text-gray-700 line-clamp-2">
                          {longAnswer.student_answer}
                        </p>
                      </div>

                      {/* Action */}
                      <div className="flex items-center justify-between pt-2">
                        {isAlreadyEvaluated ? (
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className="text-green-600 bg-green-50 border-green-200">
                              <CheckCircle2 className="w-3 h-3 mr-1" />
                              Evaluated
                            </Badge>
                            {longAnswer.marks_awarded !== undefined && (
                              <span className="text-sm font-semibold">
                                {longAnswer.marks_awarded}/10
                              </span>
                            )}
                          </div>
                        ) : (
                          <Button
                            size="sm"
                            onClick={() =>
                              onEvaluate(
                                test.test_id,
                                longAnswer.question_id,
                                longAnswer.question_summary,
                                longAnswer.student_answer
                              )
                            }
                            disabled={isCurrentlyEvaluating}
                          >
                            {isCurrentlyEvaluating ? "Evaluating..." : "Evaluate"}
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
