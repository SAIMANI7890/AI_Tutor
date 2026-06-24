"use client";

import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

interface LongAnswerQuestionProps {
  questionId: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function LongAnswerQuestion({
  questionId,
  value,
  onChange,
  disabled = false,
}: LongAnswerQuestionProps) {
  const textareaId = `${questionId}-long-answer`;
  const wordCount = value.trim() ? value.trim().split(/\s+/).length : 0;

  return (
    <div className="space-y-3">
      <Label htmlFor={textareaId} className="text-sm font-medium text-gray-700">
        Your Answer{" "}
        <span className="text-gray-400 font-normal">(4–5 sentences)</span>
      </Label>
      <Textarea
        id={textareaId}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Write a detailed answer covering the key points…"
        rows={7}
        className="text-sm leading-relaxed focus:border-blue-500 focus:ring-blue-500/20 resize-none"
        aria-label="Long answer"
        aria-describedby={`${textareaId}-hint`}
      />
      <p id={`${textareaId}-hint`} className="text-xs text-gray-400 flex justify-between">
        <span>Provide a well-structured, detailed response.</span>
        <span>{wordCount} word{wordCount !== 1 ? "s" : ""}</span>
      </p>
    </div>
  );
}
