"use client";

import { useCallback, useEffect, useState } from "react";
import { examService, type ExamSummary } from "@/lib/services/exam.service";

export type StatusFilter = "ALL" | "GENERATED" | "IN_PROGRESS" | "SUBMITTED" | "EVALUATED";
export type TypeFilter = "ALL" | "MCQ" | "FILL_BLANKS" | "SHORT_ANSWER" | "LONG_ANSWER";

export function useExamHistory() {
  const [exams, setExams] = useState<ExamSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters / search
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("ALL");
  const [typeFilter, setTypeFilter] = useState<TypeFilter>("ALL");
  const [searchQuery, setSearchQuery] = useState("");

  const load = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await examService.getHistory();
      if (res.success && res.data) {
        setExams(res.data);
      } else {
        setError(res.message || "Failed to load history");
      }
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Network error");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = exams.filter((e) => {
    if (statusFilter !== "ALL" && e.status !== statusFilter) return false;
    if (typeFilter !== "ALL" && e.question_type !== typeFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const inId = e.id.toLowerCase().includes(q);
      const inCat = e.selected_categories.some((c) => c.toLowerCase().includes(q));
      if (!inId && !inCat) return false;
    }
    return true;
  });

  return {
    exams: filtered,
    totalCount: exams.length,
    isLoading,
    error,
    statusFilter,
    typeFilter,
    searchQuery,
    setStatusFilter,
    setTypeFilter,
    setSearchQuery,
    reload: load,
  };
}
