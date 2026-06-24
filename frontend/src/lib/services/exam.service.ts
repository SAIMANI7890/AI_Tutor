import { api } from "@/lib/api";
import type { APIResponse } from "@/lib/types";

// ─────────────────────────────────────────────
// Domain types
// ─────────────────────────────────────────────

export type QuestionType = "MCQ" | "FILL_BLANKS" | "SHORT_ANSWER" | "LONG_ANSWER";
export type TestStatus = "GENERATED" | "IN_PROGRESS" | "SUBMITTED" | "EVALUATED";
export type Category = "History" | "Geography" | "Politics" | "Economics";

export interface ExamQuestion {
  id: string;
  question_number: number;
  question_type: QuestionType;
  question_text: string;
  category: string;
  options?: string[]; // MCQ only
}

export interface ExamDetail {
  id: string;
  subject: string;
  question_type: QuestionType;
  selected_categories: string[];
  question_count: number;
  status: TestStatus;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  questions: ExamQuestion[];
}

export interface ExamSummary {
  id: string;
  subject: string;
  question_type: QuestionType;
  selected_categories: string[];
  question_count: number;
  status: TestStatus;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface SavedAnswer {
  answer_id: string;
  question_id: string;
  student_answer: string | null;
  updated_at: string;
}

export interface GenerateExamRequest {
  categories: string[];
  question_type: QuestionType;
  question_count: number;
}

export interface GenerateExamResult {
  test_id: string;
  question_count: number;
  status: string;
}

export interface SubmitResult {
  test_id: string;
  status: string;
  completed_at: string;
  questions_answered: number;
  total_questions: number;
}

// ─────────────────────────────────────────────
// Service
// ─────────────────────────────────────────────

export const examService = {
  async generate(req: GenerateExamRequest): Promise<APIResponse<GenerateExamResult>> {
    const res = await api.post<APIResponse<GenerateExamResult>>("/exams/generate", req);
    return res.data;
  },

  async list(): Promise<APIResponse<ExamSummary[]>> {
    const res = await api.get<APIResponse<ExamSummary[]>>("/exams/");
    return res.data;
  },

  async getDetail(testId: string): Promise<APIResponse<ExamDetail>> {
    const res = await api.get<APIResponse<ExamDetail>>(`/exams/${testId}`);
    return res.data;
  },

  async getQuestions(testId: string): Promise<APIResponse<ExamQuestion[]>> {
    const res = await api.get<APIResponse<ExamQuestion[]>>(`/exams/${testId}/questions`);
    return res.data;
  },

  async saveAnswer(
    testId: string,
    questionId: string,
    studentAnswer: string
  ): Promise<APIResponse<{ answer_id: string; question_id: string }>> {
    const res = await api.post<APIResponse<{ answer_id: string; question_id: string }>>(
      `/exams/${testId}/answer`,
      { question_id: questionId, student_answer: studentAnswer }
    );
    return res.data;
  },

  async getAnswers(testId: string): Promise<APIResponse<SavedAnswer[]>> {
    const res = await api.get<APIResponse<SavedAnswer[]>>(`/exams/${testId}/answers`);
    return res.data;
  },

  async submit(testId: string): Promise<APIResponse<SubmitResult>> {
    const res = await api.post<APIResponse<SubmitResult>>(`/exams/${testId}/submit`);
    return res.data;
  },

  async getHistory(): Promise<APIResponse<ExamSummary[]>> {
    const res = await api.get<APIResponse<ExamSummary[]>>("/exams/history");
    return res.data;
  },

  async delete(testId: string): Promise<APIResponse<{ test_id: string; message: string }>> {
    const res = await api.delete<APIResponse<{ test_id: string; message: string }>>(`/exams/${testId}`);
    return res.data;
  },
};
