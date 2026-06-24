/**
 * StudyPlanForm Component
 * Form for creating a new study plan
 */

"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Checkbox } from "@/components/ui/checkbox";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CalendarIcon, Loader2, AlertCircle } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";
import { CHAPTERS, CATEGORIES } from "@/data/chapters";
import type { Chapter } from "@/types/study-plan";

interface StudyPlanFormProps {
  onSubmit: (examDate: Date, dailyHours: number, chapterIds: number[]) => void;
  isLoading: boolean;
  error: string | null;
}

export function StudyPlanForm({ onSubmit, isLoading, error }: StudyPlanFormProps) {
  const [examDate, setExamDate] = useState<Date>();
  const [dailyHours, setDailyHours] = useState<number>(3);
  const [selectedChapters, setSelectedChapters] = useState<number[]>([]);
  const [expandedCategories, setExpandedCategories] = useState<string[]>(["History"]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (examDate && dailyHours && selectedChapters.length > 0) {
      onSubmit(examDate, dailyHours, selectedChapters);
    }
  };

  const toggleChapter = (chapterId: number) => {
    setSelectedChapters((prev) =>
      prev.includes(chapterId)
        ? prev.filter((id) => id !== chapterId)
        : [...prev, chapterId]
    );
  };

  const toggleCategory = (category: string) => {
    const categoryChapters = CHAPTERS.filter((ch) => ch.category === category).map(
      (ch) => ch.chapter_id
    );
    const allSelected = categoryChapters.every((id) => selectedChapters.includes(id));

    if (allSelected) {
      setSelectedChapters((prev) => prev.filter((id) => !categoryChapters.includes(id)));
    } else {
      setSelectedChapters((prev) => [
        ...new Set([...prev, ...categoryChapters]),
      ]);
    }
  };

  const isCategoryExpanded = (category: string) => expandedCategories.includes(category);

  const toggleCategoryExpansion = (category: string) => {
    setExpandedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((c) => c !== category)
        : [...prev, category]
    );
  };

  const getCategoryChapters = (category: string): Chapter[] => {
    return CHAPTERS.filter((ch) => ch.category === category);
  };

  const isCategorySelected = (category: string): boolean => {
    const categoryChapters = getCategoryChapters(category);
    return categoryChapters.every((ch) => selectedChapters.includes(ch.chapter_id));
  };

  const isCategoryPartiallySelected = (category: string): boolean => {
    const categoryChapters = getCategoryChapters(category);
    const selectedCount = categoryChapters.filter((ch) =>
      selectedChapters.includes(ch.chapter_id)
    ).length;
    return selectedCount > 0 && selectedCount < categoryChapters.length;
  };

  const isFormValid =
    examDate && dailyHours >= 1 && dailyHours <= 24 && selectedChapters.length > 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Study Plan</CardTitle>
        <CardDescription>
          Generate a personalized study schedule based on your exam date and available time
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Error Alert */}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Exam Date */}
          <div className="space-y-2">
            <Label htmlFor="exam-date">Exam Date</Label>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  id="exam-date"
                  variant="outline"
                  className={cn(
                    "w-full justify-start text-left font-normal",
                    !examDate && "text-muted-foreground"
                  )}
                >
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {examDate ? format(examDate, "PPP") : "Select exam date"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={examDate}
                  onSelect={setExamDate}
                  disabled={(date) =>
                    date < new Date() || date < new Date(new Date().setHours(0, 0, 0, 0))
                  }
                />
              </PopoverContent>
            </Popover>
            <p className="text-sm text-gray-500">
              Select your target exam date (must be in the future)
            </p>
          </div>

          {/* Daily Study Hours */}
          <div className="space-y-2">
            <Label htmlFor="daily-hours">Daily Study Hours</Label>
            <Input
              id="daily-hours"
              type="number"
              min="1"
              max="24"
              step="0.5"
              value={Number.isNaN(dailyHours) ? "" : dailyHours}
              onChange={(e) => {
                const val = e.target.valueAsNumber;
                // Only update state with a valid number; ignore empty / NaN
                if (!Number.isNaN(val)) {
                  setDailyHours(val);
                } else {
                  setDailyHours(0); // reset to safe default while typing
                }
              }}
              placeholder="Enter hours per day"
            />
            <p className="text-sm text-gray-500">
              How many hours can you study per day? (1-24 hours)
            </p>
          </div>

          {/* Chapter Selection */}
          <div className="space-y-3">
            <Label>Select Chapters</Label>
            <p className="text-sm text-gray-500">
              Choose the chapters you want to include in your study plan
            </p>

            <div className="border rounded-lg p-4 max-h-96 overflow-y-auto space-y-4">
              {CATEGORIES.map((category) => {
                const chapters = getCategoryChapters(category);
                const isExpanded = isCategoryExpanded(category);
                const isSelected = isCategorySelected(category);
                const isPartial = isCategoryPartiallySelected(category);

                return (
                  <div key={category} className="space-y-2">
                    {/* Category Header */}
                    <div className="flex items-center gap-3 p-2 bg-gray-50 rounded-md">
                      <Checkbox
                        checked={isSelected}
                        onCheckedChange={() => toggleCategory(category)}
                        className={cn(isPartial && "opacity-50")}
                      />
                      <button
                        type="button"
                        onClick={() => toggleCategoryExpansion(category)}
                        className="flex-1 text-left font-semibold text-gray-900 hover:text-primary"
                      >
                        {category} ({chapters.length})
                      </button>
                      <span className="text-xs text-gray-500">
                        {chapters.filter((ch) => selectedChapters.includes(ch.chapter_id)).length}/
                        {chapters.length}
                      </span>
                    </div>

                    {/* Category Chapters */}
                    {isExpanded && (
                      <div className="ml-8 space-y-2">
                        {chapters.map((chapter) => (
                          <div
                            key={chapter.chapter_id}
                            className="flex items-start gap-3 p-2 hover:bg-gray-50 rounded-md"
                          >
                            <Checkbox
                              id={`chapter-${chapter.chapter_id}`}
                              checked={selectedChapters.includes(chapter.chapter_id)}
                              onCheckedChange={() => toggleChapter(chapter.chapter_id)}
                            />
                            <label
                              htmlFor={`chapter-${chapter.chapter_id}`}
                              className="flex-1 text-sm cursor-pointer"
                            >
                              <div className="font-medium text-gray-900">
                                {chapter.chapter_name}
                              </div>
                              <div className="text-xs text-gray-500 mt-0.5">
                                {chapter.difficulty} · {chapter.estimated_study_hours}h
                              </div>
                            </label>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            <div className="text-sm text-gray-600">
              Selected: {selectedChapters.length} chapter{selectedChapters.length !== 1 && "s"}
            </div>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            className="w-full"
            size="lg"
            disabled={!isFormValid || isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating with AI... (10-20s)
              </>
            ) : (
              "Generate Study Plan"
            )}
          </Button>
          
          {isLoading && (
            <p className="text-sm text-center text-gray-500">
              Please wait while our AI creates an optimized study schedule for you
            </p>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
