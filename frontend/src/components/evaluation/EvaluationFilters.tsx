/**
 * Evaluation Filters Component
 * Search, filter, and sort evaluations
 */

"use client";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { Search, Filter, ArrowUpDown } from "lucide-react";
import type { EvaluationFilters as Filters } from "@/types/evaluation";

interface EvaluationFiltersProps {
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
  chapters: string[];
}

export function EvaluationFilters({
  filters,
  onFiltersChange,
  chapters,
}: EvaluationFiltersProps) {
  const handleSearchChange = (value: string) => {
    onFiltersChange({ ...filters, searchQuery: value });
  };

  const handleChapterChange = (value: string) => {
    onFiltersChange({ ...filters, chapter: value });
  };

  const handleScoreRangeChange = (value: string) => {
    onFiltersChange({ ...filters, scoreRange: value });
  };

  const handleSortChange = (value: string) => {
    onFiltersChange({
      ...filters,
      sortBy: value as Filters["sortBy"],
    });
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {/* Search */}
          <div className="space-y-2">
            <Label htmlFor="search" className="flex items-center gap-2">
              <Search className="w-4 h-4" />
              Search Question
            </Label>
            <Input
              id="search"
              placeholder="Search..."
              value={filters.searchQuery}
              onChange={(e) => handleSearchChange(e.target.value)}
            />
          </div>

          {/* Chapter Filter */}
          <div className="space-y-2">
            <Label htmlFor="chapter" className="flex items-center gap-2">
              <Filter className="w-4 h-4" />
              Chapter
            </Label>
            <Select value={filters.chapter} onValueChange={handleChapterChange}>
              <SelectTrigger id="chapter">
                <SelectValue placeholder="All Chapters" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Chapters</SelectItem>
                {chapters.map((chapter) => (
                  <SelectItem key={chapter} value={chapter}>
                    {chapter}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Score Range Filter */}
          <div className="space-y-2">
            <Label htmlFor="score" className="flex items-center gap-2">
              <Filter className="w-4 h-4" />
              Score Range
            </Label>
            <Select
              value={filters.scoreRange}
              onValueChange={handleScoreRangeChange}
            >
              <SelectTrigger id="score">
                <SelectValue placeholder="All Scores" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Scores</SelectItem>
                <SelectItem value="excellent">Excellent (80%+)</SelectItem>
                <SelectItem value="good">Good (60-79%)</SelectItem>
                <SelectItem value="needs-improvement">
                  Needs Improvement (&lt;60%)
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Sort By */}
          <div className="space-y-2">
            <Label htmlFor="sort" className="flex items-center gap-2">
              <ArrowUpDown className="w-4 h-4" />
              Sort By
            </Label>
            <Select value={filters.sortBy} onValueChange={handleSortChange}>
              <SelectTrigger id="sort">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="newest">Newest First</SelectItem>
                <SelectItem value="oldest">Oldest First</SelectItem>
                <SelectItem value="highest">Highest Score</SelectItem>
                <SelectItem value="lowest">Lowest Score</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
