/**
 * Submitted Tests Page
 * /dashboard/social/examination/tests
 * Shows all SUBMITTED and EVALUATED tests ready for AI evaluation
 */

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { SubmittedTestsGrid } from "@/components/evaluation/SubmittedTestsGrid";
import { getSubmittedTests } from "@/lib/evaluation-api";
import type { SubmittedTestSummary } from "@/types/evaluation";
import {
  ArrowLeft,
  AlertCircle,
  ClipboardCheck,
  CheckCircle2,
  Clock,
  RefreshCw,
} from "lucide-react";

export default function SubmittedTestsPage() {
  const router = useRouter();
  const [tests, setTests] = useState<SubmittedTestSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const res = await getSubmittedTests();
      if (res.success) {
        setTests(res.data.tests);
      } else {
        setError(res.message || "Failed to load submitted tests");
      }
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          err?.message ||
          "Failed to load submitted tests"
      );
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const submittedCount = tests.filter((t) => t.status === "SUBMITTED").length;
  const evaluatedCount = tests.filter((t) => t.status === "EVALUATED").length;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        <main className="container mx-auto px-4 py-8 max-w-7xl">

          {/* Page Header */}
          <div className="mb-8">
            <div className="flex items-center gap-4 mb-4">
              <Link href="/dashboard/social/examination">
                <Button variant="ghost" size="sm" className="gap-1.5">
                  <ArrowLeft className="h-4 w-4" />
                  Back to Examination
                </Button>
              </Link>
            </div>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <div className="bg-purple-100 p-2.5 rounded-xl">
                    <ClipboardCheck className="h-6 w-6 text-purple-600" />
                  </div>
                  <h1 className="text-3xl font-bold text-gray-900">
                    Submitted Tests
                  </h1>
                </div>
                <p className="text-gray-500 ml-14">
                  Select a test to generate your AI-powered evaluation report
                </p>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={load}
                disabled={isLoading}
                className="gap-1.5 self-start sm:self-auto"
              >
                <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
                Refresh
              </Button>
            </div>
          </div>

          {/* Stats */}
          {!isLoading && !error && tests.length > 0 && (
            <div className="grid gap-4 grid-cols-2 sm:grid-cols-3 mb-8">
              <div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
                <p className="text-2xl font-bold text-gray-900">{tests.length}</p>
                <p className="text-sm text-gray-500 flex items-center gap-1 mt-1">
                  <ClipboardCheck className="h-3.5 w-3.5" /> Total Tests
                </p>
              </div>
              <div className="bg-white rounded-xl border border-yellow-200 p-4 shadow-sm">
                <p className="text-2xl font-bold text-yellow-700">{submittedCount}</p>
                <p className="text-sm text-yellow-600 flex items-center gap-1 mt-1">
                  <Clock className="h-3.5 w-3.5" /> Awaiting Evaluation
                </p>
              </div>
              <div className="bg-white rounded-xl border border-green-200 p-4 shadow-sm col-span-2 sm:col-span-1">
                <p className="text-2xl font-bold text-green-700">{evaluatedCount}</p>
                <p className="text-sm text-green-600 flex items-center gap-1 mt-1">
                  <CheckCircle2 className="h-3.5 w-3.5" /> Evaluated
                </p>
              </div>
            </div>
          )}

          {/* Loading skeleton */}
          {isLoading && (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
                  <div className="flex justify-between">
                    <Skeleton className="h-9 w-9 rounded-lg" />
                    <Skeleton className="h-5 w-20 rounded-full" />
                  </div>
                  <Skeleton className="h-4 w-3/4" />
                  <div className="flex gap-1">
                    <Skeleton className="h-5 w-16 rounded" />
                    <Skeleton className="h-5 w-20 rounded" />
                  </div>
                  <Skeleton className="h-3 w-1/2" />
                  <div className="flex gap-2 pt-1">
                    <Skeleton className="h-8 flex-1 rounded-md" />
                    <Skeleton className="h-8 flex-1 rounded-md" />
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Error */}
          {!isLoading && error && (
            <Alert variant="destructive" className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription className="flex items-center justify-between">
                <span>{error}</span>
                <Button size="sm" variant="outline" onClick={load} className="ml-4">
                  Retry
                </Button>
              </AlertDescription>
            </Alert>
          )}

          {/* Tests grid */}
          {!isLoading && !error && <SubmittedTestsGrid tests={tests} />}

        </main>
      </div>
    </ProtectedRoute>
  );
}
