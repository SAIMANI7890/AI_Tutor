/**
 * Test Evaluation Page
 * /dashboard/social/evaluation/[testId]
 *
 * States:
 *  loading        → skeleton while fetching existing results
 *  pre-evaluation → shows test info + question list + "Generate Evaluation" button
 *  evaluating     → animated overlay while AI runs
 *  results        → full score card + per-question breakdown + AI insights
 *  error          → error alert with retry
 */

"use client";

import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { TestInfoCard } from "@/components/evaluation/TestInfoCard";
import { TestScoreCard } from "@/components/evaluation/TestScoreCard";
import { AIInsightsCard } from "@/components/evaluation/AIInsightsCard";
import { QuestionBreakdownCard } from "@/components/evaluation/QuestionBreakdownCard";
import { EvaluationProgressOverlay } from "@/components/evaluation/EvaluationProgressOverlay";
import { useTestEvaluation } from "@/hooks/useTestEvaluation";
import {
  ArrowLeft,
  AlertCircle,
  Sparkles,
  History,
  ListChecks,
  RotateCcw,
  FileQuestion,
  MessageSquare,
  ChevronRight,
} from "lucide-react";

export default function TestEvaluationPage() {
  const params = useParams();
  const router = useRouter();
  const testId = params?.testId as string;

  const { pageState, summary, error, loadExistingResults, triggerEvaluation } =
    useTestEvaluation(testId);

  // Load existing results on mount
  useEffect(() => {
    if (testId) {
      loadExistingResults();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [testId]);

  // ── Loading skeleton ───────────────────────────────────────────────────────
  if (pageState === "loading") {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
          <DashboardHeader />
          <SocialNav />
          <main className="container mx-auto px-4 py-8 max-w-4xl space-y-6">
            <Skeleton className="h-8 w-40" />
            <Skeleton className="h-32 w-full rounded-xl" />
            <Skeleton className="h-6 w-48" />
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-20 w-full rounded-xl" />
            ))}
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  // ── Error state ────────────────────────────────────────────────────────────
  if (pageState === "error") {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
          <DashboardHeader />
          <SocialNav />
          <main className="container mx-auto px-4 py-8 max-w-4xl">
            <Alert variant="destructive" className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
            <div className="flex gap-3">
              <Button onClick={loadExistingResults} variant="outline" className="gap-1.5">
                <RotateCcw className="h-4 w-4" />
                Retry
              </Button>
              <Button onClick={() => router.push("/dashboard/social/examination/tests")} variant="ghost">
                Back to Tests
              </Button>
            </div>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        {/* AI evaluating overlay */}
        {pageState === "evaluating" && <EvaluationProgressOverlay />}

        <main className="container mx-auto px-4 py-8 max-w-4xl">

          {/* Back navigation */}
          <div className="mb-6">
            <Link href="/dashboard/social/examination/tests">
              <Button variant="ghost" size="sm" className="gap-1.5 text-gray-600 hover:text-gray-900">
                <ArrowLeft className="h-4 w-4" />
                Back to Submitted Tests
              </Button>
            </Link>
          </div>

          {/* ── PRE-EVALUATION VIEW ────────────────────────────────────────────── */}
          {pageState === "pre-evaluation" && (
            <div className="space-y-6">
              {/* Page title */}
              <div className="flex items-center gap-3">
                <div className="bg-purple-100 p-2.5 rounded-xl">
                  <Sparkles className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Evaluate Test</h1>
                  <p className="text-sm text-gray-500">
                    Generate an AI-powered evaluation report for this test
                  </p>
                </div>
              </div>

              {/* Info card placeholder (we don't have full detail yet) */}
              <Card className="border border-blue-100 bg-blue-50/50">
                <CardContent className="pt-4 pb-4">
                  <div className="flex items-start gap-3">
                    <FileQuestion className="h-5 w-5 text-blue-500 mt-0.5 shrink-0" />
                    <div>
                      <p className="text-sm font-medium text-blue-900">
                        Test ID: <span className="font-mono text-xs">{testId}</span>
                      </p>
                      <p className="text-sm text-blue-700 mt-1">
                        Click <strong>Generate Evaluation</strong> below to run AI analysis on all your answers.
                        MCQ and Fill-in-the-Blank questions are auto-graded instantly;
                        Short and Long Answer questions use AI + RAG.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* What to expect */}
              <Card className="border border-gray-200 bg-white shadow-sm">
                <CardContent className="pt-5 pb-5">
                  <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                    <ListChecks className="h-5 w-5 text-indigo-500" />
                    What you'll get
                  </h3>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {[
                      { emoji: "🎯", title: "Overall Score", desc: "Total marks and percentage" },
                      { emoji: "📊", title: "Performance Badge", desc: "Excellent / Good / Average / Needs Improvement" },
                      { emoji: "🔍", title: "Question Breakdown", desc: "Per-question feedback and model answers" },
                      { emoji: "🧠", title: "AI Insights", desc: "Strengths, weak areas, and study recommendations" },
                    ].map(({ emoji, title, desc }) => (
                      <div key={title} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                        <span className="text-xl">{emoji}</span>
                        <div>
                          <p className="text-sm font-medium text-gray-800">{title}</p>
                          <p className="text-xs text-gray-500">{desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Generate button */}
              <div className="flex flex-col sm:flex-row gap-3">
                <Button
                  onClick={triggerEvaluation}
                  disabled={pageState === "evaluating"}
                  className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold gap-2 py-6 text-base flex-1 sm:flex-none sm:px-10"
                  id="generate-evaluation-btn"
                >
                  <Sparkles className="h-5 w-5" />
                  Generate Evaluation
                </Button>
                <Button
                  variant="outline"
                  onClick={() => router.push("/dashboard/social/examination/tests")}
                  className="gap-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back to Tests
                </Button>
              </div>
            </div>
          )}

          {/* ── RESULTS VIEW ───────────────────────────────────────────────────── */}
          {pageState === "results" && summary && (
            <div className="space-y-6">
              {/* Page title */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="bg-green-100 p-2.5 rounded-xl">
                    <Sparkles className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold text-gray-900">Evaluation Report</h1>
                    <p className="text-sm text-gray-500">
                      {summary.evaluation_count} question{summary.evaluation_count !== 1 ? "s" : ""} evaluated
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => router.push("/dashboard/social/evaluation/history")}
                    className="gap-1.5"
                  >
                    <History className="h-4 w-4" />
                    History
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => router.push("/dashboard/social/examination")}
                    className="gap-1.5"
                  >
                    New Test
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Test Info Card */}
              <TestInfoCard
                testName={summary.test_name}
                categories={summary.categories}
                questionType={summary.question_type}
                questionCount={summary.question_count}
                submittedAt={summary.submitted_at}
                status={summary.status}
              />

              {/* Overall Score Card */}
              <TestScoreCard
                totalAwarded={summary.total_marks_awarded}
                totalPossible={summary.total_marks_possible}
                percentage={summary.percentage}
                performanceLevel={summary.performance_level}
                questionCount={summary.evaluation_count}
              />

              {/* AI Insights */}
              <AIInsightsCard insights={summary.ai_insights} />

              <Separator />

              {/* Question Breakdown */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <MessageSquare className="h-5 w-5 text-gray-500" />
                  Question-by-Question Breakdown
                  <Badge variant="outline" className="text-xs font-normal text-gray-500">
                    {summary.question_results.length} questions
                  </Badge>
                </h2>
                <div className="space-y-3">
                  {summary.question_results.map((result, idx) => (
                    <QuestionBreakdownCard
                      key={result.question_id}
                      result={result}
                      defaultOpen={idx === 0}
                    />
                  ))}
                </div>
              </div>

              {/* Bottom CTA */}
              <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-100 rounded-xl p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                  <p className="font-semibold text-indigo-900">
                    Want to improve your score?
                  </p>
                  <p className="text-sm text-indigo-600">
                    Review weak areas and take a new test to track your progress
                  </p>
                </div>
                <div className="flex gap-2 flex-shrink-0">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => router.push("/dashboard/social/evaluation/history")}
                    className="gap-1.5"
                  >
                    <History className="h-4 w-4" />
                    All Evaluations
                  </Button>
                  <Button
                    size="sm"
                    onClick={() => router.push("/dashboard/social/examination")}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white gap-1.5"
                  >
                    <Sparkles className="h-4 w-4" />
                    New Test
                  </Button>
                </div>
              </div>
            </div>
          )}

        </main>
      </div>
    </ProtectedRoute>
  );
}
