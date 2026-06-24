/**
 * Question Display Component
 * Renders different question types with appropriate input methods
 */

"use client";

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import type { Question, QuestionType } from "@/types/examination";

interface QuestionDisplayProps {
  question: Question;
  currentAnswer: string;
  onAnswerChange: (answer: string) => void;
  questionNumber: number;
  totalQuestions: number;
}

export function QuestionDisplay({
  question,
  currentAnswer,
  onAnswerChange,
  questionNumber,
  totalQuestions,
}: QuestionDisplayProps) {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      History: "bg-blue-100 text-blue-800",
      Geography: "bg-green-100 text-green-800",
      Politics: "bg-purple-100 text-purple-800",
      Economics: "bg-orange-100 text-orange-800",
    };
    return colors[category] || "bg-gray-100 text-gray-800";
  };

  const getQuestionTypeLabel = (type: QuestionType) => {
    const labels: Record<QuestionType, string> = {
      MCQ: "Multiple Choice",
      FILL_BLANKS: "Fill in the Blanks",
      SHORT_ANSWER: "Short Answer",
      LONG_ANSWER: "Long Answer",
    };
    return labels[type];
  };

  return (
    <Card className="w-full">
      <CardHeader className="space-y-4">
        {/* Question Header */}
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-base">
              Question {questionNumber} of {totalQuestions}
            </Badge>
            <Badge className={getCategoryColor(question.category)}>
              {question.category}
            </Badge>
          </div>
          <Badge variant="secondary">
            {getQuestionTypeLabel(question.question_type)}
          </Badge>
        </div>

        {/* Question Text */}
        <div className="pt-2">
          <p className="text-lg font-medium leading-relaxed">
            {question.question_text}
          </p>
        </div>
      </CardHeader>

      <CardContent>
        {/* MCQ Options */}
        {question.question_type === "MCQ" && question.options && (
          <RadioGroup value={currentAnswer} onValueChange={onAnswerChange}>
            <div className="space-y-3">
              {question.options.map((option, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-3 p-4 rounded-lg border-2 hover:border-primary/50 transition-colors cursor-pointer"
                  onClick={() => onAnswerChange(option)}
                >
                  <RadioGroupItem value={option} id={`option-${index}`} className="mt-0.5" />
                  <Label
                    htmlFor={`option-${index}`}
                    className="flex-1 cursor-pointer text-base leading-relaxed"
                  >
                    <span className="font-semibold mr-2">
                      {String.fromCharCode(65 + index)}.
                    </span>
                    {option}
                  </Label>
                </div>
              ))}
            </div>
          </RadioGroup>
        )}

        {/* Fill in the Blanks */}
        {question.question_type === "FILL_BLANKS" && (
          <div className="space-y-3">
            <Label htmlFor="fill-blank" className="text-base">
              Your Answer
            </Label>
            <Input
              id="fill-blank"
              type="text"
              value={currentAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              placeholder="Type your answer here..."
              className="text-base"
            />
            <p className="text-sm text-muted-foreground">
              Tip: Keep your answer concise (1-4 words typically)
            </p>
          </div>
        )}

        {/* Short Answer */}
        {question.question_type === "SHORT_ANSWER" && (
          <div className="space-y-3">
            <Label htmlFor="short-answer" className="text-base">
              Your Answer
            </Label>
            <Textarea
              id="short-answer"
              value={currentAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              placeholder="Write your answer in 2-3 sentences (30-50 words)..."
              rows={5}
              className="text-base resize-none"
            />
            <div className="flex items-center justify-between text-sm text-muted-foreground">
              <span>Tip: Answer in 2-3 complete sentences</span>
              <span>{currentAnswer.split(/\s+/).filter(Boolean).length} words</span>
            </div>
          </div>
        )}

        {/* Long Answer */}
        {question.question_type === "LONG_ANSWER" && (
          <div className="space-y-3">
            <Label htmlFor="long-answer" className="text-base">
              Your Answer
            </Label>
            <Textarea
              id="long-answer"
              value={currentAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              placeholder="Write your detailed answer in 5-6 sentences (100-150 words)..."
              rows={10}
              className="text-base resize-none"
            />
            <div className="flex items-center justify-between text-sm text-muted-foreground">
              <span>Tip: Structure your answer with introduction, main points, and conclusion</span>
              <span>{currentAnswer.split(/\s+/).filter(Boolean).length} words</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
