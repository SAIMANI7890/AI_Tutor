"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useExam } from "@/hooks/useExam";
import { useQuestionNavigation } from "@/hooks/useQuestionNavigation";
import { useSubmitExam } from "@/hooks/useSubmitExam";
import { ProgressBar } from "@/components/examination/ProgressBar";
import { SaveIndicator } from "@/components/examination/SaveIndicator";
import { QuestionNavigator } from "@/components/examination/QuestionNavigator";
import { QuestionRenderer } from "@/components/examination/QuestionRenderer";
import { SubmissionDialog } from "@/components/examination/SubmissionDialog";
import { ExamSkeletonLoader } from "@/components/examination/ExamSkeletonLoader";
import {
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
  Send,
  AlertCircle,
  CheckCircle2,
  LayoutDashboard,
  Clock,
  ArrowLeft,
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { QuestionType } from "@/lib/services/exam.service";
import { format, parseISO } from "date-fns";

// ─── helpers ─────────────────────────────────────────────────────────────────

function typeLabel(type: QuestionType) {
  const map: Record<QuestionType, string> = {
    MCQ: "Multiple Choice",
    FILL_BLANKS: "Fill in the Blanks",
    SHORT_ANSWER: "Short Answer",
    LONG_ANSWER: "Long Answer",
  };
  return map[type] ?? type;
}

// ─── page ────────────────────────────────────────────────────────────────────

export default function TestTakingPage() {
  const params = useParams();
  const router = useRouter();
  const testId = params.testId as string;

  const [navOpen, setNavOpen] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);

  const {
    questions,
    answers,
    currentIndex,
    currentQuestion,
    isLoading,
    error,
    saveStatus,
    answeredCount,
    examStatus,
    isReadOnly,
    setAnswer,
    goTo,
  } = useExam(testId);

  const { jumpTo, goNext, goPrev, isFirst, isLast } = useQuestionNavigation({
    total: questions.length,
    currentIndex,
    goTo,
  });

  const { submit, submitState, submitResult, submitError } = useSubmitExam(testId);

  // ── Success screen ────────────────────────────────────────────────────────

  if (submitState === "success" && submitResult) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-teal-50 flex flex-col">
          <DashboardHeader />
          <main className="flex-1 flex items-center justify-center p-6">
            <div className="max-w-md w-full text-center space-y-6">
              <div className="bg-emerald-100 p-5 rounded-full inline-flex items-center justify-center mx-auto">
                <CheckCircle2 className="h-16 w-16 text-emerald-600" />
              </div>

              <div>
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  Test Submitted! 🎉
                </h1>
                <p className="text-gray-500 text-sm">
                  Your answers have been recorded successfully.
                </p>
              </div>

              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-3 text-left">
                <h2 className="text-sm font-semibold text-gray-700 border-b pb-2">
                  Test Summary
                </h2>
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Questions answered</span>
                  <span className="font-semibold text-gray-800">
                    {submitResult.questions_answered} / {submitResult.total_questions}
                  </span>
                </div>
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Status</span>
                  <Badge variant="warning">Awaiting Evaluation</Badge>
                </div>
                {submitResult.completed_at && (
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Completed at</span>
                    <span className="font-medium text-gray-800">
                      {format(parseISO(submitResult.completed_at), "dd MMM yyyy, HH:mm")}
                    </span>
                  </div>
                )}
              </div>

              <div className="flex flex-col sm:flex-row gap-3">
                <Button
                  variant="outline"
                  className="flex-1 gap-2"
                  onClick={() => router.push("/dashboard/social/examination/history")}
                >
                  <Clock className="h-4 w-4" />
                  View Test History
                </Button>
                <Button
                  className="flex-1 gap-2 bg-blue-600 hover:bg-blue-700 text-white"
                  onClick={() => router.push("/dashboard")}
                >
                  <LayoutDashboard className="h-4 w-4" />
                  Return to Dashboard
                </Button>
              </div>
            </div>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  // ── Loading ───────────────────────────────────────────────────────────────

  if (isLoading) {
    return (
      <ProtectedRoute>
        <ExamSkeletonLoader />
      </ProtectedRoute>
    );
  }

  // ── Error ─────────────────────────────────────────────────────────────────

  if (error) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-rose-50 flex flex-col">
          <DashboardHeader />
          <main className="flex-1 flex items-center justify-center p-6">
            <div className="max-w-sm text-center space-y-5">
              <div className="bg-red-100 p-4 rounded-full inline-flex">
                <AlertCircle className="h-12 w-12 text-red-500" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-1">Something went wrong</h2>
                <p className="text-sm text-gray-500">{error}</p>
              </div>
              <Button
                variant="outline"
                onClick={() => router.push("/dashboard/social/examination")}
                className="gap-2"
              >
                <ArrowLeft className="h-4 w-4" />
                Back to Exams
              </Button>
            </div>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  // ── Main test-taking UI ───────────────────────────────────────────────────

  const firstQuestion = questions[0];
  const questionType = firstQuestion?.question_type;

  return (
    <ProtectedRoute>
      <div className="min-h-screen flex flex-col bg-gray-50">
        {/* ── Sticky Exam Header ──────────────────────────────────────────── */}
        <header className="sticky top-0 z-30 bg-white border-b shadow-sm">
          <div className="px-4 py-3 space-y-2.5">
            {/* Top row */}
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3 min-w-0">
                {/* Mobile nav toggle */}
                <button
                  className="lg:hidden p-1.5 rounded-md hover:bg-gray-100 transition-colors"
                  onClick={() => setNavOpen((p) => !p)}
                  aria-label={navOpen ? "Close question navigator" : "Open question navigator"}
                >
                  {navOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
                </button>
                <div className="min-w-0">
                  <h1 className="text-sm font-bold text-gray-900 truncate">
                    Social Studies Examination
                  </h1>
                  <div className="flex items-center gap-2">
                    {questionType && (
                      <p className="text-xs text-gray-500">{typeLabel(questionType)}</p>
                    )}
                    {isReadOnly && (
                      <Badge variant="warning" className="text-xs">View Only</Badge>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                {!isReadOnly && <SaveIndicator status={saveStatus} />}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => router.push("/dashboard/social/examination")}
                  className="hidden sm:flex gap-1.5 text-gray-500 text-xs"
                >
                  <ArrowLeft className="h-3.5 w-3.5" />
                  Exit
                </Button>
              </div>
            </div>

            {/* Progress bar */}
            <ProgressBar
              current={currentIndex + 1}
              total={questions.length}
            />
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden">
          {/* ── Navigator Sidebar (desktop always visible, mobile overlay) ── */}
          <>
            {/* Mobile overlay backdrop */}
            {navOpen && (
              <div
                className="fixed inset-0 z-20 bg-black/40 lg:hidden"
                onClick={() => setNavOpen(false)}
              />
            )}
            <aside
              className={cn(
                "border-r bg-white transition-all duration-300 overflow-y-auto",
                // Desktop: always visible
                "hidden lg:block lg:w-56 lg:flex-shrink-0",
                // Mobile: slide-in overlay
                navOpen && "!block fixed z-30 left-0 top-[89px] bottom-0 w-64 shadow-xl"
              )}
            >
              <QuestionNavigator
                total={questions.length}
                currentIndex={currentIndex}
                answers={answers}
                questionIds={questions.map((q) => q.id)}
                onJump={(idx) => {
                  goTo(idx);
                  setNavOpen(false);
                }}
              />
            </aside>
          </>

          {/* ── Main Question Area ───────────────────────────────────────── */}
          <main className="flex-1 overflow-y-auto">
            {currentQuestion ? (
              <div className="max-w-2xl mx-auto px-4 sm:px-6 py-8 space-y-8">
                {/* Read-only mode banner */}
                {isReadOnly && (
                  <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3">
                    <div className="flex items-start gap-3">
                      <AlertCircle className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="text-sm font-semibold text-amber-900 mb-1">
                          View Only Mode
                        </h3>
                        <p className="text-xs text-amber-800 leading-relaxed">
                          This exam has been submitted. You can review your answers but cannot make changes.
                          {examStatus === "EVALUATED" && " Your results are being processed."}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Question number pill + category */}
                <div className="flex items-center gap-3">
                  <span className="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                    Q{currentQuestion.question_number}
                  </span>
                  {currentQuestion.category && (
                    <span className="text-xs text-gray-400 font-medium uppercase tracking-wide">
                      {currentQuestion.category}
                    </span>
                  )}
                </div>

                {/* Question text */}
                <div className="bg-white rounded-2xl border border-gray-200 shadow-sm px-6 py-5">
                  <p className="text-gray-900 text-base leading-relaxed font-medium">
                    {currentQuestion.question_text}
                  </p>
                </div>

                {/* Answer input area */}
                <div className="space-y-2">
                  <h2 className="text-sm font-semibold text-gray-700">
                    {isReadOnly ? "Your Submitted Answer" : "Your Answer"}
                  </h2>
                  <QuestionRenderer
                    question={currentQuestion}
                    value={answers[currentQuestion.id] ?? ""}
                    onChange={(val) => setAnswer(currentQuestion.id, val)}
                    disabled={isReadOnly}
                  />
                </div>
              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center p-8">
                <p className="text-gray-400">No questions available.</p>
              </div>
            )}
          </main>
        </div>

        {/* ── Sticky Footer Nav ────────────────────────────────────────────── */}
        <footer className="sticky bottom-0 z-20 bg-white border-t shadow-sm px-4 py-3">
          <div className="max-w-2xl mx-auto flex items-center justify-between gap-3">
            <Button
              variant="outline"
              onClick={goPrev}
              disabled={isFirst}
              className="gap-1.5 min-w-[90px]"
              aria-label="Previous question"
            >
              <ChevronLeft className="h-4 w-4" />
              Previous
            </Button>

            {/* Submit button - only show if not read-only */}
            {!isReadOnly && (
              <Button
                onClick={() => setDialogOpen(true)}
                className="bg-emerald-600 hover:bg-emerald-700 text-white gap-1.5 px-5"
                id="submit-test-btn"
              >
                <Send className="h-4 w-4" />
                Submit Test
              </Button>
            )}

            {/* In read-only mode, show status badge instead */}
            {isReadOnly && (
              <Badge variant="warning" className="px-4 py-2">
                {examStatus === "SUBMITTED" ? "Submitted" : "Evaluated"}
              </Badge>
            )}

            <Button
              variant="outline"
              onClick={goNext}
              disabled={isLast}
              className="gap-1.5 min-w-[90px]"
              aria-label="Next question"
            >
              Next
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>

          {/* Submit error */}
          {submitError && !isReadOnly && (
            <p className="text-center text-xs text-red-500 mt-2">{submitError}</p>
          )}
        </footer>

        {/* ── Submission Dialog ─────────────────────────────────────────────── */}
        <SubmissionDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          onConfirm={submit}
          answeredCount={answeredCount}
          totalCount={questions.length}
        />
      </div>
    </ProtectedRoute>
  );
}
