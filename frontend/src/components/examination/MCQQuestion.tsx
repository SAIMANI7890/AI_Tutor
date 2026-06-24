"use client";

import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

interface MCQQuestionProps {
  questionId: string;
  options: string[];
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function MCQQuestion({
  questionId,
  options,
  value,
  onChange,
  disabled = false,
}: MCQQuestionProps) {
  return (
    <RadioGroup
      value={value}
      onValueChange={onChange}
      disabled={disabled}
      className="space-y-3"
      aria-label="Answer choices"
    >
      {options.map((option, idx) => {
        const optionId = `${questionId}-option-${idx}`;
        const isSelected = value === option;
        return (
          <div
            key={idx}
            className={cn(
              "flex items-start gap-3 rounded-xl border-2 px-4 py-3.5 cursor-pointer transition-all duration-150",
              isSelected
                ? "border-blue-500 bg-blue-50"
                : "border-gray-200 bg-white hover:border-blue-200 hover:bg-blue-50/40",
              disabled && "opacity-60 cursor-not-allowed"
            )}
            onClick={() => !disabled && onChange(option)}
          >
            <RadioGroupItem
              value={option}
              id={optionId}
              className="mt-0.5 flex-shrink-0"
              aria-label={`Option ${String.fromCharCode(65 + idx)}: ${option}`}
            />
            <Label
              htmlFor={optionId}
              className={cn(
                "cursor-pointer text-sm leading-relaxed",
                isSelected ? "text-blue-700 font-medium" : "text-gray-700"
              )}
            >
              <span className="font-semibold mr-2 text-gray-400">
                {String.fromCharCode(65 + idx)}.
              </span>
              {option}
            </Label>
          </div>
        );
      })}
    </RadioGroup>
  );
}
