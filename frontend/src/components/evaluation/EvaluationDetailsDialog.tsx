/**
 * Evaluation Details Dialog Component
 * Modal showing complete evaluation details
 */

"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  FileQuestion,
  User,
  Lightbulb,
  MessageSquare,
  CheckCircle2,
  AlertCircle,
  Calendar,
  Trophy,
} from "lucide-react";
import type { Evaluation } from "@/types/evaluation";
import {
  calculatePercentage,
  getScoreStatus,
  getScoreStatusColor,
  getScoreStatusLabel,
  formatEvaluationDate,
} from "@/lib/evaluation-utils";

interface EvaluationDetailsDialogProps {
  evaluation: Evaluation | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function EvaluationDetailsDialog({
  evaluation,
  open,
  onOpenChange,
}: EvaluationDetailsDialogProps) {
  if (!evaluation) return null;

  const percentage = calculatePercentage(
    evaluation.marks_awarded,
    evaluation.total_marks
  );
  const status = getScoreStatus(percentage);
  const statusColor = getScoreStatusColor(status);
  const statusLabel = getScoreStatusLabel(status);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] p-0">
        <DialogHeader className="p-6 pb-0">
          <div className="flex items-start justify-between">
            <DialogTitle className="text-2xl">Evaluation Details</DialogTitle>
            <Badge variant="outline" className={statusColor}>
              {statusLabel}
            </Badge>
          </div>
        </DialogHeader>

        <ScrollArea className="max-h-[calc(90vh-80px)] px-6 pb-6">
          <div className="space-y-6 pt-4">
            {/* Score Section */}
            <Card className="border-2">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between mb-4">
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
                      <p className="text-3xl font-bold">
                        {evaluation.marks_awarded} / {evaluation.total_marks}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-muted-foreground">Percentage</p>
                    <p className="text-3xl font-bold">{percentage}%</p>
                  </div>
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
              </CardContent>
            </Card>

            {/* Feedback */}
            {evaluation.feedback && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <MessageSquare className="w-5 h-5" />
                    Feedback
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed">
                    {evaluation.feedback}
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Strengths and Improvements */}
            <div className="grid gap-6 md:grid-cols-2">
              {/* Strengths */}
              {evaluation.strengths && evaluation.strengths.length > 0 && (
                <Card className="border-green-200 bg-green-50/50">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2 text-green-700">
                      <CheckCircle2 className="w-5 h-5" />
                      Strengths
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {evaluation.strengths.map((strength, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-gray-700">
                            {strength}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {/* Improvements */}
              {evaluation.improvements && evaluation.improvements.length > 0 && (
                <Card className="border-amber-200 bg-amber-50/50">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2 text-amber-700">
                      <AlertCircle className="w-5 h-5" />
                      Areas for Improvement
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {evaluation.improvements.map((improvement, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-gray-700">
                            {improvement}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Model Answer */}
            {evaluation.model_answer && (
              <Card className="border-blue-200 bg-blue-50/50">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2 text-blue-700">
                    <Lightbulb className="w-5 h-5" />
                    Model Answer
                  </CardTitle>
                  <p className="text-sm text-muted-foreground">
                    This is the ideal answer generated from textbook content
                  </p>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                    {evaluation.model_answer}
                  </p>
                </CardContent>
              </Card>
            )}

            <Separator />

            {/* Question */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <FileQuestion className="w-5 h-5" />
                  Question
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {evaluation.question}
                </p>
              </CardContent>
            </Card>

            {/* Student Answer */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <User className="w-5 h-5" />
                  Your Answer
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {evaluation.student_answer}
                </p>
              </CardContent>
            </Card>

            {/* Metadata */}
            <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
              {evaluation.chapter_name && (
                <div className="flex items-center gap-2">
                  <span className="font-medium">Chapter:</span>
                  <span>{evaluation.chapter_name}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span>{formatEvaluationDate(evaluation.created_at)}</span>
              </div>
            </div>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
