/**
 * Submit Confirmation Dialog Component
 * Comprehensive confirmation before test submission
 */

"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";
import {
  CheckCircle2,
  Circle,
  AlertTriangle,
  Send,
  Loader2,
  Clock,
  FileCheck,
} from "lucide-react";
import type { Test } from "@/types/examination";

interface SubmitConfirmationDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  test: Test | null;
  answeredQuestions: Set<number>;
  onConfirm: () => void;
  isSubmitting: boolean;
}

export function SubmitConfirmationDialog({
  open,
  onOpenChange,
  test,
  answeredQuestions,
  onConfirm,
  isSubmitting,
}: SubmitConfirmationDialogProps) {
  if (!test) return null;

  const totalQuestions = test.questions.length;
  const answeredCount = answeredQuestions.size;
  const unansweredCount = totalQuestions - answeredCount;
  const completionPercentage = (answeredCount / totalQuestions) * 100;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-xl">
            <FileCheck className="h-6 w-6 text-primary" />
            Submit Test for Evaluation?
          </DialogTitle>
          <DialogDescription className="text-base">
            Please review your submission details before proceeding. This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* Progress Overview */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="font-medium">Completion Status</span>
              <span className="text-muted-foreground">
                {answeredCount} / {totalQuestions} questions
              </span>
            </div>
            <Progress value={completionPercentage} className="h-2" />
            <div className="text-center">
              <span className="text-2xl font-bold text-primary">
                {Math.round(completionPercentage)}%
              </span>
              <span className="text-sm text-muted-foreground ml-2">Complete</span>
            </div>
          </div>

          {/* Statistics Grid */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center gap-2 mb-1">
                <CheckCircle2 className="h-4 w-4 text-green-600" />
                <span className="text-xs font-medium text-green-700">Answered</span>
              </div>
              <p className="text-xl font-bold text-green-900">{answeredCount}</p>
            </div>

            <div className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
              <div className="flex items-center gap-2 mb-1">
                <Circle className="h-4 w-4 text-orange-600" />
                <span className="text-xs font-medium text-orange-700">Unanswered</span>
              </div>
              <p className="text-xl font-bold text-orange-900">{unansweredCount}</p>
            </div>
          </div>

          {/* Warning for Unanswered Questions */}
          {unansweredCount > 0 && (
            <Alert variant="destructive" className="bg-orange-50 border-orange-200">
              <AlertTriangle className="h-4 w-4 text-orange-600" />
              <AlertDescription className="text-orange-900">
                <strong>Warning:</strong> You have {unansweredCount} unanswered question
                {unansweredCount !== 1 && "s"}. These will be marked as incorrect during
                evaluation. Consider reviewing them before submitting.
              </AlertDescription>
            </Alert>
          )}

          {/* Test Information */}
          <div className="space-y-2 p-3 bg-gray-50 rounded-lg text-sm">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Test Type:</span>
              <Badge variant="secondary">
                {test.question_type.replace("_", " ")}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Categories:</span>
              <span className="font-medium text-right">
                {test.selected_categories.join(", ")}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Total Questions:</span>
              <span className="font-medium">{totalQuestions}</span>
            </div>
          </div>

          {/* Important Notice */}
          <Alert>
            <Clock className="h-4 w-4" />
            <AlertDescription>
              <strong>Important:</strong> After submission, you will not be able to modify
              your answers. Your test will be queued for AI-powered evaluation.
            </AlertDescription>
          </Alert>
        </div>

        <DialogFooter className="flex-col sm:flex-row gap-2">
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isSubmitting}
            className="w-full sm:w-auto"
          >
            Cancel
          </Button>
          <Button
            onClick={onConfirm}
            disabled={isSubmitting}
            className="w-full sm:w-auto bg-primary hover:bg-primary/90"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Submitting...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                Submit Test
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
