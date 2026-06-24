/**
 * Study Planner Page
 * Main page for creating and viewing study plans
 */

"use client";

import { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { StudyPlanForm } from "@/components/study-plan/study-plan-form";
import { StudyPlanCard } from "@/components/study-plan/study-plan-card";
import { ProgressDashboard } from "@/components/study-plan/progress-dashboard";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  createStudyPlan,
  getStudyPlan,
  getStudyPlans,
  updateTaskStatus,
} from "@/lib/study-plan-api";
import type { StudyPlanDetail, StudyStatus } from "@/types/study-plan";
import { Calendar, Clock, Target, TrendingUp, RefreshCw } from "lucide-react";
import { format, differenceInDays } from "date-fns";
import { useRouter } from "next/navigation";

export default function StudyPlanPage() {
  const [currentPlan, setCurrentPlan] = useState<StudyPlanDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const router = useRouter();

  // Fetch existing study plan on mount
  useEffect(() => {
    fetchLatestPlan();
  }, []);

  const fetchLatestPlan = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Fetch all user's plans and get the latest one
      const response = await getStudyPlans();
      
      if (response.data.plans && response.data.plans.length > 0) {
        // Get the most recent plan (plans are ordered by creation date, newest first)
        const latestPlanSummary = response.data.plans[0];
        
        // Fetch full details of the latest plan
        const planDetailResponse = await getStudyPlan(latestPlanSummary.id);
        setCurrentPlan(planDetailResponse.data);
        setShowForm(false);
      } else {
        // No plans exist, show the form
        setShowForm(true);
        setCurrentPlan(null);
      }
    } catch (err: any) {
      // If any error occurs, show the form
      console.error("Failed to fetch study plan:", err);
      setShowForm(true);
      setCurrentPlan(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreatePlan = async (
    examDate: Date,
    dailyHours: number,
    chapterIds: number[]
  ) => {
    try {
      setIsCreating(true);
      setError(null);

      // Show progress message
      console.log("Generating study plan with AI...");

      const response = await createStudyPlan({
        exam_date: format(examDate, "yyyy-MM-dd"),
        daily_study_hours: dailyHours,
        selected_chapter_ids: chapterIds,
      });

      console.log("Study plan generated successfully");

      // Fetch the newly created plan
      const planResponse = await getStudyPlan(response.data.plan_id);
      setCurrentPlan(planResponse.data);
      setShowForm(false);
    } catch (err: any) {
      console.error("Failed to create study plan:", err);
      setError(
        err.response?.data?.detail ||
          err.response?.data?.message ||
          "Failed to generate study plan. Please try again."
      );
    } finally {
      setIsCreating(false);
    }
  };

  const handleStatusChange = async (itemId: number, newStatus: StudyStatus) => {
    if (!currentPlan) return;

    try {
      // Call the new task-based API endpoint
      const response = await updateTaskStatus(itemId, { status: newStatus });

      // Update local state with the response data
      setCurrentPlan((prev) => {
        if (!prev) return prev;

        const newCompletionPercentage = response.data.completion_percentage;
        const updatedItems = prev.items.map((item) =>
          item.id === itemId
            ? {
                ...item,
                status: newStatus,
                completed_at:
                  newStatus === "Completed"
                    ? response.data.completed_at || new Date().toISOString()
                    : null,
              }
            : item
        );

        // Recalculate counts
        const completed_items = updatedItems.filter((i) => i.status === "Completed").length;

        return {
          ...prev,
          items: updatedItems,
          completed_items,
          completion_percentage: newCompletionPercentage,
        };
      });
    } catch (err) {
      console.error("Failed to update status:", err);
      throw err; // Re-throw so StudyPlanCard can handle rollback
    }
  };

  const handleCreateNewPlan = () => {
    setShowForm(true);
    setCurrentPlan(null);
  };

  const daysUntilExam = currentPlan
    ? differenceInDays(new Date(currentPlan.exam_date), new Date())
    : 0;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        <main className="container mx-auto px-4 py-8 max-w-7xl">
          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Study Planner</h1>
            <p className="text-gray-600 mt-2">
              Create a personalized study schedule for your upcoming examination
            </p>
          </div>

          {isLoading ? (
            // Loading State
            <div className="space-y-6">
              <Skeleton className="h-64 w-full" />
              <Skeleton className="h-96 w-full" />
            </div>
          ) : showForm || !currentPlan ? (
            // Form State
            <div className="max-w-3xl mx-auto">
              <StudyPlanForm
                onSubmit={handleCreatePlan}
                isLoading={isCreating}
                error={error}
              />
            </div>
          ) : (
            // Display Study Plan
            <div className="space-y-6">
              {/* Stats Overview */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-3">
                      <div className="bg-blue-100 p-3 rounded-lg">
                        <Calendar className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Exam Date</p>
                        <p className="text-lg font-bold">
                          {format(new Date(currentPlan.exam_date), "MMM dd, yyyy")}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-3">
                      <div className="bg-purple-100 p-3 rounded-lg">
                        <Clock className="h-5 w-5 text-purple-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Days Remaining</p>
                        <p className="text-lg font-bold">{daysUntilExam} days</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-3">
                      <div className="bg-green-100 p-3 rounded-lg">
                        <Target className="h-5 w-5 text-green-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Daily Hours</p>
                        <p className="text-lg font-bold">
                          {currentPlan.daily_study_hours}h
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-3">
                      <div className="bg-orange-100 p-3 rounded-lg">
                        <TrendingUp className="h-5 w-5 text-orange-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Progress</p>
                        <p className="text-lg font-bold">
                          {Math.round(currentPlan.completion_percentage)}%
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Progress Bar */}
              <ProgressDashboard
                totalTasks={currentPlan.total_items}
                completedTasks={currentPlan.completed_items}
                pendingTasks={
                  currentPlan.items.filter((i) => i.status === "Pending").length
                }
                skippedTasks={
                  currentPlan.items.filter((i) => i.status === "Skipped").length
                }
                completionPercentage={currentPlan.completion_percentage}
              />

              {/* Action Buttons */}
              <div className="flex gap-3">
                <Button
                  onClick={handleCreateNewPlan}
                  variant="outline"
                  className="gap-2"
                >
                  <RefreshCw className="h-4 w-4" />
                  Create New Plan
                </Button>
              </div>

              {/* Study Plan Items */}
              <Card>
                <CardHeader>
                  <CardTitle>Your Study Schedule</CardTitle>
                  <CardDescription>
                    Follow your personalized study plan day by day
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {currentPlan.items.map((item) => (
                      <StudyPlanCard
                        key={item.id}
                        item={item}
                        onStatusChange={handleStatusChange}
                      />
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && !currentPlan && !showForm && (
            <Card className="max-w-2xl mx-auto">
              <CardContent className="pt-6 text-center py-12">
                <Calendar className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  No Study Plan Yet
                </h3>
                <p className="text-gray-600 mb-6">
                  Create your first study schedule to get started with organized learning
                </p>
                <Button onClick={() => setShowForm(true)} size="lg">
                  Create Study Plan
                </Button>
              </CardContent>
            </Card>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}
