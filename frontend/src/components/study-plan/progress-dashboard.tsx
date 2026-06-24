/**
 * Progress Dashboard Component
 * Displays comprehensive progress metrics for study plan
 */

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { CheckCircle2, Clock, XCircle, Target } from "lucide-react";

interface ProgressDashboardProps {
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
  skippedTasks: number;
  completionPercentage: number;
}

export function ProgressDashboard({
  totalTasks,
  completedTasks,
  pendingTasks,
  skippedTasks,
  completionPercentage,
}: ProgressDashboardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Progress Overview</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Overall Completion</span>
            <span className="font-semibold text-gray-900">
              {Math.round(completionPercentage)}%
            </span>
          </div>
          <Progress value={completionPercentage} className="h-3" />
          <p className="text-xs text-gray-500 text-center">
            {completedTasks} of {totalTasks} tasks completed
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {/* Total Tasks */}
          <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className="bg-gray-100 p-2 rounded-lg">
              <Target className="h-5 w-5 text-gray-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{totalTasks}</p>
              <p className="text-xs text-gray-600">Total</p>
            </div>
          </div>

          {/* Completed Tasks */}
          <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <div className="bg-green-100 p-2 rounded-lg">
              <CheckCircle2 className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-green-900">{completedTasks}</p>
              <p className="text-xs text-green-700">Completed</p>
            </div>
          </div>

          {/* Pending Tasks */}
          <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
            <div className="bg-blue-100 p-2 rounded-lg">
              <Clock className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-blue-900">{pendingTasks}</p>
              <p className="text-xs text-blue-700">Pending</p>
            </div>
          </div>

          {/* Skipped Tasks */}
          <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className="bg-gray-100 p-2 rounded-lg">
              <XCircle className="h-5 w-5 text-gray-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{skippedTasks}</p>
              <p className="text-xs text-gray-600">Skipped</p>
            </div>
          </div>
        </div>

        {/* Progress Message */}
        <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
          {completionPercentage === 100 ? (
            <p className="text-sm font-medium text-blue-900">
              🎉 Congratulations! You've completed your study plan!
            </p>
          ) : completionPercentage >= 75 ? (
            <p className="text-sm font-medium text-blue-900">
              🚀 Great progress! You're almost there!
            </p>
          ) : completionPercentage >= 50 ? (
            <p className="text-sm font-medium text-blue-900">
              💪 Keep going! You're halfway through!
            </p>
          ) : completionPercentage >= 25 ? (
            <p className="text-sm font-medium text-blue-900">
              📚 Good start! Keep up the momentum!
            </p>
          ) : (
            <p className="text-sm font-medium text-blue-900">
              🎯 Let's get started on your study journey!
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
