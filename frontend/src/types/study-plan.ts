/**
 * Study Plan Type Definitions
 * Matches backend API schemas
 */

export enum ActivityType {
  STUDY = "Study",
  REVISION = "Revision",
  MOCK_TEST = "MockTest",
}

export enum StudyStatus {
  PENDING = "Pending",
  COMPLETED = "Completed",
  SKIPPED = "Skipped",
}

export interface StudyPlanItem {
  id: number;
  study_plan_id: number;
  day_number: number;
  study_date: string;
  activity_type: ActivityType;
  chapter_id: number | null;
  chapter_name: string | null;
  allocated_hours: number;
  status: StudyStatus;
  completed_at: string | null;
  created_at: string;
}

export interface StudyPlanSummary {
  id: number;
  exam_date: string;
  daily_study_hours: number;
  created_at: string;
  updated_at: string;
  completion_percentage: number;
  total_items: number;
  completed_items: number;
}

export interface StudyPlanDetail {
  id: number;
  user_id: number;
  exam_date: string;
  daily_study_hours: number;
  created_at: string;
  updated_at: string;
  completion_percentage: number;
  total_items: number;
  completed_items: number;
  items: StudyPlanItem[];
}

export interface CreateStudyPlanRequest {
  exam_date: string;
  daily_study_hours: number;
  selected_chapter_ids: number[];
}

export interface CreateStudyPlanResponse {
  plan_id: number;
  total_days: number;
  items_count: number;
  exam_date: string;
  daily_study_hours: number;
}

export interface UpdateStudyItemStatusRequest {
  status: StudyStatus;
}

export interface Chapter {
  chapter_id: number;
  chapter_name: string;
  category: string;
  difficulty: string;
  estimated_study_hours: number;
}

export interface APIResponse<T> {
  success: boolean;
  message: string;
  data: T;
}
