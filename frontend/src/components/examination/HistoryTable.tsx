"use client";

import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { ExamSummary, TestStatus, QuestionType } from "@/lib/services/exam.service";
import { examService } from "@/lib/services/exam.service";
import { BookOpen, Play, Eye, FileQuestion, Calendar, Trash2, Check, AlertCircle, Sparkles } from "lucide-react";
import { format, parseISO } from "date-fns";
import { useState } from "react";

// ─── helpers ────────────────────────────────────────────────────────────────

function statusBadge(status: TestStatus) {
  const map: Record<TestStatus, { label: string; variant: "success" | "info" | "warning" | "muted" }> = {
    GENERATED: { label: "Not Started", variant: "muted" },
    IN_PROGRESS: { label: "In Progress", variant: "info" },
    SUBMITTED: { label: "Submitted", variant: "warning" },
    EVALUATED: { label: "Evaluated", variant: "success" },
  };
  const { label, variant } = map[status] ?? { label: status, variant: "muted" };
  return <Badge variant={variant}>{label}</Badge>;
}

function typeLabel(type: QuestionType) {
  const map: Record<QuestionType, string> = {
    MCQ: "Multiple Choice",
    FILL_BLANKS: "Fill in the Blanks",
    SHORT_ANSWER: "Short Answer",
    LONG_ANSWER: "Long Answer",
  };
  return map[type] ?? type;
}

function typeIcon(type: QuestionType) {
  const colours: Record<QuestionType, string> = {
    MCQ: "bg-violet-100 text-violet-600",
    FILL_BLANKS: "bg-amber-100 text-amber-600",
    SHORT_ANSWER: "bg-teal-100 text-teal-600",
    LONG_ANSWER: "bg-rose-100 text-rose-600",
  };
  return (
    <div className={`p-2 rounded-lg ${colours[type] ?? "bg-gray-100 text-gray-500"}`}>
      <FileQuestion className="h-5 w-5" />
    </div>
  );
}

function fmtDate(iso: string | null) {
  if (!iso) return "—";
  try { return format(parseISO(iso), "dd MMM yyyy"); } catch { return "—"; }
}

// ─── component ──────────────────────────────────────────────────────────────

interface HistoryTableProps {
  exams: ExamSummary[];
  onDelete?: (examId: string) => void;
}

export function HistoryTable({ exams, onDelete }: HistoryTableProps) {
  const router = useRouter();
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleDelete = async (examId: string, examType: string) => {
    if (!confirm(`Are you sure you want to delete this ${examType} exam? This action cannot be undone.`)) {
      return;
    }

    setDeletingId(examId);
    setSuccessMessage(null);
    setErrorMessage(null);

    try {
      await examService.delete(examId);
      setSuccessMessage("Exam deleted successfully");
      if (onDelete) {
        onDelete(examId);
      }
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || "Failed to delete the exam. Please try again.";
      setErrorMessage(errorMsg);
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setDeletingId(null);
    }
  };

  if (exams.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <div className="bg-blue-50 p-6 rounded-full mb-4">
          <BookOpen className="h-14 w-14 text-blue-400" />
        </div>
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          No exams yet
        </h3>
        <p className="text-gray-500 text-sm max-w-xs leading-relaxed mb-6">
          You haven&apos;t taken any exams yet. Generate your first practice test to get started.
        </p>
        <Button
          onClick={() => router.push("/dashboard/social/examination")}
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          Generate Your First Test
        </Button>
      </div>
    );
  }

  return (
    <>
      {/* Success/Error Alerts */}
      {successMessage && (
        <Alert className="mb-4 bg-green-50 border-green-200">
          <Check className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-900">
            {successMessage}
          </AlertDescription>
        </Alert>
      )}

      {errorMessage && (
        <Alert variant="destructive" className="mb-4">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            {errorMessage}
          </AlertDescription>
        </Alert>
      )}

      {/* Desktop table */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b bg-gray-50 text-left">
              <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Type</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Categories</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Questions</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Created</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Completed</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {exams.map((exam) => (
              <tr
                key={exam.id}
                className="bg-white hover:bg-gray-50 transition-colors"
              >
                <td className="px-4 py-4">
                  <div className="flex items-center gap-2.5">
                    {typeIcon(exam.question_type)}
                    <span className="font-medium text-gray-800">
                      {typeLabel(exam.question_type)}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-4">
                  <div className="flex flex-wrap gap-1">
                    {exam.selected_categories.map((cat) => (
                      <span
                        key={cat}
                        className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs font-medium"
                      >
                        {cat}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="px-4 py-4 text-gray-600">{exam.question_count}</td>
                <td className="px-4 py-4">
                  <div className="flex items-center gap-1.5 text-gray-500">
                    <Calendar className="h-3.5 w-3.5" />
                    {fmtDate(exam.created_at)}
                  </div>
                </td>
                <td className="px-4 py-4 text-gray-500">{fmtDate(exam.completed_at)}</td>
                <td className="px-4 py-4">{statusBadge(exam.status)}</td>
                <td className="px-4 py-4">
                  <div className="flex items-center gap-2">
                    <ActionButton exam={exam} router={router} />
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => handleDelete(exam.id, typeLabel(exam.question_type))}
                      disabled={deletingId === exam.id}
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile card list */}
      <div className="md:hidden space-y-3">
        {exams.map((exam) => (
          <div
            key={exam.id}
            className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2.5">
                {typeIcon(exam.question_type)}
                <div>
                  <p className="font-semibold text-gray-800 text-sm">
                    {typeLabel(exam.question_type)}
                  </p>
                  <p className="text-xs text-gray-500">
                    {exam.question_count} questions
                  </p>
                </div>
              </div>
              {statusBadge(exam.status)}
            </div>

            <div className="flex flex-wrap gap-1 mb-3">
              {exam.selected_categories.map((cat) => (
                <span
                  key={cat}
                  className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs font-medium"
                >
                  {cat}
                </span>
              ))}
            </div>

            <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
              <span>Created: {fmtDate(exam.created_at)}</span>
              {exam.completed_at && <span>Done: {fmtDate(exam.completed_at)}</span>}
            </div>

            <div className="flex items-center gap-2">
              <ActionButton exam={exam} router={router} fullWidth />
              <Button
                size="sm"
                variant="ghost"
                onClick={() => handleDelete(exam.id, typeLabel(exam.question_type))}
                disabled={deletingId === exam.id}
                className="text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

// ─── Action button (resume / start / view / evaluate) ──────────────────────

function ActionButton({
  exam,
  router,
  fullWidth = false,
}: {
  exam: ExamSummary;
  router: ReturnType<typeof useRouter>;
  fullWidth?: boolean;
}) {
  const cls = fullWidth ? "w-full" : "";

  if (exam.status === "IN_PROGRESS") {
    return (
      <Button
        size="sm"
        onClick={() => router.push(`/dashboard/social/examination/test/${exam.id}`)}
        className={`bg-blue-600 hover:bg-blue-700 text-white gap-1.5 ${cls}`}
      >
        <Play className="h-3.5 w-3.5" />
        Resume
      </Button>
    );
  }

  if (exam.status === "GENERATED") {
    return (
      <Button
        size="sm"
        onClick={() => router.push(`/dashboard/social/examination/test/${exam.id}`)}
        className={`bg-emerald-600 hover:bg-emerald-700 text-white gap-1.5 ${cls}`}
      >
        <Play className="h-3.5 w-3.5" />
        Start
      </Button>
    );
  }

  if (exam.status === "SUBMITTED") {
    return (
      <div className={`flex items-center gap-1.5 ${fullWidth ? "flex-col w-full" : ""}`}>
        <Button
          size="sm"
          variant="outline"
          onClick={() => router.push(`/dashboard/social/examination/test/${exam.id}`)}
          className={`gap-1 ${fullWidth ? "w-full" : ""}`}
        >
          <Eye className="h-3.5 w-3.5" />
          View
        </Button>
        <Button
          size="sm"
          onClick={() => router.push(`/dashboard/social/evaluation/${exam.id}`)}
          className={`bg-purple-600 hover:bg-purple-700 text-white gap-1 ${fullWidth ? "w-full" : ""}`}
        >
          <Sparkles className="h-3.5 w-3.5" />
          Evaluate
        </Button>
      </div>
    );
  }

  if (exam.status === "EVALUATED") {
    return (
      <Button
        size="sm"
        onClick={() => router.push(`/dashboard/social/evaluation/${exam.id}`)}
        className={`bg-green-600 hover:bg-green-700 text-white gap-1.5 ${cls}`}
      >
        <Sparkles className="h-3.5 w-3.5" />
        View Results
      </Button>
    );
  }

  return null;
}
