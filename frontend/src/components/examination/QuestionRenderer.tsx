"use client";

import type { ExamQuestion } from "@/lib/services/exam.service";
import { MCQQuestion } from "./MCQQuestion";
import { FillBlankQuestion } from "./FillBlankQuestion";
import { ShortAnswerQuestion } from "./ShortAnswerQuestion";
import { LongAnswerQuestion } from "./LongAnswerQuestion";

interface QuestionRendererProps {
  question: ExamQuestion;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function QuestionRenderer({
  question,
  value,
  onChange,
  disabled = false,
}: QuestionRendererProps) {
  switch (question.question_type) {
    case "MCQ":
      return (
        <MCQQuestion
          questionId={question.id}
          options={question.options ?? []}
          value={value}
          onChange={onChange}
          disabled={disabled}
        />
      );
    case "FILL_BLANKS":
      return (
        <FillBlankQuestion
          questionId={question.id}
          value={value}
          onChange={onChange}
          disabled={disabled}
        />
      );
    case "SHORT_ANSWER":
      return (
        <ShortAnswerQuestion
          questionId={question.id}
          value={value}
          onChange={onChange}
          disabled={disabled}
        />
      );
    case "LONG_ANSWER":
      return (
        <LongAnswerQuestion
          questionId={question.id}
          value={value}
          onChange={onChange}
          disabled={disabled}
        />
      );
    default:
      return (
        <p className="text-sm text-red-500">
          Unknown question type: {question.question_type}
        </p>
      );
  }
}
