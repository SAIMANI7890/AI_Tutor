/**
 * Examination Configuration Page
 * --------------------------------
 * Allows students to configure a new test.
 * After generation it redirects to /dashboard/social/examination/test/{testId}
 * so the dedicated test-taking page handles the full exam flow.
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { TestConfigurationForm } from "@/components/examination/test-configuration-form";
import { Button } from "@/components/ui/button";
import { examService } from "@/lib/services/exam.service";
import type { QuestionType } from "@/lib/services/exam.service";
import { History, FileText, ClipboardCheck } from "lucide-react";

export default function ExaminationPage() {
  const router = useRouter();
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateTest = async (data: {
    categories: string[];
    question_type: QuestionType;
    question_count: number;
  }) => {
    try {
      setIsGenerating(true);
      setError(null);

      // ── Sanitise every field before sending ───────────────────────────────
      // JSON.stringify serialises NaN as null → Pydantic 422. Guard it.
      const safeCount = Math.max(
        1,
        Math.min(10, Math.round(Number.isNaN(data.question_count) ? 5 : data.question_count))
      );
      const safeType: QuestionType = data.question_type ?? "MCQ";
      const safeCategories = Array.isArray(data.categories) ? data.categories : [];

      console.log("[exam] generating:", { categories: safeCategories, question_type: safeType, question_count: safeCount });

      const response = await examService.generate({
        categories: safeCategories,
        question_type: safeType,
        question_count: safeCount,
      });

      if (response.success && response.data?.test_id) {
        router.push(
          `/dashboard/social/examination/test/${response.data.test_id}`
        );
      } else {
        setError(response.message || "Failed to generate test. Please try again.");
      }
    } catch (err: any) {
      // Pydantic 422 returns detail as an array of error objects — parse it properly
      const detail = err?.response?.data?.detail;
      let errorMsg = "Failed to generate test. Please try again.";

      if (Array.isArray(detail)) {
        // e.g. [{loc: ["body","question_count"], msg: "..."}]
        errorMsg = detail
          .map((e: any) => {
            const field = Array.isArray(e.loc) ? e.loc.slice(1).join(".") : "field";
            return `${field}: ${e.msg}`;
          })
          .join(" | ");
      } else if (typeof detail === "string") {
        errorMsg = detail;
        
        // Special handling for "0 valid questions" error
        if (detail.includes("Could only generate 0 valid questions")) {
          errorMsg = 
            "⚠️ No textbook content found. The vector database needs to be populated first. " +
            "Please contact your administrator to run the ingestion script: " +
            "python app/rag/ingestion/ingest_all_local.py";
        }
      } else if (err?.response?.data?.message) {
        errorMsg = err.response.data.message;
      } else if (err?.message) {
        errorMsg = err.message;
      }

      console.error("❌ Exam generation failed:");
      console.error("Status:", err?.response?.status);
      console.error("Detail:", err?.response?.data?.detail);
      console.error("Full error:", err);
      
      setError(errorMsg);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        <main className="container mx-auto px-4 py-8 max-w-4xl">
          {/* Page Header */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-blue-100 p-2.5 rounded-xl">
                  <FileText className="h-6 w-6 text-blue-600" />
                </div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Examination
                </h1>
              </div>
              <p className="text-gray-500 ml-14">
                Generate a personalised AI-powered test from your textbook
              </p>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                onClick={() =>
                  router.push("/dashboard/social/examination/tests")
                }
                className="gap-2 hidden sm:flex"
                id="view-submitted-tests-btn"
              >
                <ClipboardCheck className="h-4 w-4" />
                Submitted Tests
              </Button>
              <Button
                variant="outline"
                onClick={() =>
                  router.push("/dashboard/social/examination/history")
                }
                className="gap-2 hidden sm:flex"
                id="view-history-btn"
              >
                <History className="h-4 w-4" />
                Test History
              </Button>
            </div>
          </div>

          {/* Configuration Form */}
          <TestConfigurationForm
            onSubmit={handleGenerateTest}
            isLoading={isGenerating}
            error={error}
          />

          {/* Mobile history link */}
          <div className="mt-4 text-center sm:hidden">
            <button
              onClick={() =>
                router.push("/dashboard/social/examination/history")
              }
              className="text-sm text-blue-600 hover:underline flex items-center gap-1.5 mx-auto"
            >
              <History className="h-3.5 w-3.5" />
              View test history
            </button>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
