"use client";

import { useCallback } from "react";

interface UseQuestionNavigationOptions {
  total: number;
  currentIndex: number;
  goTo: (idx: number) => void;
}

/**
 * Thin wrapper around `goTo` from useExam.
 * Adds `jumpTo` (1-based) for the navigator panel and keyboard helpers.
 */
export function useQuestionNavigation({
  total,
  currentIndex,
  goTo,
}: UseQuestionNavigationOptions) {
  /** Jump to a 1-based question number (from the navigator panel) */
  const jumpTo = useCallback(
    (n: number) => goTo(n - 1),
    [goTo]
  );

  const goNext = useCallback(
    () => goTo(Math.min(currentIndex + 1, total - 1)),
    [currentIndex, goTo, total]
  );

  const goPrev = useCallback(
    () => goTo(Math.max(currentIndex - 1, 0)),
    [currentIndex, goTo]
  );

  return {
    jumpTo,
    goNext,
    goPrev,
    isFirst: currentIndex === 0,
    isLast: currentIndex === total - 1,
  };
}
