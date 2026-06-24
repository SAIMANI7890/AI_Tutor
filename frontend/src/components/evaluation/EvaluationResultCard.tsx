/**
 * Evaluation Result Card Component
 * Complete evaluation display with all details
 */

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ScoreCard } from "./ScoreCard";
import { FeedbackCard } from "./FeedbackCard";
import { StrengthsCard } from "./StrengthsCard";
import { ImprovementCard } from "./ImprovementCard";
import { ModelAnswerCard } from "./ModelAnswerCard";
import { FileQuestion, User } from "lucide-react";
import type { EvaluationResponse } from "@/types/evaluation";
import { formatEvaluationDate } from "@/lib/evaluation-utils";

interface EvaluationResultCardProps {
  evaluation: EvaluationResponse;
}

export function EvaluationResultCard({ evaluation }: EvaluationResultCardProps) {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Score Section */}
      <ScoreCard
        marksAwarded={evaluation.marks_awarded}
        totalMarks={evaluation.total_marks}
        size="lg"
      />

      {/* Feedback */}
      <FeedbackCard feedback={evaluation.feedback} />

      {/* Strengths and Improvements */}
      <div className="grid gap-6 md:grid-cols-2">
        <StrengthsCard strengths={evaluation.strengths} />
        <ImprovementCard improvements={evaluation.improvements} />
      </div>

      {/* Model Answer */}
      <ModelAnswerCard modelAnswer={evaluation.model_answer} />

      <Separator />

      {/* Question Section */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <FileQuestion className="w-5 h-5" />
            Question
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {evaluation.question}
          </p>
        </CardContent>
      </Card>

      {/* Student Answer Section */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <User className="w-5 h-5" />
            Your Answer
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {evaluation.student_answer}
          </p>
        </CardContent>
      </Card>

      {/* Metadata */}
      <div className="flex justify-between items-center text-sm text-muted-foreground">
        <span>
          {evaluation.chapter_name && (
            <>Chapter: {evaluation.chapter_name}</>
          )}
        </span>
        <span>Evaluated on {formatEvaluationDate(evaluation.created_at)}</span>
      </div>
    </div>
  );
}
