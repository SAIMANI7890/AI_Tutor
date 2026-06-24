/**
 * Evaluation Module Types
 * Type definitions for answer evaluation and full-test evaluation
 */

// ─── Basic evaluation types ────────────────────────────────────────────────────

export interface EvaluateAnswerRequest {
  question: string;
  student_answer: string;
  chapter_name?: string;
  test_id?: string;
  question_id?: string;
  total_marks?: number;
}

export interface EvaluationResponse {
  evaluation_id: string;
  question: string;
  student_answer: string;
  model_answer: string;
  marks_awarded: number;
  total_marks: number;
  feedback: string;
  strengths: string[];
  improvements: string[];
  chapter_name: string | null;
  created_at: string;
  percentage: number;
}

export interface Evaluation {
  id: string;
  user_id: number;
  test_id: string | null;
  question_id: string | null;
  question: string;
  student_answer: string;
  model_answer: string;
  marks_awarded: number;
  total_marks: number;
  feedback: string;
  strengths: string[] | null;
  improvements: string[] | null;
  chapter_name: string | null;
  created_at: string;
}

export interface ChapterPerformance {
  chapter_name: string;
  total_evaluations: number;
  total_marks_obtained: number;
  total_marks_possible: number;
  average_percentage: number;
  latest_evaluation_date: string;
}

export interface UserPerformanceStats {
  user_id: number;
  total_evaluations: number;
  total_marks_obtained: number;
  total_marks_possible: number;
  overall_percentage: number;
  chapters_covered: number;
  recent_evaluations: Evaluation[];
}

export interface APIResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export type ScoreStatus = "excellent" | "good" | "needs-improvement";

export interface EvaluationFilters {
  searchQuery: string;
  chapter: string;
  scoreRange: string;
  sortBy: "newest" | "oldest" | "highest" | "lowest";
}

export interface SubmittedTestLongAnswer {
  question_id: string;
  question_number: number;
  question_summary: string;
  student_answer: string;
  evaluation_id?: string;
  marks_awarded?: number;
}

export interface SubmittedTestForEvaluation {
  test_id: string;
  test_name: string;
  created_at: string;
  completed_at: string;
  category: string;
  long_answers: SubmittedTestLongAnswer[];
}

// ─── Full-test evaluation workflow types (Phase 7D + 7E) ──────────────────────

export interface QuestionEvaluationResult {
  question_id: string;
  question_number: number;
  question_type: string;
  question_text: string;
  student_answer: string;
  correct_answer: string | null;  // MCQ/FILL_BLANKS only
  model_answer: string;
  marks_awarded: number;
  total_marks: number;
  feedback: string;
  strengths: string[];
  improvements: string[];
  category: string;
  is_auto_graded: boolean;
  evaluation_id: string;
}

export interface AIInsights {
  strengths: string[];
  weak_areas: string[];
  recommendations: string[];
}

export interface TestEvaluationSummary {
  test_id: string;
  test_name: string;
  question_type: string;
  categories: string[];
  question_count: number;
  submitted_at: string;
  status: string;
  total_marks_awarded: number;
  total_marks_possible: number;
  percentage: number;
  performance_level: "Excellent" | "Good" | "Average" | "Needs Improvement";
  question_results: QuestionEvaluationResult[];
  ai_insights: AIInsights;
  evaluated: boolean;
  evaluation_count: number;
}

export interface SubmittedTestSummary {
  id: string;
  subject: string;
  question_type: string;
  selected_categories: string[];
  question_count: number;
  status: "SUBMITTED" | "EVALUATED";
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export type PerformanceLevel = "Excellent" | "Good" | "Average" | "Needs Improvement";
