/**
 * Examination API Service
 * Handles all examination-related API calls
 */

import { api } from "./api";
import type {
  APIResponse,
  GenerateTestRequest,
  GenerateTestResponse,
  Test,
  SaveAnswerRequest,
  SaveAnswerResponse,
  SubmitTestResponse,
  StudentAnswer,
} from "@/types/examination";

const BASE_PATH = "/exams";

/**
 * Generate a new test
 */
export async function generateTest(
  request: GenerateTestRequest
): Promise<APIResponse<GenerateTestResponse>> {
  const response = await api.post<APIResponse<GenerateTestResponse>>(
    `${BASE_PATH}/generate`,
    request
  );
  return response.data;
}

/**
 * Get test details with questions
 */
export async function getTest(testId: string): Promise<APIResponse<Test>> {
  const response = await api.get<APIResponse<Test>>(`${BASE_PATH}/${testId}`);
  return response.data;
}

/**
 * Get all questions for a test
 */
export async function getTestQuestions(
  testId: string
): Promise<APIResponse<Test["questions"]>> {
  const response = await api.get<APIResponse<Test["questions"]>>(
    `${BASE_PATH}/${testId}/questions`
  );
  return response.data;
}

/**
 * Save/update a student answer
 */
export async function saveAnswer(
  testId: string,
  request: SaveAnswerRequest
): Promise<APIResponse<SaveAnswerResponse>> {
  const response = await api.post<APIResponse<SaveAnswerResponse>>(
    `${BASE_PATH}/${testId}/answer`,
    request
  );
  return response.data;
}

/**
 * Get saved answers for a test
 */
export async function getSavedAnswers(
  testId: string
): Promise<APIResponse<StudentAnswer[]>> {
  const response = await api.get<APIResponse<StudentAnswer[]>>(
    `${BASE_PATH}/${testId}/answers`
  );
  return response.data;
}

/**
 * Submit test for evaluation
 */
export async function submitTest(
  testId: string
): Promise<APIResponse<SubmitTestResponse>> {
  const response = await api.post<APIResponse<SubmitTestResponse>>(
    `${BASE_PATH}/${testId}/submit`
  );
  return response.data;
}

/**
 * Get test history
 */
export async function getTestHistory(): Promise<
  APIResponse<{ tests: Test[]; total_count: number }>
> {
  const response = await api.get<
    APIResponse<{ tests: Test[]; total_count: number }>
  >(`${BASE_PATH}/history`);
  return response.data;
}
