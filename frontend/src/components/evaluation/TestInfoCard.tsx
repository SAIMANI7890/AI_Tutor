/**
 * TestInfoCard – shows test metadata at top of evaluation page
 */
"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { BookOpen, Calendar, FileQuestion, Hash } from "lucide-react";
import { format, parseISO } from "date-fns";

interface TestInfoCardProps {
  testName: string;
  categories: string[];
  questionType: string;
  questionCount: number;
  submittedAt: string;
  status: string;
}

function fmtDate(iso: string) {
  try { return format(parseISO(iso), "dd MMM yyyy, h:mm a"); } catch { return iso; }
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
  MCQ: "bg-violet-100 text-violet-700 border-violet-200",
  FILL_BLANKS: "bg-amber-100 text-amber-700 border-amber-200",
  SHORT_ANSWER: "bg-teal-100 text-teal-700 border-teal-200",
  LONG_ANSWER: "bg-rose-100 text-rose-700 border-rose-200",
};

export function TestInfoCard({
  testName,
  categories,
  questionType,
  questionCount,
  submittedAt,
  status,
}: TestInfoCardProps) {
  return (
    <Card className="border border-gray-200 shadow-sm bg-white">
      <CardContent className="pt-5 pb-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h2 className="text-xl font-bold text-gray-900 mb-3 truncate">{testName}</h2>
            <div className="flex flex-wrap gap-2 mb-4">
              {categories.map((cat) => (
                <Badge
                  key={cat}
                  variant="outline"
                  className="bg-blue-50 text-blue-700 border-blue-200 font-medium"
                >
                  <BookOpen className="h-3 w-3 mr-1" />
                  {cat}
                </Badge>
              ))}
            </div>
            <div className="flex flex-wrap gap-4 text-sm text-gray-600">
              <span className="flex items-center gap-1.5">
                <FileQuestion className="h-4 w-4 text-gray-400" />
                <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold ${qtColour[questionType] ?? "bg-gray-100 text-gray-700 border-gray-200"}`}>
                  {qtLabel(questionType)}
                </span>
              </span>
              <span className="flex items-center gap-1.5">
                <Hash className="h-4 w-4 text-gray-400" />
                {questionCount} question{questionCount !== 1 ? "s" : ""}
              </span>
              <span className="flex items-center gap-1.5">
                <Calendar className="h-4 w-4 text-gray-400" />
                Submitted {fmtDate(submittedAt)}
              </span>
            </div>
          </div>
          <Badge
            variant="outline"
            className={status === "EVALUATED"
              ? "bg-green-50 text-green-700 border-green-200 self-start"
              : "bg-yellow-50 text-yellow-700 border-yellow-200 self-start"}
          >
            {status === "EVALUATED" ? "✓ Evaluated" : "Submitted"}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}
