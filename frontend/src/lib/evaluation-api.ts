/**
 * Evaluation API Service
 * Handles all evaluation-related API calls
 */

import { api } from "./api";
import type {
  APIResponse,
  EvaluateAnswerRequest,
  EvaluationResponse,
  Evaluation,
  ChapterPerformance,
  UserPerformanceStats,
  TestEvaluationSummary,
  SubmittedTestSummary,
} from "@/types/evaluation";

const BASE_PATH = "/evaluations";

// ─── Legacy: single-question evaluation ───────────────────────────────────────

export async function getSubmittedTestsForEvaluation(): Promise<
  APIResponse<{
    tests: Array<{
      test_id: string;
      test_name: string;
      created_at: string;
      completed_at: string;
      category: string;
      long_answers: Array<{
        question_id: string;
        question_number: number;
        question_summary: string;
        student_answer: string;
        evaluation_id?: string;
        marks_awarded?: number;
      }>;
    }>;
    count: number;
  }>
> {
  const response = await api.get<
    APIResponse<{
      tests: Array<{
        test_id: string;
        test_name: string;
        created_at: string;
        completed_at: string;
        category: string;
        long_answers: Array<{
          question_id: string;
          question_number: number;
          question_summary: string;
          student_answer: string;
          evaluation_id?: string;
          marks_awarded?: number;
        }>;
      }>;
      count: number;
    }>
  >(`${BASE_PATH}/submitted-tests`);
  return response.data;
}

export async function evaluateAnswer(
  request: EvaluateAnswerRequest
): Promise<APIResponse<EvaluationResponse>> {
  const response = await api.post<APIResponse<EvaluationResponse>>(
    `${BASE_PATH}/evaluate`,
    request
  );
  return response.data;
}

export async function getUserEvaluations(
  limit?: number,
  offset?: number
): Promise<APIResponse<{ evaluations: Evaluation[]; count: number }>> {
  const params = new URLSearchParams();
  if (limit) params.append("limit", limit.toString());
  if (offset) params.append("offset", offset.toString());
  const response = await api.get<
    APIResponse<{ evaluations: Evaluation[]; count: number }>
  >(`${BASE_PATH}?${params.toString()}`);
  return response.data;
}

export async function getEvaluation(
  evaluationId: string
): Promise<APIResponse<Evaluation>> {
  const response = await api.get<APIResponse<Evaluation>>(
    `${BASE_PATH}/${evaluationId}`
  );
  return response.data;
}

export async function getChapterEvaluations(
  chapterName: string
): Promise<APIResponse<{ chapter_name: string; evaluations: Evaluation[]; count: number }>> {
  const response = await api.get<
    APIResponse<{ chapter_name: string; evaluations: Evaluation[]; count: number }>
  >(`${BASE_PATH}/chapter/${encodeURIComponent(chapterName)}`);
  return response.data;
}

export async function getPerformanceStats(): Promise<APIResponse<UserPerformanceStats>> {
  const response = await api.get<APIResponse<UserPerformanceStats>>(
    `${BASE_PATH}/stats/performance`
  );
  return response.data;
}

export async function getChaptersPerformance(): Promise<
  APIResponse<{ chapters: ChapterPerformance[]; count: number }>
> {
  const response = await api.get<
    APIResponse<{ chapters: ChapterPerformance[]; count: number }>
  >(`${BASE_PATH}/stats/chapters`);
  return response.data;
}

export async function getChapterPerformance(
  chapterName: string
): Promise<APIResponse<ChapterPerformance>> {
  const response = await api.get<APIResponse<ChapterPerformance>>(
    `${BASE_PATH}/stats/chapter/${encodeURIComponent(chapterName)}`
  );
  return response.data;
}

export async function deleteEvaluation(
  evaluationId: string
): Promise<APIResponse<{ evaluation_id: string }>> {
  const response = await api.delete<APIResponse<{ evaluation_id: string }>>(
    `${BASE_PATH}/${evaluationId}`
  );
  return response.data;
}

export async function checkEvaluationHealth(): Promise<
  APIResponse<{ status: string; chunks_loaded: number; model: string }>
> {
  const response = await api.get<
    APIResponse<{ status: string; chunks_loaded: number; model: string }>
  >(`${BASE_PATH}/health/check`);
  return response.data;
}

// ─── Full-test evaluation (Phase 7D + 7E) ─────────────────────────────────────

/**
 * Get all submitted/evaluated tests for the Submitted Tests page
 */
export async function getSubmittedTests(): Promise<
  APIResponse<{ tests: SubmittedTestSummary[]; count: number }>
> {
  const response = await api.get<
    APIResponse<{ tests: SubmittedTestSummary[]; count: number }>
  >("/exams/submitted");
  return response.data;
}

/**
 * Check if a test already has evaluation results.
 * Returns { evaluated: false } if not yet evaluated, or full summary if it is.
 */
export async function getTestEvaluationResults(testId: string): Promise<
  APIResponse<
    TestEvaluationSummary | { evaluated: false; evaluation_count: 0; test_id: string }
  >
> {
  const response = await api.get<
    APIResponse<
      TestEvaluationSummary | { evaluated: false; evaluation_count: 0; test_id: string }
    >
  >(`${BASE_PATH}/test/${testId}/results`);
  return response.data;
}

/**
 * Trigger full AI evaluation for all questions in a submitted test.
 * - MCQ / FILL_BLANKS → auto-graded (no AI cost)
 * - SHORT_ANSWER / LONG_ANSWER → AI-graded via RAG + Gemini
 */
export async function evaluateFullTest(
  testId: string
): Promise<APIResponse<TestEvaluationSummary>> {
  const response = await api.post<APIResponse<TestEvaluationSummary>>(
    `${BASE_PATH}/test/${testId}/evaluate`
  );
  return response.data;
}
