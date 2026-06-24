/**
 * SubmittedTestsGrid – Grid of cards for SUBMITTED and EVALUATED tests
 */
"use client";

import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Eye,
  Sparkles,
  BookOpen,
  Calendar,
  Hash,
  CheckCircle2,
  ClipboardCheck,
  FileQuestion,
} from "lucide-react";
import { format, parseISO } from "date-fns";
import type { SubmittedTestSummary } from "@/types/evaluation";

interface SubmittedTestsGridProps {
  tests: SubmittedTestSummary[];
}

function fmtDate(iso: string | null) {
  if (!iso) return "—";
  try { return format(parseISO(iso), "dd MMM yyyy"); } catch { return "—"; }
}

function qtLabel(qt: string) {
  const map: Record<string, string> = {
    MCQ: "Multiple Choice",
    FILL_BLANKS: "Fill in the Blanks",
    SHORT_ANSWER: "Short Answer",
    LONG_ANSWER: "Long Answer",
  };
  return map[qt] ?? qt;
}

const qtColour: Record<string, string> = {
  MCQ: "bg-violet-100 text-violet-700",
  FILL_BLANKS: "bg-amber-100 text-amber-700",
  SHORT_ANSWER: "bg-teal-100 text-teal-700",
  LONG_ANSWER: "bg-rose-100 text-rose-700",
};

export function SubmittedTestsGrid({ tests }: SubmittedTestsGridProps) {
  const router = useRouter();

  if (tests.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <div className="bg-blue-50 p-6 rounded-full mb-4">
          <ClipboardCheck className="h-14 w-14 text-blue-400" />
        </div>
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          No submitted tests yet
        </h3>
        <p className="text-gray-500 text-sm max-w-xs leading-relaxed mb-6">
          Complete and submit a practice test to see it here for AI evaluation.
        </p>
        <Button
          onClick={() => router.push("/dashboard/social/examination")}
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          Generate a Test
        </Button>
      </div>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {tests.map((test) => {
        const isEvaluated = test.status === "EVALUATED";

        return (
          <Card
            key={test.id}
            className="hover:shadow-md transition-all duration-200 border border-gray-200"
          >
            <CardContent className="pt-5 pb-4">
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className={`p-2 rounded-lg ${qtColour[test.question_type] ?? "bg-gray-100 text-gray-500"}`}>
                  <FileQuestion className="h-5 w-5" />
                </div>
                {isEvaluated ? (
                  <Badge className="bg-green-100 text-green-800 border border-green-200 text-xs">
                    <CheckCircle2 className="h-3 w-3 mr-1" />
                    Evaluated
                  </Badge>
                ) : (
                  <Badge className="bg-yellow-100 text-yellow-800 border border-yellow-200 text-xs">
                    Submitted
                  </Badge>
                )}
              </div>

              {/* Title */}
              <p className="font-semibold text-gray-900 text-sm mb-1">
                {qtLabel(test.question_type)} Test
              </p>

              {/* Categories */}
              <div className="flex flex-wrap gap-1 mb-3">
                {test.selected_categories.map((cat) => (
                  <span
                    key={cat}
                    className="inline-flex items-center gap-0.5 px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs font-medium"
                  >
                    <BookOpen className="h-2.5 w-2.5" />
                    {cat}
                  </span>
                ))}
              </div>

              {/* Meta */}
              <div className="flex items-center gap-3 text-xs text-gray-500 mb-4">
                <span className="flex items-center gap-1">
                  <Hash className="h-3 w-3" />
                  {test.question_count}q
                </span>
                <span className="flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {fmtDate(test.completed_at)}
                </span>
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  className="flex-1 gap-1.5 text-xs"
                  onClick={() =>
                    router.push(`/dashboard/social/examination/test/${test.id}`)
                  }
                >
                  <Eye className="h-3.5 w-3.5" />
                  View Test
                </Button>
                <Button
                  size="sm"
                  className={`flex-1 gap-1.5 text-xs ${
                    isEvaluated
                      ? "bg-indigo-600 hover:bg-indigo-700"
                      : "bg-purple-600 hover:bg-purple-700"
                  } text-white`}
                  onClick={() =>
                    router.push(`/dashboard/social/evaluation/${test.id}`)
                  }
                >
                  <Sparkles className="h-3.5 w-3.5" />
                  {isEvaluated ? "View Results" : "Evaluate"}
                </Button>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
