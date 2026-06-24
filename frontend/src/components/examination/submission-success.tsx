/**
 * Submission Success Component
 * Displays success message and statistics after test submission
 */

"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  CheckCircle2,
  RefreshCw,
  Home,
  Clock,
  FileCheck,
  TrendingUp,
} from "lucide-react";
import { format } from "date-fns";

interface SubmissionSuccessProps {
  testId: string;
  totalQuestions: number;
  answeredQuestions: number;
  completedAt: string;
  onNewTest: () => void;
  onDashboard: () => void;
}

export function SubmissionSuccess({
  testId,
  totalQuestions,
  answeredQuestions,
  completedAt,
  onNewTest,
  onDashboard,
}: SubmissionSuccessProps) {
  const unansweredCount = totalQuestions - answeredQuestions;
  const completionPercentage = (answeredQuestions / totalQuestions) * 100;

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Success Header */}
      <Card className="border-green-200 bg-gradient-to-br from-green-50 to-white">
        <CardContent className="pt-12 pb-8 text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-100 mb-4">
            <CheckCircle2 className="h-12 w-12 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Test Submitted Successfully!
          </h1>
          <p className="text-lg text-gray-600 mb-6">
            Your answers have been saved and your test has been submitted for evaluation.
          </p>
          <Badge variant="secondary" className="text-sm px-4 py-2">
            <FileCheck className="h-4 w-4 mr-2" />
            Test ID: {testId.substring(0, 8)}...
          </Badge>
        </CardContent>
      </Card>

      {/* Statistics Card */}
      <Card>
        <CardContent className="pt-6 space-y-6">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="h-5 w-5 text-primary" />
            <h2 className="text-xl font-semibold">Submission Summary</h2>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-700 mb-1">Total Questions</p>
              <p className="text-3xl font-bold text-blue-900">{totalQuestions}</p>
            </div>

            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-700 mb-1">Answered</p>
              <p className="text-3xl font-bold text-green-900">{answeredQuestions}</p>
            </div>

            {unansweredCount > 0 && (
              <div className="col-span-2 p-4 bg-orange-50 border border-orange-200 rounded-lg">
                <p className="text-sm text-orange-700 mb-1">Unanswered Questions</p>
                <p className="text-3xl font-bold text-orange-900">{unansweredCount}</p>
                <p className="text-xs text-orange-600 mt-1">
                  These will be marked as incorrect during evaluation
                </p>
              </div>
            )}

            <div className="col-span-2 p-4 bg-purple-50 border border-purple-200 rounded-lg">
              <p className="text-sm text-purple-700 mb-2">Completion Rate</p>
              <div className="flex items-end gap-2">
                <p className="text-4xl font-bold text-purple-900">
                  {Math.round(completionPercentage)}%
                </p>
                <p className="text-sm text-purple-600 mb-1">completed</p>
              </div>
              <div className="mt-3 h-2 bg-purple-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-purple-600 transition-all duration-300"
                  style={{ width: `${completionPercentage}%` }}
                />
              </div>
            </div>
          </div>

          {/* Submission Time */}
          <div className="flex items-center justify-center gap-2 p-3 bg-gray-50 rounded-lg text-sm text-gray-700">
            <Clock className="h-4 w-4" />
            <span>
              Submitted on {format(new Date(completedAt), "MMMM dd, yyyy 'at' hh:mm a")}
            </span>
          </div>

          {/* What's Next */}
          <div className="pt-4 border-t">
            <h3 className="font-semibold mb-3 text-gray-900">What happens next?</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>Your answers have been securely stored in our database</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>Your test has been queued for AI-powered evaluation</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>You'll be able to view your results once evaluation is complete</span>
              </li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3">
        <Button onClick={onNewTest} size="lg" className="flex-1">
          <RefreshCw className="mr-2 h-4 w-4" />
          Take Another Test
        </Button>
        <Button onClick={onDashboard} variant="outline" size="lg" className="flex-1">
          <Home className="mr-2 h-4 w-4" />
          Back to Dashboard
        </Button>
      </div>
    </div>
  );
}
