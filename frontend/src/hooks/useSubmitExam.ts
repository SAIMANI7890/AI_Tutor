"use client";

import { useCallback, useState } from "react";
import { examService, type SubmitResult } from "@/lib/services/exam.service";

export type SubmitState = "idle" | "submitting" | "success" | "error";

/**
 * Handles the submit exam flow:
 *  - Calls examService.submit(testId)
 *  - Tracks loading / success / error state
 *  - Returns the submission result for post-submit display
 */
export function useSubmitExam(testId: string) {
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitResult, setSubmitResult] = useState<SubmitResult | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const submit = useCallback(async () => {
    setSubmitState("submitting");
    setSubmitError(null);
    try {
      const res = await examService.submit(testId);
      if (res.success && res.data) {
        setSubmitResult(res.data);
        setSubmitState("success");
      } else {
        throw new Error(res.message || "Submission failed");
      }
    } catch (e: any) {
      const msg =
        e?.response?.data?.detail ||
        e?.message ||
        "Something went wrong. Please try again.";
      setSubmitError(msg);
      setSubmitState("error");
      throw e; // re-throw so the dialog can reset its loading state
    }
  }, [testId]);

  const reset = useCallback(() => {
    setSubmitState("idle");
    setSubmitError(null);
    setSubmitResult(null);
  }, []);

  return {
    submit,
    reset,
    submitState,
    submitResult,
    submitError,
    isSubmitting: submitState === "submitting",
    isSuccess: submitState === "success",
  };
}
