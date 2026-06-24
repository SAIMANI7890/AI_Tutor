/**
 * Evaluation Form Component
 * Form for submitting answers for AI evaluation
 */

"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2, Send, RotateCcw, AlertCircle } from "lucide-react";
import { CHAPTERS } from "@/data/chapters";
import type { EvaluateAnswerRequest } from "@/types/evaluation";

interface EvaluationFormProps {
  onSubmit: (data: EvaluateAnswerRequest) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

interface FormData {
  question: string;
  student_answer: string;
  chapter_name: string;
  total_marks: number;
}

export function EvaluationForm({
  onSubmit,
  isLoading,
  error,
}: EvaluationFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch,
  } = useForm<FormData>({
    defaultValues: {
      question: "",
      student_answer: "",
      chapter_name: "",
      total_marks: 5,
    },
  });

  const [selectedChapter, setSelectedChapter] = useState<string>("");

  const handleFormSubmit = async (data: FormData) => {
    await onSubmit({
      question: data.question.trim(),
      student_answer: data.student_answer.trim(),
      chapter_name: data.chapter_name || undefined,
      total_marks: data.total_marks,
    });
  };

  const handleClear = () => {
    reset();
    setSelectedChapter("");
  };

  const questionValue = watch("question");
  const answerValue = watch("student_answer");

  return (
    <Card>
      <CardHeader>
        <CardTitle>Submit Answer for Evaluation</CardTitle>
        <p className="text-sm text-muted-foreground">
          Enter your question and answer to receive detailed AI feedback
        </p>
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

          {/* Question Field */}
          <div className="space-y-2">
            <Label htmlFor="question">
              Question <span className="text-red-500">*</span>
            </Label>
            <Textarea
              id="question"
              placeholder="Enter the question you're answering..."
              className="min-h-[100px] resize-y"
              disabled={isLoading}
              {...register("question", {
                required: "Question is required",
                minLength: {
                  value: 10,
                  message: "Question must be at least 10 characters",
                },
              })}
            />
            {errors.question && (
              <p className="text-sm text-red-500">{errors.question.message}</p>
            )}
            <p className="text-xs text-muted-foreground">
              {questionValue.length} characters
            </p>
          </div>

          {/* Student Answer Field */}
          <div className="space-y-2">
            <Label htmlFor="student_answer">
              Your Answer <span className="text-red-500">*</span>
            </Label>
            <Textarea
              id="student_answer"
              placeholder="Write your answer here..."
              className="min-h-[200px] resize-y"
              disabled={isLoading}
              {...register("student_answer", {
                required: "Answer is required",
                minLength: {
                  value: 20,
                  message: "Answer must be at least 20 characters",
                },
              })}
            />
            {errors.student_answer && (
              <p className="text-sm text-red-500">
                {errors.student_answer.message}
              </p>
            )}
            <p className="text-xs text-muted-foreground">
              {answerValue.length} characters
            </p>
          </div>

          {/* Chapter Selection */}
          <div className="space-y-2">
            <Label htmlFor="chapter">Chapter (Optional)</Label>
            <Select
              value={selectedChapter}
              onValueChange={(value) => {
                setSelectedChapter(value);
                setValue("chapter_name", value === "none" ? "" : value);
              }}
              disabled={isLoading}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select a chapter..." />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">None</SelectItem>
                {CHAPTERS.map((chapter) => (
                  <SelectItem key={chapter.chapter_id} value={chapter.chapter_name}>
                    {chapter.chapter_name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <p className="text-xs text-muted-foreground">
              Helps improve evaluation accuracy by providing context
            </p>
          </div>

          {/* Total Marks */}
          <div className="space-y-2">
            <Label htmlFor="total_marks">Total Marks</Label>
            <Select
              defaultValue="5"
              onValueChange={(value) =>
                setValue("total_marks", parseInt(value))
              }
              disabled={isLoading}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {[2, 3, 4, 5, 6, 8, 10].map((marks) => (
                  <SelectItem key={marks} value={marks.toString()}>
                    {marks} marks
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <Button
              type="submit"
              disabled={isLoading}
              className="flex-1"
              size="lg"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Evaluating...
                </>
              ) : (
                <>
                  <Send className="mr-2 h-4 w-4" />
                  Evaluate Answer
                </>
              )}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={handleClear}
              disabled={isLoading}
              size="lg"
            >
              <RotateCcw className="mr-2 h-4 w-4" />
              Clear
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
