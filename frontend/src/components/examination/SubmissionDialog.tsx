"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { AlertTriangle, Loader2 } from "lucide-react";

interface SubmissionDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm: () => Promise<void>;
  answeredCount: number;
  totalCount: number;
}

export function SubmissionDialog({
  open,
  onOpenChange,
  onConfirm,
  answeredCount,
  totalCount,
}: SubmissionDialogProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const unanswered = totalCount - answeredCount;

  const handleConfirm = async () => {
    setIsSubmitting(true);
    try {
      await onConfirm();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(v) => !isSubmitting && onOpenChange(v)}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="flex items-center gap-3 mb-1">
            <div className="bg-amber-100 p-2 rounded-full">
              <AlertTriangle className="h-5 w-5 text-amber-600" />
            </div>
            <DialogTitle className="text-lg">Submit Test?</DialogTitle>
          </div>
          <DialogDescription className="text-sm text-gray-600 leading-relaxed">
            Are you sure you want to submit your test? You{" "}
            <strong>cannot modify answers</strong> after submission.
          </DialogDescription>
        </DialogHeader>

        {/* Answer summary */}
        <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
          <div className="flex justify-between text-gray-700">
            <span>Questions answered:</span>
            <span className="font-semibold text-emerald-600">
              {answeredCount} / {totalCount}
            </span>
          </div>
          {unanswered > 0 && (
            <div className="flex justify-between text-gray-700">
              <span>Unanswered:</span>
              <span className="font-semibold text-amber-600">
                {unanswered}
              </span>
            </div>
          )}
        </div>

        {unanswered > 0 && (
          <p className="text-xs text-amber-600 flex items-center gap-1.5">
            <AlertTriangle className="h-3 w-3 flex-shrink-0" />
            You have {unanswered} unanswered question{unanswered > 1 ? "s" : ""}. They will be left blank.
          </p>
        )}

        <DialogFooter className="gap-2">
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isSubmitting}
            className="flex-1 sm:flex-none"
          >
            Cancel
          </Button>
          <Button
            onClick={handleConfirm}
            disabled={isSubmitting}
            className="flex-1 sm:flex-none bg-blue-600 hover:bg-blue-700 text-white"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Submitting…
              </>
            ) : (
              "Submit Test"
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
