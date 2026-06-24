"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { examService, type ExamQuestion, type SavedAnswer, type TestStatus } from "@/lib/services/exam.service";

export type SaveStatus = "idle" | "saving" | "saved" | "error";

/**
 * Manages all state for an in-progress exam:
 *  - questions, answers, current index
 *  - exam status (for read-only view)
 *  - debounced autosave (1 000 ms)
 *  - page-refresh answer recovery
 */
export function useExam(testId: string) {
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({}); // questionId → text
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<SaveStatus>("idle");
  const [examStatus, setExamStatus] = useState<TestStatus | null>(null);

  // Debounce timer ref
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  // Track pending saves so we can warn on navigation
  const pendingSaveRef = useRef(false);

  // Check if exam is read-only (submitted or evaluated)
  const isReadOnly = examStatus === "SUBMITTED" || examStatus === "EVALUATED";

  // ── Load questions + restore saved answers + get exam status ────────────
  useEffect(() => {
    if (!testId) return;
    let cancelled = false;

    async function load() {
      setIsLoading(true);
      setError(null);
      try {
        const [qRes, aRes, detailRes] = await Promise.all([
          examService.getQuestions(testId),
          examService.getAnswers(testId),
          examService.getDetail(testId),
        ]);

        if (cancelled) return;

        if (qRes.success && qRes.data) {
          setQuestions(qRes.data);
        } else {
          setError(qRes.message || "Failed to load questions");
        }

        if (aRes.success && aRes.data) {
          const restored: Record<string, string> = {};
          aRes.data.forEach((a: SavedAnswer) => {
            if (a.student_answer) restored[a.question_id] = a.student_answer;
          });
          setAnswers(restored);
        }

        if (detailRes.success && detailRes.data) {
          setExamStatus(detailRes.data.status);
        }
      } catch (e: any) {
        if (!cancelled) setError(e?.response?.data?.detail || "Network error");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [testId]);

  // ── Warn before unload if save is pending ───────────────────────────────
  useEffect(() => {
    const handler = (e: BeforeUnloadEvent) => {
      if (pendingSaveRef.current) {
        e.preventDefault();
        e.returnValue = "";
      }
    };
    window.addEventListener("beforeunload", handler);
    return () => window.removeEventListener("beforeunload", handler);
  }, []);

  // ── Answer change with debounced autosave (disabled for read-only) ──────
  const setAnswer = useCallback(
    (questionId: string, value: string) => {
      // Don't allow changes if exam is submitted/evaluated
      if (isReadOnly) return;

      setAnswers((prev) => ({ ...prev, [questionId]: value }));
      pendingSaveRef.current = true;
      setSaveStatus("saving");

      if (debounceRef.current) clearTimeout(debounceRef.current);

      debounceRef.current = setTimeout(async () => {
        try {
          await examService.saveAnswer(testId, questionId, value);
          setSaveStatus("saved");
          pendingSaveRef.current = false;
          // Reset to idle after 2 s
          setTimeout(() => setSaveStatus("idle"), 2000);
        } catch {
          setSaveStatus("error");
          pendingSaveRef.current = false;
        }
      }, 1000);
    },
    [testId, isReadOnly]
  );

  // Navigation helpers
  const goTo = useCallback((idx: number) => {
    setCurrentIndex(Math.max(0, Math.min(idx, questions.length - 1)));
  }, [questions.length]);

  const goNext = useCallback(() => goTo(currentIndex + 1), [currentIndex, goTo]);
  const goPrev = useCallback(() => goTo(currentIndex - 1), [currentIndex, goTo]);

  const answeredCount = questions.filter((q) => !!answers[q.id]).length;

  return {
    questions,
    answers,
    currentIndex,
    currentQuestion: questions[currentIndex] ?? null,
    isLoading,
    error,
    saveStatus,
    answeredCount,
    examStatus,
    isReadOnly,
    setAnswer,
    goTo,
    goNext,
    goPrev,
  };
}
