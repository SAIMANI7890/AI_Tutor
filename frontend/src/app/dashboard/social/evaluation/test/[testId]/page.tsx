/**
 * Test Evaluation Page
 * Evaluates all questions in a submitted test and shows comprehensive results
 */

"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { 
  ArrowLeft, 
  CheckCircle2, 
  XCircle, 
  TrendingUp,
  TrendingDown,
  Lightbulb,
  Target,
  Award,
  Clock,
  AlertCircle,
  Loader2
} from "lucide-react";
import Link from "next/link";
import { api } from "@/lib/api";

interface QuestionResult {
  question_id: string;
  question_number: number;
  question_type: string;
  question_text: string;
  student_answer: string;
  correct_answer?: string;
  model_answer: string;
  marks_awarded: number;
  total_marks: number;
  feedback: string;
  strengths: string[];
  improvements: string[];
  category: string;
  is_auto_graded: boolean;
  evaluation_id: string;
}

interface TestEvaluationSummary {
  test_id: string;
  test_name: string;
  question_type: string;
  categories: string[];
  question_count: number;
  submitted_at: string;
  status: string;
  total_marks_awarded: number;
  total_marks_possible: number;
  percentage: number;
  performance_level: string;
  question_results: QuestionResult[];
  ai_insights: {
    strengths: string[];
    weak_areas: string[];
    recommendations: string[];
  };
  evaluated: boolean;
  evaluation_count: number;
}

export default function TestEvaluationPage() {
  const params = useParams();
  const router = useRouter();
  const testId = params?.testId as string;

  const [evaluation, setEvaluation] = useState<TestEvaluationSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (testId) {
      checkExistingEvaluation();
    }
  }, [testId]);

  const checkExistingEvaluation = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await api.get(`/evaluations/test/${testId}/results`);

      if (response.data.success && response.data.data.evaluated) {
        // Evaluation already exists
        setEvaluation(response.data.data);
        setIsLoading(false);
      } else {
        // No evaluation yet, start evaluating automatically
        await evaluateTest();
      }
    } catch (err: any) {
      console.error("Error checking evaluation:", err);
      // If 404 or no evaluation, try to evaluate
      if (err.response?.status === 404 || !err.response) {
        await evaluateTest();
      } else {
        setError(err.response?.data?.detail || "Failed to load evaluation");
        setIsLoading(false);
      }
    }
  };

  const evaluateTest = async () => {
    try {
      setIsEvaluating(true);
      setError(null);

      const response = await api.post(`/evaluations/test/${testId}/evaluate`);

      if (response.data.success) {
        setEvaluation(response.data.data);
      } else {
        setError(response.data.message || "Failed to evaluate test");
      }
    } catch (err: any) {
      console.error("Evaluation error:", err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to evaluate test. Please try again."
      );
    } finally {
      setIsEvaluating(false);
      setIsLoading(false);
    }
  };

  const getPerformanceColor = (level: string) => {
    switch (level) {
      case "Excellent":
        return "text-green-700 bg-green-100 border-green-200";
      case "Good":
        return "text-blue-700 bg-blue-100 border-blue-200";
      case "Average":
        return "text-yellow-700 bg-yellow-100 border-yellow-200";
      default:
        return "text-red-700 bg-red-100 border-red-200";
    }
  };

  const getMarksColor = (percentage: number) => {
    if (percentage >= 80) return "text-green-600";
    if (percentage >= 60) return "text-blue-600";
    if (percentage >= 40) return "text-yellow-600";
    return "text-red-600";
  };

  if (isLoading || isEvaluating) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
          <DashboardHeader />
          <SocialNav />

          <main className="container mx-auto px-4 py-8 max-w-6xl">
            <Card className="border-blue-200">
              <CardContent className="p-12">
                <div className="flex flex-col items-center justify-center text-center space-y-6">
                  <div className="bg-blue-100 p-4 rounded-full">
                    <Loader2 className="h-12 w-12 text-blue-600 animate-spin" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                      {isEvaluating ? "Evaluating Your Test..." : "Loading Evaluation..."}
                    </h2>
                    <p className="text-gray-500 max-w-md mx-auto">
                      {isEvaluating
                        ? "Our AI is analyzing your answers and generating detailed feedback. This may take 30-60 seconds."
                        : "Please wait while we load your evaluation results."}
                    </p>
                  </div>
                  <div className="space-y-3 w-full max-w-md">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-5/6 mx-auto" />
                    <Skeleton className="h-4 w-4/6 mx-auto" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  if (error) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
          <DashboardHeader />
          <SocialNav />

          <main className="container mx-auto px-4 py-8 max-w-6xl">
            <div className="mb-6">
              <Button
                variant="outline"
                onClick={() => router.push("/dashboard/social/examination/history")}
                size="lg"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to History
              </Button>
            </div>

            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                <p className="font-medium mb-2">{error}</p>
                <Button
                  variant="outline"
                  onClick={() => window.location.reload()}
                  className="mt-2"
                >
                  Try Again
                </Button>
              </AlertDescription>
            </Alert>
          </main>
        </div>
      </ProtectedRoute>
    );
  }

  if (!evaluation) {
    return null;
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        <main className="container mx-auto px-4 py-8 max-w-6xl space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <Button
              variant="outline"
              onClick={() => router.push("/dashboard/social/examination/history")}
              size="lg"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to History
            </Button>

            <Link href="/dashboard/social/evaluation/history">
              <Button variant="default" size="lg">
                View All Evaluations
              </Button>
            </Link>
          </div>

          {/* Overall Score Card */}
          <Card className="border-2 border-blue-200 shadow-lg">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl mb-1">{evaluation.test_name}</CardTitle>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {evaluation.categories.map((cat) => (
                      <Badge key={cat} variant="secondary">
                        {cat}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-2 mb-1">
                    <Award className="h-5 w-5 text-yellow-600" />
                    <Badge
                      className={`text-lg px-4 py-2 ${getPerformanceColor(
                        evaluation.performance_level
                      )}`}
                    >
                      {evaluation.performance_level}
                    </Badge>
                  </div>
                  <div className="text-sm text-gray-500 flex items-center gap-1 justify-end">
                    <Clock className="h-3.5 w-3.5" />
                    {new Date(evaluation.submitted_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </CardHeader>

            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Total Score */}
                <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl">
                  <div className={`text-5xl font-bold mb-2 ${getMarksColor(evaluation.percentage)}`}>
                    {evaluation.total_marks_awarded}
                    <span className="text-2xl text-gray-500">/{evaluation.total_marks_possible}</span>
                  </div>
                  <p className="text-sm font-medium text-gray-700">Total Score</p>
                </div>

                {/* Percentage */}
                <div className="text-center p-6 bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-xl">
                  <div className={`text-5xl font-bold mb-2 ${getMarksColor(evaluation.percentage)}`}>
                    {evaluation.percentage}%
                  </div>
                  <p className="text-sm font-medium text-gray-700">Percentage</p>
                </div>

                {/* Questions */}
                <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl">
                  <div className="text-5xl font-bold mb-2 text-purple-600">
                    {evaluation.question_count}
                  </div>
                  <p className="text-sm font-medium text-gray-700">Questions</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* AI Insights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Strengths */}
            <Card>
              <CardHeader className="bg-green-50">
                <CardTitle className="flex items-center gap-2 text-green-700">
                  <TrendingUp className="h-5 w-5" />
                  Strengths
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4">
                {evaluation.ai_insights.strengths.length > 0 ? (
                  <ul className="space-y-2">
                    {evaluation.ai_insights.strengths.map((strength, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <CheckCircle2 className="h-4 w-4 text-green-600 flex-shrink-0 mt-0.5" />
                        <span>{strength}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-500">Keep working to build your strengths!</p>
                )}
              </CardContent>
            </Card>

            {/* Weak Areas */}
            <Card>
              <CardHeader className="bg-red-50">
                <CardTitle className="flex items-center gap-2 text-red-700">
                  <TrendingDown className="h-5 w-5" />
                  Areas for Improvement
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4">
                {evaluation.ai_insights.weak_areas.length > 0 ? (
                  <ul className="space-y-2">
                    {evaluation.ai_insights.weak_areas.map((area, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <XCircle className="h-4 w-4 text-red-600 flex-shrink-0 mt-0.5" />
                        <span>{area}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-500">Great job! No major areas for improvement.</p>
                )}
              </CardContent>
            </Card>

            {/* Recommendations */}
            <Card>
              <CardHeader className="bg-blue-50">
                <CardTitle className="flex items-center gap-2 text-blue-700">
                  <Lightbulb className="h-5 w-5" />
                  Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4">
                <ul className="space-y-2">
                  {evaluation.ai_insights.recommendations.map((rec, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <Target className="h-4 w-4 text-blue-600 flex-shrink-0 mt-0.5" />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

          {/* Question-by-Question Results */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Question-by-Question Breakdown</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {evaluation.question_results.map((result, idx) => {
                const percentage = (result.marks_awarded / result.total_marks) * 100;

                return (
                  <div key={result.question_id}>
                    {idx > 0 && <Separator className="my-6" />}

                    <div className="space-y-4">
                      {/* Question Header */}
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <Badge variant="outline">Q{result.question_number}</Badge>
                            <Badge variant="secondary">{result.category}</Badge>
                            {result.is_auto_graded && (
                              <Badge variant="default" className="bg-purple-600">
                                Auto-graded
                              </Badge>
                            )}
                          </div>
                          <p className="font-medium text-gray-900">{result.question_text}</p>
                        </div>

                        <div className="text-right ml-4">
                          <div className={`text-2xl font-bold ${getMarksColor(percentage)}`}>
                            {result.marks_awarded}/{result.total_marks}
                          </div>
                          <p className="text-xs text-gray-500">marks</p>
                        </div>
                      </div>

                      {/* Student Answer */}
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <p className="text-sm font-semibold text-blue-900 mb-2">Your Answer:</p>
                        <p className="text-sm text-gray-700 whitespace-pre-wrap">
                          {result.student_answer || "No answer provided"}
                        </p>
                      </div>

                      {/* Model Answer */}
                      <div className="bg-green-50 p-4 rounded-lg">
                        <p className="text-sm font-semibold text-green-900 mb-2">
                          {result.is_auto_graded ? "Correct Answer:" : "Model Answer:"}
                        </p>
                        <p className="text-sm text-gray-700 whitespace-pre-wrap">
                          {result.model_answer}
                        </p>
                      </div>

                      {/* Feedback */}
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-semibold text-gray-900 mb-2">Feedback:</p>
                        <p className="text-sm text-gray-700">{result.feedback}</p>
                      </div>

                      {/* Strengths & Improvements */}
                      {(result.strengths.length > 0 || result.improvements.length > 0) && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {result.strengths.length > 0 && (
                            <div className="bg-green-50 p-4 rounded-lg">
                              <p className="text-sm font-semibold text-green-900 mb-2 flex items-center gap-1">
                                <CheckCircle2 className="h-4 w-4" />
                                Strengths:
                              </p>
                              <ul className="space-y-1">
                                {result.strengths.map((str, i) => (
                                  <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                                    <span className="text-green-600">•</span>
                                    <span>{str}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {result.improvements.length > 0 && (
                            <div className="bg-orange-50 p-4 rounded-lg">
                              <p className="text-sm font-semibold text-orange-900 mb-2 flex items-center gap-1">
                                <Target className="h-4 w-4" />
                                Improvements:
                              </p>
                              <ul className="space-y-1">
                                {result.improvements.map((imp, i) => (
                                  <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                                    <span className="text-orange-600">•</span>
                                    <span>{imp}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex gap-3 justify-center flex-wrap pb-8">
            <Button
              variant="outline"
              onClick={() => router.push("/dashboard/social/examination/history")}
              size="lg"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to History
            </Button>
            <Link href="/dashboard/social/examination">
              <Button variant="default" size="lg" className="bg-blue-600 hover:bg-blue-700">
                Take Another Test
              </Button>
            </Link>
            <Link href="/dashboard/social/evaluation/history">
              <Button variant="default" size="lg">
                View All Evaluations
              </Button>
            </Link>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
