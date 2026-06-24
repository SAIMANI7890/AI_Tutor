"use client";

import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

interface ShortAnswerQuestionProps {
  questionId: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function ShortAnswerQuestion({
  questionId,
  value,
  onChange,
  disabled = false,
}: ShortAnswerQuestionProps) {
  const textareaId = `${questionId}-short-answer`;
  const wordCount = value.trim() ? value.trim().split(/\s+/).length : 0;

  return (
    <div className="space-y-3">
      <Label htmlFor={textareaId} className="text-sm font-medium text-gray-700">
        Your Answer{" "}
        <span className="text-gray-400 font-normal">(1–2 sentences)</span>
      </Label>
      <Textarea
        id={textareaId}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Write your answer in 1–2 sentences…"
        rows={3}
        className="text-sm leading-relaxed focus:border-blue-500 focus:ring-blue-500/20 resize-none"
        aria-label="Short answer"
        aria-describedby={`${textareaId}-hint`}
      />
      <p id={`${textareaId}-hint`} className="text-xs text-gray-400 flex justify-between">
        <span>Keep your answer brief and precise.</span>
        <span>{wordCount} word{wordCount !== 1 ? "s" : ""}</span>
      </p>
    </div>
  );
}
