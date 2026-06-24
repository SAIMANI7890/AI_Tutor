"use client";

import { useRouter } from "next/navigation";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { SocialNav } from "@/components/layout/social-nav";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { HistoryTable } from "@/components/examination/HistoryTable";
import { HistorySkeletonLoader } from "@/components/examination/HistorySkeletonLoader";
import { useExamHistory, type StatusFilter, type TypeFilter } from "@/hooks/useExamHistory";
import {
  ArrowLeft,
  History,
  Plus,
  Search,
  RefreshCw,
  AlertCircle,
} from "lucide-react";

export default function TestHistoryPage() {
  const router = useRouter();

  const {
    exams,
    totalCount,
    isLoading,
    error,
    statusFilter,
    typeFilter,
    searchQuery,
    setStatusFilter,
    setTypeFilter,
    setSearchQuery,
    reload,
  } = useExamHistory();

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />
        <SocialNav />

        <main className="container mx-auto px-4 py-8 max-w-5xl">
          {/* ── Breadcrumb ── */}
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={() => router.push("/dashboard/social/examination")}
              className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-800 transition-colors"
              aria-label="Back to exam setup"
            >
              <ArrowLeft className="h-4 w-4" />
              Generate Test
            </button>

            <Button
              size="sm"
              onClick={() => router.push("/dashboard/social/examination")}
              className="bg-blue-600 hover:bg-blue-700 text-white gap-1.5"
              id="new-test-btn"
            >
              <Plus className="h-4 w-4" />
              New Test
            </Button>
          </div>

          {/* ── Page Header ── */}
          <div className="flex items-center gap-3 mb-8">
            <div className="bg-blue-100 p-2.5 rounded-xl">
              <History className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Test History</h1>
              <p className="text-sm text-gray-500">
                {totalCount > 0
                  ? `${totalCount} test${totalCount !== 1 ? "s" : ""} total — ${exams.length} shown`
                  : "Your examination records"}
              </p>
            </div>
          </div>

          {/* ── Filters ── */}
          <div className="flex flex-wrap gap-3 mb-6">
            {/* Status filter */}
            <Select
              value={statusFilter}
              onValueChange={(v) => setStatusFilter(v as StatusFilter)}
            >
              <SelectTrigger className="w-44 bg-white" aria-label="Filter by status">
                <SelectValue placeholder="All Statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Statuses</SelectItem>
                <SelectItem value="GENERATED">Not Started</SelectItem>
                <SelectItem value="IN_PROGRESS">In Progress</SelectItem>
                <SelectItem value="SUBMITTED">Submitted</SelectItem>
                <SelectItem value="EVALUATED">Evaluated</SelectItem>
              </SelectContent>
            </Select>

            {/* Type filter */}
            <Select
              value={typeFilter}
              onValueChange={(v) => setTypeFilter(v as TypeFilter)}
            >
              <SelectTrigger className="w-52 bg-white" aria-label="Filter by question type">
                <SelectValue placeholder="All Types" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">All Types</SelectItem>
                <SelectItem value="MCQ">Multiple Choice</SelectItem>
                <SelectItem value="FILL_BLANKS">Fill in the Blanks</SelectItem>
                <SelectItem value="SHORT_ANSWER">Short Answer</SelectItem>
                <SelectItem value="LONG_ANSWER">Long Answer</SelectItem>
              </SelectContent>
            </Select>

            {/* Search */}
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
              <Input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by test ID or category…"
                className="pl-9 bg-white"
                aria-label="Search tests"
              />
            </div>

            {/* Reload */}
            <Button
              variant="outline"
              size="icon"
              onClick={reload}
              aria-label="Refresh history"
              className="flex-shrink-0 bg-white"
            >
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>

          {/* ── Content ── */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
            {isLoading ? (
              <div className="p-5">
                <HistorySkeletonLoader />
              </div>
            ) : error ? (
              <div className="flex flex-col items-center justify-center py-16 text-center gap-4">
                <div className="bg-red-100 p-4 rounded-full">
                  <AlertCircle className="h-10 w-10 text-red-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-1">Failed to load history</h3>
                  <p className="text-sm text-gray-500">{error}</p>
                </div>
                <Button variant="outline" onClick={reload} className="gap-2">
                  <RefreshCw className="h-4 w-4" />
                  Try Again
                </Button>
              </div>
            ) : (
              <HistoryTable exams={exams} onDelete={(examId) => reload()} />
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
