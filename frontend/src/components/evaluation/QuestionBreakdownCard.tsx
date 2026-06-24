/**
 * QuestionBreakdownCard – per-question evaluation result, expandable accordion
 */
"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  ChevronDown,
  ChevronUp,
  CheckCircle2,
  XCircle,
  Zap,
  BookOpen,
} from "lucide-react";
import type { QuestionEvaluationResult } from "@/types/evaluation";

interface QuestionBreakdownCardProps {
  result: QuestionEvaluationResult;
  defaultOpen?: boolean;
}

function scoreColour(pct: number) {
  if (pct >= 90) return { indicator: "bg-emerald-500", badge: "bg-emerald-100 text-emerald-800 border-emerald-300", text: "text-emerald-700" };
  if (pct >= 70) return { indicator: "bg-blue-500", badge: "bg-blue-100 text-blue-800 border-blue-300", text: "text-blue-700" };
  if (pct >= 50) return { indicator: "bg-amber-500", badge: "bg-amber-100 text-amber-800 border-amber-300", text: "text-amber-700" };
  return { indicator: "bg-red-500", badge: "bg-red-100 text-red-800 border-red-300", text: "text-red-700" };
}

function qtLabel(qt: string) {
  const map: Record<string, string> = {
    MCQ: "MCQ",
    FILL_BLANKS: "Fill Blanks",
    SHORT_ANSWER: "Short Answer",
    LONG_ANSWER: "Long Answer",
  };
  return map[qt] ?? qt;
}

export function QuestionBreakdownCard({
  result,
  defaultOpen = false,
}: QuestionBreakdownCardProps) {
  const [open, setOpen] = useState(defaultOpen);
  const pct = result.total_marks > 0 ? (result.marks_awarded / result.total_marks) * 100 : 0;
  const col = scoreColour(pct);

  return (
    <Card className="border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      {/* Header — always visible */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full text-left px-5 py-4 flex items-center gap-4 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 rounded-t-lg"
        aria-expanded={open}
      >
        {/* Question number */}
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm font-bold text-gray-600">
          {result.question_number}
        </div>

        {/* Question preview */}
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-800 line-clamp-1">
            {result.question_text}
          </p>
          <div className="flex items-center gap-2 mt-1">
            <Badge variant="outline" className="text-xs py-0 px-1.5 border-gray-300 text-gray-500">
              {qtLabel(result.question_type)}
            </Badge>
            <span className="text-xs text-gray-400">{result.category}</span>
            {result.is_auto_graded && (
              <Badge variant="outline" className="text-xs py-0 px-1.5 border-violet-200 text-violet-600 bg-violet-50">
                <Zap className="h-2.5 w-2.5 mr-0.5" /> Auto-graded
              </Badge>
            )}
          </div>
        </div>

        {/* Score + expand icon */}
        <div className="flex items-center gap-3 flex-shrink-0">
          <div className="text-right">
            <p className={`text-lg font-bold ${col.text}`}>
              {result.marks_awarded}
              <span className="text-sm font-normal text-gray-400">/{result.total_marks}</span>
            </p>
            <p className="text-xs text-gray-400">{pct.toFixed(0)}%</p>
          </div>
          {open ? (
            <ChevronUp className="h-4 w-4 text-gray-400" />
          ) : (
            <ChevronDown className="h-4 w-4 text-gray-400" />
          )}
        </div>
      </button>

      {/* Score bar */}
      <Progress value={pct} className="h-1 rounded-none" indicatorClassName={col.indicator} />

      {/* Expanded detail */}
      {open && (
        <CardContent className="pt-5 pb-5 space-y-5 border-t border-gray-100">

          {/* Question */}
          <div>
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">Question</p>
            <p className="text-sm text-gray-800 leading-relaxed">{result.question_text}</p>
          </div>

          {/* Student Answer */}
          <div>
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">Your Answer</p>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
                {result.student_answer || <span className="italic text-gray-400">No answer provided</span>}
              </p>
            </div>
          </div>

          {/* Correct/Model Answer */}
          <div>
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5 flex items-center gap-1.5">
              <BookOpen className="h-3.5 w-3.5" />
              {result.is_auto_graded ? "Correct Answer" : "Model Answer"}
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-sm text-blue-800 leading-relaxed whitespace-pre-wrap">
                {(result.is_auto_graded ? result.correct_answer : result.model_answer) || "—"}
              </p>
            </div>
          </div>

          {/* Feedback */}
          <div>
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">Feedback</p>
            <p className="text-sm text-gray-700 leading-relaxed italic">{result.feedback}</p>
          </div>

          {/* Strengths & Improvements */}
          {(result.strengths.length > 0 || result.improvements.length > 0) && (
            <div className="grid gap-4 sm:grid-cols-2">
              {result.strengths.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-green-600 uppercase tracking-wide mb-2 flex items-center gap-1">
                    <CheckCircle2 className="h-3.5 w-3.5" /> Strengths
                  </p>
                  <ul className="space-y-1">
                    {result.strengths.map((s, i) => (
                      <li key={i} className="text-xs text-green-700 flex items-start gap-1.5">
                        <span className="text-green-400 mt-0.5 shrink-0">✓</span>
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {result.improvements.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-red-600 uppercase tracking-wide mb-2 flex items-center gap-1">
                    <XCircle className="h-3.5 w-3.5" /> To Improve
                  </p>
                  <ul className="space-y-1">
                    {result.improvements.map((imp, i) => (
                      <li key={i} className="text-xs text-red-700 flex items-start gap-1.5">
                        <span className="text-red-400 mt-0.5 shrink-0">•</span>
                        {imp}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Marks badge */}
          <div className="flex justify-end">
            <Badge className={`${col.badge} border text-sm font-bold px-4 py-1`}>
              {result.marks_awarded} / {result.total_marks} marks
            </Badge>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
