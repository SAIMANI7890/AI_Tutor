/**
 * Evaluation History Page
 * View all previous evaluations with filtering and sorting
 */

"use client";

import { useEffect, useState, useMemo } from "react";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { EvaluationHistoryTable } from "@/components/evaluation/EvaluationHistoryTable";
import { EvaluationFilters } from "@/components/evaluation/EvaluationFilters";
import { EvaluationDetailsDialog } from "@/components/evaluation/EvaluationDetailsDialog";
import { ChapterPerformanceCard } from "@/components/evaluation/ChapterPerformanceCard";
import { ArrowLeft, AlertCircle, TrendingUp, History } from "lucide-react";
import Link from "next/link";
import {
  getUserEvaluations,
  deleteEvaluation,
  getChaptersPerformance,
} from "@/lib/evaluation-api";
import {
  filterEvaluations,
  sortEvaluations,
  getUniqueChapters,
} from "@/lib/evaluation-utils";
import type {
  Evaluation,
  EvaluationFilters as Filters,
  ChapterPerformance,
} from "@/types/evaluation";

export default function EvaluationHistoryPage() {
  // State management
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [chapterPerformance, setChapterPerformance] = useState<
    ChapterPerformance[]
  >([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingPerformance, setIsLoadingPerformance] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [selectedEvaluation, setSelectedEvaluation] =
    useState<Evaluation | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  // Filter state
  const [filters, setFilters] = useState<Filters>({
    searchQuery: "",
    chapter: "all",
    scoreRange: "all",
    sortBy: "newest",
  });

  // Load evaluations on mount
  useEffect(() => {
    loadEvaluations();
    loadChapterPerformance();
  }, []);

  const loadEvaluations = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await getUserEvaluations();

      if (response.success) {
        setEvaluations(response.data.evaluations);
      } else {
        setError(response.message || "Failed to load evaluations");
      }
    } catch (err: any) {
      console.error("Error loading evaluations:", err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to load evaluations"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const loadChapterPerformance = async () => {
    try {
      setIsLoadingPerformance(true);
      const response = await getChaptersPerformance();

      if (response.success) {
        setChapterPerformance(response.data.chapters);
      }
    } catch (err: any) {
      console.error("Error loading chapter performance:", err);
      // Don't set error state for performance stats - it's not critical
    } finally {
      setIsLoadingPerformance(false);
    }
  };

  // Handle delete
  const handleDelete = async (evaluationId: string) => {
    try {
      setDeletingId(evaluationId);
      const response = await deleteEvaluation(evaluationId);

      if (response.success) {
        setEvaluations((prev) =>
          prev.filter((evaluation) => evaluation.id !== evaluationId)
        );
        // Reload performance stats after deletion
        loadChapterPerformance();
      } else {
        alert(response.message || "Failed to delete evaluation");
      }
    } catch (err: any) {
      console.error("Error deleting evaluation:", err);
      alert(
        err.response?.data?.detail ||
          err.message ||
          "Failed to delete evaluation"
      );
    } finally {
      setDeletingId(null);
    }
  };

  // Handle view details
  const handleViewDetails = (evaluation: Evaluation) => {
    setSelectedEvaluation(evaluation);
    setDialogOpen(true);
  };

  // Get available chapters from evaluations
  const availableChapters = useMemo(
    () => getUniqueChapters(evaluations),
    [evaluations]
  );

  // Apply filters and sorting
  const filteredAndSortedEvaluations = useMemo(() => {
    const filtered = filterEvaluations(evaluations, {
      searchQuery: filters.searchQuery,
      chapter: filters.chapter,
      scoreRange: filters.scoreRange,
    });
    return sortEvaluations(filtered, filters.sortBy);
  }, [evaluations, filters]);

  // Loading state
  if (isLoading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
          <DashboardHeader />
          <SocialNav />
          <main className="container mx-auto px-4 py-8 max-w-7xl">
            <Skeleton className="h-12 w-64 mb-4" />
            <Skeleton className="h-6 w-96 mb-8" />
            <div className="space-y-6">
              <Skeleton className="h-32" />
              <Skeleton className="h-96" />
            </div>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  // Error state
  if (error) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
          <DashboardHeader />
          <SocialNav />
          <main className="container mx-auto px-4 py-8 max-w-7xl">
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
            <div className="flex gap-3">
              <Button onClick={loadEvaluations}>Retry</Button>
              <Link href="/dashboard/social/evaluation">
                <Button variant="outline">Back to Evaluation</Button>
              </Link>
            </div>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        <main className="container mx-auto px-4 py-8 max-w-7xl">
          {/* Page Header */}
          <div className="mb-8">
            <div className="flex items-center gap-4 mb-4">
              <Link href="/dashboard/social/evaluation">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back
                </Button>
              </Link>
            </div>
            <div className="flex items-center gap-3 mb-2">
              <div className="bg-purple-100 p-2.5 rounded-xl">
                <History className="h-6 w-6 text-purple-600" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900">
                Evaluation History
              </h1>
            </div>
            <p className="text-gray-500 ml-14">
              Review your past evaluations and track your progress
            </p>
          </div>

          {/* Chapter Performance Section */}
          {chapterPerformance.length > 0 && (
            <div className="mb-8">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="h-5 w-5 text-primary" />
                <h2 className="text-xl font-semibold">Chapter Performance</h2>
              </div>
              {isLoadingPerformance ? (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {[1, 2, 3].map((i) => (
                    <Skeleton key={i} className="h-48" />
                  ))}
                </div>
              ) : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                  {chapterPerformance.map((chapter) => (
                    <ChapterPerformanceCard
                      key={chapter.chapter_name}
                      performance={chapter}
                    />
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Filters */}
          {evaluations.length > 0 && (
            <div className="mb-6">
              <EvaluationFilters
                filters={filters}
                onFiltersChange={setFilters}
                chapters={availableChapters}
              />
            </div>
          )}

          {/* Results Summary */}
          {evaluations.length > 0 && (
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                Showing {filteredAndSortedEvaluations.length} of{" "}
                {evaluations.length} evaluation
                {evaluations.length !== 1 ? "s" : ""}
              </p>
            </div>
          )}

          {/* Evaluations Table/List */}
          <EvaluationHistoryTable
            evaluations={filteredAndSortedEvaluations}
            onViewDetails={handleViewDetails}
            onDelete={handleDelete}
            isDeleting={deletingId}
          />

          {/* Details Dialog */}
          <EvaluationDetailsDialog
            evaluation={selectedEvaluation}
            open={dialogOpen}
            onOpenChange={setDialogOpen}
          />
        </main>
      </div>
    </ProtectedRoute>
  );
}
