/**
 * Examination Module Types
 * Type definitions for examination/test generation and taking
 */

export type QuestionType = "MCQ" | "FILL_BLANKS" | "SHORT_ANSWER" | "LONG_ANSWER";

export type TestStatus = "GENERATED" | "IN_PROGRESS" | "SUBMITTED" | "EVALUATED";

export interface MCQOptions {
  A: string;
  B: string;
  C: string;
  D: string;
}

export interface Question {
  id: string;
  question_number: number;
  question_type: QuestionType;
  question_text: string;
  options?: string[]; // For MCQ
  category: string;
}

export interface StudentAnswer {
  question_id: string;
  answer: string;
}

export interface Test {
  id: string;
  subject: string;
  question_type: QuestionType;
  selected_categories: string[];
  question_count: number;
  status: TestStatus;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  questions: Question[];
}

export interface GenerateTestRequest {
  categories: string[];
  question_type: QuestionType;
  question_count: number;
}

export interface GenerateTestResponse {
  test_id: string;
  question_count: number;
  status: string;
}

export interface SaveAnswerRequest {
  question_id: string;
  student_answer: string;
}

export interface SaveAnswerResponse {
  answer_id: string;
  question_id: string;
}

export interface SubmitTestResponse {
  test_id: string;
  status: string;
  completed_at: string;
  questions_answered: number;
  total_questions: number;
}

export interface APIResponse<T> {
  success: boolean;
  message: string;
  data: T;
}
