/**
 * Test Configuration Form Component
 * Allows students to configure and generate tests
 */

"use client";

import { useState } from "react";
import { Controller } from "react-hook-form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Slider } from "@/components/ui/slider";
import { Loader2, AlertCircle, BookOpen, ListChecks } from "lucide-react";
import { CATEGORIES } from "@/data/chapters";
import type { QuestionType } from "@/types/examination";

const formSchema = z.object({
  categories: z.array(z.string()).min(1, "Select at least one category"),
  question_type: z.enum(["MCQ", "FILL_BLANKS", "SHORT_ANSWER", "LONG_ANSWER"]),
  question_count: z.number().min(1).max(10),
});

type FormData = z.infer<typeof formSchema>;

interface TestConfigurationFormProps {
  onSubmit: (data: FormData) => void;
  isLoading: boolean;
  error: string | null;
}

const QUESTION_TYPE_INFO = {
  MCQ: {
    label: "Multiple Choice Questions",
    description: "Four options with one correct answer",
    icon: "🎯",
  },
  FILL_BLANKS: {
    label: "Fill in the Blanks",
    description: "Complete sentences with missing terms",
    icon: "✏️",
  },
  SHORT_ANSWER: {
    label: "Short Answer",
    description: "2-3 sentence explanations (30-50 words)",
    icon: "📝",
  },
  LONG_ANSWER: {
    label: "Long Answer",
    description: "Detailed essays (100-150 words)",
    icon: "📄",
  },
};

export function TestConfigurationForm({
  onSubmit,
  isLoading,
  error,
}: TestConfigurationFormProps) {
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [questionCount, setQuestionCount] = useState<number>(5); // max 10 (backend limit)

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      categories: [],
      question_type: "MCQ",
      question_count: 5,
    },
  });

  const questionType = watch("question_type");

  const toggleCategory = (category: string) => {
    const updated = selectedCategories.includes(category)
      ? selectedCategories.filter((c) => c !== category)
      : [...selectedCategories, category];
    
    setSelectedCategories(updated);
    setValue("categories", updated, { shouldValidate: true });
  };

  const handleFormSubmit = (data: FormData) => {
    onSubmit(data);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center gap-2">
          <BookOpen className="h-6 w-6 text-primary" />
          <CardTitle>Configure Your Test</CardTitle>
        </div>
        <CardDescription>
          Select categories, question type, and number of questions to generate your personalized test
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
          {/* Error Alert */}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Category Selection */}
          <div className="space-y-3">
            <Label className="text-base font-semibold">
              Select Categories
              <span className="text-sm font-normal text-muted-foreground ml-2">
                (Choose one or more)
              </span>
            </Label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {CATEGORIES.map((category) => (
                <label
                  key={category}
                  className={`
                    flex items-center space-x-3 p-4 rounded-lg border-2 cursor-pointer transition-all select-none
                    ${
                      selectedCategories.includes(category)
                        ? "border-primary bg-primary/5"
                        : "border-gray-200 hover:border-gray-300"
                    }
                  `}
                >
                  <Checkbox
                    checked={selectedCategories.includes(category)}
                    onCheckedChange={() => toggleCategory(category)}
                  />
                  <div className="flex-1">
                    <p className="font-medium">{category}</p>
                  </div>
                </label>
              ))}
            </div>
            {errors.categories && (
              <p className="text-sm text-red-500">{errors.categories.message}</p>
            )}
            {selectedCategories.length > 0 && (
              <p className="text-sm text-muted-foreground">
                Selected: {selectedCategories.join(", ")}
              </p>
            )}
          </div>

          {/* Question Type Selection */}
          <div className="space-y-3">
            <Label className="text-base font-semibold">Question Type</Label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {Object.entries(QUESTION_TYPE_INFO).map(([type, info]) => {
                const isSelected = questionType === type;
                return (
                  <button
                    key={type}
                    type="button"
                    id={`qtype-${type}`}
                    onClick={() => setValue("question_type", type as QuestionType, { shouldValidate: true })}
                    className={`
                      flex flex-col p-4 rounded-lg border-2 cursor-pointer transition-all text-left w-full
                      ${isSelected
                        ? "border-primary bg-primary/5 ring-2 ring-primary/20"
                        : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                      }
                    `}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-2xl">{info.icon}</span>
                      <span className={`font-semibold ${isSelected ? "text-primary" : "text-gray-900"}`}>
                        {info.label}
                      </span>
                      {isSelected && (
                        <span className="ml-auto text-xs font-medium text-primary bg-primary/10 px-2 py-0.5 rounded-full">
                          Selected
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground">{info.description}</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Question Count Slider */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-base font-semibold">Number of Questions</Label>
              <span className="text-2xl font-bold text-primary">{questionCount}</span>
            </div>
            <input
              type="range"
              min={1}
              max={10}
              value={questionCount}
              onChange={(e) => {
                const value = Number(e.target.value);
                setQuestionCount(value);
                setValue("question_count", value);
              }}
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>1 question</span>
              <span>10 questions</span>
            </div>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            size="lg"
            className="w-full"
            disabled={isLoading || selectedCategories.length === 0}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating Test... (10-20s)
              </>
            ) : (
              <>
                <ListChecks className="mr-2 h-4 w-4" />
                Generate Test
              </>
            )}
          </Button>

          {isLoading && (
            <p className="text-sm text-center text-muted-foreground">
              Our AI is creating personalized questions from your selected topics. Please wait...
            </p>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
