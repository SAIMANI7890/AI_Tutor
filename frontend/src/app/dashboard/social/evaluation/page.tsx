/**
 * Evaluation Page
 * Shows submitted tests with long answers for AI evaluation
 */

"use client";

import { useEffect, useState } from "react";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { SubmittedTestCard } from "@/components/evaluation/SubmittedTestCard";
import { EvaluationResultCard } from "@/components/evaluation/EvaluationResultCard";
import { EvaluationLoadingSkeleton } from "@/components/evaluation/EvaluationLoadingSkeleton";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft, History, AlertCircle, FileCheck, ClipboardCheck } from "lucide-react";
import { evaluateAnswer, getSubmittedTestsForEvaluation } from "@/lib/evaluation-api";
import type {
  EvaluationResponse,
  SubmittedTestForEvaluation,
} from "@/types/evaluation";
import Link from "next/link";

export default function EvaluationPage() {
  const [tests, setTests] = useState<SubmittedTestForEvaluation[]>([]);
  const [isLoadingTests, setIsLoadingTests] = useState(true);
  const [isEvaluating, setIsEvaluating] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<{
    testId: string;
    questionId: string;
  } | null>(null);

  // Load submitted tests on mount
  useEffect(() => {
    loadSubmittedTests();
  }, []);

  const loadSubmittedTests = async () => {
    try {
      setIsLoadingTests(true);
      setError(null);
      const response = await getSubmittedTestsForEvaluation();

      if (response.success) {
        setTests(response.data.tests);
      } else {
        setError(response.message || "Failed to load submitted tests");
      }
    } catch (err: any) {
      console.error("Error loading tests:", err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to load submitted tests"
      );
    } finally {
      setIsLoadingTests(false);
    }
  };

  const handleEvaluate = async (
    testId: string,
    questionId: string,
    questionSummary: string,
    studentAnswer: string
  ) => {
    const evaluatingKey = `${testId}-${questionId}`;
    setIsEvaluating(evaluatingKey);
    setError(null);
    setEvaluation(null);
    setCurrentQuestion({ testId, questionId });

    try {
      const response = await evaluateAnswer({
        question: questionSummary,
        student_answer: studentAnswer,
        test_id: testId,
        question_id: questionId,
        total_marks: 10, // Default to 10 marks for test evaluations
      });

      if (response.success) {
        setEvaluation(response.data);
        // Reload tests to update evaluation status
        await loadSubmittedTests();
      } else {
        setError(response.message || "Failed to evaluate answer");
      }
    } catch (err: any) {
      console.error("Evaluation error:", err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to evaluate answer. Please try again."
      );
    } finally {
      setIsEvaluating(null);
    }
  };

  const handleBackToTests = () => {
    setEvaluation(null);
    setCurrentQuestion(null);
    setError(null);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        <main className="container mx-auto px-4 py-8 max-w-6xl">
          {/* Page Header */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-green-100 p-2.5 rounded-xl">
                  <ClipboardCheck className="h-6 w-6 text-green-600" />
                </div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Answer Evaluation
                </h1>
              </div>
              <p className="text-gray-500 ml-14">
                Evaluate your submitted test answers and receive detailed AI feedback
              </p>
            </div>

            <Link href="/dashboard/social/evaluation/history" className="hidden sm:block">
              <Button variant="outline" className="gap-2">
                <History className="h-4 w-4" />
                View History
              </Button>
            </Link>
          </div>

          {/* Error Alert */}
          {error && !evaluation && (
            <Alert variant="destructive" className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Loading State */}
          {isLoadingTests && (
            <div className="space-y-4">
              <Skeleton className="h-48" />
              <Skeleton className="h-48" />
            </div>
          )}

          {/* Show Evaluation Result */}
          {evaluation && !isLoadingTests && (
            <div className="space-y-6">
              {/* Back Button */}
              <Button
                variant="outline"
                onClick={handleBackToTests}
                size="lg"
                className="w-full md:w-auto"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Tests
              </Button>

              {/* Results */}
              <EvaluationResultCard evaluation={evaluation} />

              {/* Action Buttons */}
              <div className="flex gap-3 justify-center flex-wrap">
                <Button variant="outline" onClick={handleBackToTests} size="lg">
                  Back to Tests
                </Button>
                <Link href="/dashboard/social/evaluation/history">
                  <Button variant="default" size="lg">
                    <History className="mr-2 h-4 w-4" />
                    View All Evaluations
                  </Button>
                </Link>
              </div>
            </div>
          )}

          {/* Show Evaluating State */}
          {isEvaluating && !evaluation && <EvaluationLoadingSkeleton />}

          {/* Show Submitted Tests */}
          {!evaluation && !isEvaluating && !isLoadingTests && (
            <>
              {tests.length === 0 ? (
                <Alert>
                  <FileCheck className="h-4 w-4" />
                  <AlertDescription>
                    <p className="font-medium mb-2">No submitted tests found</p>
                    <p className="text-sm text-muted-foreground">
                      Complete and submit a test with long answer questions from the
                      Examinations section to see them here for evaluation.
                    </p>
                  </AlertDescription>
                </Alert>
              ) : (
                <div className="space-y-6">
                  <p className="text-sm text-muted-foreground">
                    Showing {tests.length} submitted test{tests.length !== 1 ? "s" : ""} with
                    long answer questions
                  </p>
                  {tests.map((test) => (
                    <SubmittedTestCard
                      key={test.test_id}
                      test={test}
                      onEvaluate={handleEvaluate}
                      isEvaluating={isEvaluating}
                    />
                  ))}
                </div>
              )}
            </>
          )}

          {/* Mobile history link */}
          {!evaluation && (
            <div className="mt-6 text-center sm:hidden">
              <Link
                href="/dashboard/social/evaluation/history"
                className="text-sm text-blue-600 hover:underline flex items-center gap-1.5 mx-auto justify-center"
              >
                <History className="h-3.5 w-3.5" />
                View evaluation history
              </Link>
            </div>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}
