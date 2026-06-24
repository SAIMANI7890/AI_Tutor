/**
 * Study Plan API Service
 * Handles all study plan related API calls
 */

import { api } from "./api";
import type {
  APIResponse,
  CreateStudyPlanRequest,
  CreateStudyPlanResponse,
  StudyPlanDetail,
  StudyPlanSummary,
  UpdateStudyItemStatusRequest,
} from "@/types/study-plan";

const BASE_PATH = "/study-plans";

/**
 * Create a new study plan
 */
export async function createStudyPlan(
  request: CreateStudyPlanRequest
): Promise<APIResponse<CreateStudyPlanResponse>> {
  const response = await api.post<APIResponse<CreateStudyPlanResponse>>(
    BASE_PATH,
    request
  );
  return response.data;
}

/**
 * Get all study plans for the current user
 */
export async function getStudyPlans(): Promise<
  APIResponse<{ plans: StudyPlanSummary[]; total_count: number }>
> {
  const response = await api.get<
    APIResponse<{ plans: StudyPlanSummary[]; total_count: number }>
  >(BASE_PATH);
  return response.data;
}

/**
 * Get study plan history (alias for getStudyPlans)
 */
export async function getStudyPlanHistory(): Promise<
  APIResponse<{ plans: StudyPlanSummary[]; total_count: number }>
> {
  return getStudyPlans();
}

/**
 * Get a specific study plan by ID
 */
export async function getStudyPlan(
  planId: number
): Promise<APIResponse<StudyPlanDetail>> {
  const response = await api.get<APIResponse<StudyPlanDetail>>(
    `${BASE_PATH}/${planId}`
  );
  return response.data;
}

/**
 * Update study item status (new task-based endpoint)
 */
export async function updateTaskStatus(
  taskId: number,
  request: UpdateStudyItemStatusRequest
): Promise<
  APIResponse<{
    task_id: number;
    status: string;
    completed_at: string | null;
    completion_percentage: number;
  }>
> {
  const response = await api.patch<
    APIResponse<{
      task_id: number;
      status: string;
      completed_at: string | null;
      completion_percentage: number;
    }>
  >(`${BASE_PATH}/task/${taskId}`, request);
  return response.data;
}

/**
 * Update study item status (legacy endpoint - keeping for backward compatibility)
 */
export async function updateStudyItemStatus(
  planId: number,
  itemId: number,
  request: UpdateStudyItemStatusRequest
): Promise<
  APIResponse<{
    item_id: number;
    day_number: number;
    status: string;
    chapter_name: string | null;
    activity_type: string;
  }>
> {
  const response = await api.patch<
    APIResponse<{
      item_id: number;
      day_number: number;
      status: string;
      chapter_name: string | null;
      activity_type: string;
    }>
  >(`${BASE_PATH}/${planId}/items/${itemId}`, request);
  return response.data;
}

/**
 * Get study progress for the latest plan
 */
export async function getStudyProgress(): Promise<
  APIResponse<{
    plan_id: number;
    exam_date: string;
    total_tasks: number;
    completed_tasks: number;
    pending_tasks: number;
    skipped_tasks: number;
    completion_percentage: number;
  }>
> {
  const response = await api.get<
    APIResponse<{
      plan_id: number;
      exam_date: string;
      total_tasks: number;
      completed_tasks: number;
      pending_tasks: number;
      skipped_tasks: number;
      completion_percentage: number;
    }>
  >(`${BASE_PATH}/progress`);
  return response.data;
}

/**
 * Delete a study plan
 */
export async function deleteStudyPlan(
  planId: number
): Promise<APIResponse<{ plan_id: number }>> {
  const response = await api.delete<APIResponse<{ plan_id: number }>>(
    `${BASE_PATH}/${planId}`
  );
  return response.data;
}
