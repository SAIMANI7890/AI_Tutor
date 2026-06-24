/**
 * Evaluation Utility Functions
 */

import type { ScoreStatus, Evaluation } from "@/types/evaluation";

/**
 * Calculate percentage from marks
 */
export function calculatePercentage(
  marksAwarded: number,
  totalMarks: number
): number {
  if (totalMarks === 0) return 0;
  return Math.round((marksAwarded / totalMarks) * 100);
}

/**
 * Get score status based on percentage
 */
export function getScoreStatus(percentage: number): ScoreStatus {
  if (percentage >= 80) return "excellent";
  if (percentage >= 60) return "good";
  return "needs-improvement";
}

/**
 * Get score status color
 */
export function getScoreStatusColor(status: ScoreStatus): string {
  switch (status) {
    case "excellent":
      return "text-green-600 bg-green-50 border-green-200";
    case "good":
      return "text-blue-600 bg-blue-50 border-blue-200";
    case "needs-improvement":
      return "text-amber-600 bg-amber-50 border-amber-200";
  }
}

/**
 * Get score status label
 */
export function getScoreStatusLabel(status: ScoreStatus): string {
  switch (status) {
    case "excellent":
      return "Excellent";
    case "good":
      return "Good";
    case "needs-improvement":
      return "Needs Improvement";
  }
}

/**
 * Format date for display
 */
export function formatEvaluationDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

/**
 * Get relative time (e.g., "2 hours ago")
 */
export function getRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (diffInSeconds < 60) return "Just now";
  if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
  }
  if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours} hour${hours > 1 ? "s" : ""} ago`;
  }
  if (diffInSeconds < 604800) {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days} day${days > 1 ? "s" : ""} ago`;
  }
  return formatEvaluationDate(dateString);
}

/**
 * Truncate text with ellipsis
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
}

/**
 * Filter evaluations based on filters
 */
export function filterEvaluations(
  evaluations: Evaluation[],
  filters: {
    searchQuery?: string;
    chapter?: string;
    scoreRange?: string;
  }
): Evaluation[] {
  let filtered = [...evaluations];

  // Search filter
  if (filters.searchQuery) {
    const query = filters.searchQuery.toLowerCase();
    filtered = filtered.filter((evaluation) =>
      evaluation.question.toLowerCase().includes(query) ||
      evaluation.student_answer.toLowerCase().includes(query)
    );
  }

  // Chapter filter
  if (filters.chapter && filters.chapter !== "all") {
    filtered = filtered.filter((evaluation) => evaluation.chapter_name === filters.chapter);
  }

  // Score range filter
  if (filters.scoreRange && filters.scoreRange !== "all") {
    filtered = filtered.filter((evaluation) => {
      const percentage = calculatePercentage(
        evaluation.marks_awarded,
        evaluation.total_marks
      );
      const status = getScoreStatus(percentage);
      return status === filters.scoreRange;
    });
  }

  return filtered;
}

/**
 * Sort evaluations
 */
export function sortEvaluations(
  evaluations: Evaluation[],
  sortBy: "newest" | "oldest" | "highest" | "lowest"
): Evaluation[] {
  const sorted = [...evaluations];

  switch (sortBy) {
    case "newest":
      return sorted.sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    case "oldest":
      return sorted.sort(
        (a, b) =>
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      );
    case "highest":
      return sorted.sort((a, b) => {
        const percentA = calculatePercentage(a.marks_awarded, a.total_marks);
        const percentB = calculatePercentage(b.marks_awarded, b.total_marks);
        return percentB - percentA;
      });
    case "lowest":
      return sorted.sort((a, b) => {
        const percentA = calculatePercentage(a.marks_awarded, a.total_marks);
        const percentB = calculatePercentage(b.marks_awarded, b.total_marks);
        return percentA - percentB;
      });
    default:
      return sorted;
  }
}

/**
 * Get unique chapters from evaluations
 */
export function getUniqueChapters(evaluations: Evaluation[]): string[] {
  const chapters = evaluations
    .map((evaluation) => evaluation.chapter_name)
    .filter((chapter): chapter is string => chapter !== null);
  return Array.from(new Set(chapters)).sort();
}
