"use client";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface FillBlankQuestionProps {
  questionId: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function FillBlankQuestion({
  questionId,
  value,
  onChange,
  disabled = false,
}: FillBlankQuestionProps) {
  const inputId = `${questionId}-fill-blank`;
  return (
    <div className="space-y-3">
      <Label htmlFor={inputId} className="text-sm font-medium text-gray-700">
        Fill in the blank:
      </Label>
      <Input
        id={inputId}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Type your answer here…"
        className="max-w-md text-base py-3 focus:border-blue-500 focus:ring-blue-500/20"
        autoComplete="off"
        spellCheck="false"
        aria-label="Fill in the blank answer"
      />
      <p className="text-xs text-gray-400">
        Enter the word or phrase that best completes the sentence.
      </p>
    </div>
  );
}
