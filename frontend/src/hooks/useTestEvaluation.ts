/**
 * useTestEvaluation Hook
 * Manages all state for the /evaluation/[testId] page
 */

"use client";

import { useState, useCallback } from "react";
import { getTestEvaluationResults, evaluateFullTest } from "@/lib/evaluation-api";
import type { TestEvaluationSummary } from "@/types/evaluation";

type PageState = "loading" | "pre-evaluation" | "evaluating" | "results" | "error";

interface UseTestEvaluationReturn {
  pageState: PageState;
  summary: TestEvaluationSummary | null;
  error: string | null;
  loadExistingResults: () => Promise<void>;
  triggerEvaluation: () => Promise<void>;
}

export function useTestEvaluation(testId: string): UseTestEvaluationReturn {
  const [pageState, setPageState] = useState<PageState>("loading");
  const [summary, setSummary] = useState<TestEvaluationSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadExistingResults = useCallback(async () => {
    setPageState("loading");
    setError(null);
    try {
      const res = await getTestEvaluationResults(testId);
      if (res.success && res.data && "evaluated" in res.data && res.data.evaluated === true) {
        setSummary(res.data as TestEvaluationSummary);
        setPageState("results");
      } else {
        setPageState("pre-evaluation");
      }
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Failed to load evaluation data";
      setError(msg);
      setPageState("error");
    }
  }, [testId]);

  const triggerEvaluation = useCallback(async () => {
    setPageState("evaluating");
    setError(null);
    try {
      const res = await evaluateFullTest(testId);
      if (res.success && res.data) {
        setSummary(res.data);
        setPageState("results");
      } else {
        throw new Error(res.message || "Evaluation failed");
      }
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Evaluation failed. Please try again.";
      setError(msg);
      setPageState("error");
    }
  }, [testId]);

  return { pageState, summary, error, loadExistingResults, triggerEvaluation };
}
