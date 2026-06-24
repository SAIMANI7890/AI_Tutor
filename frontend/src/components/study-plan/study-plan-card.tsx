/**
 * StudyPlanCard Component
 * Displays individual study plan items with optimistic UI updates
 */

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { ActivityType, StudyStatus, type StudyPlanItem } from "@/types/study-plan";
import { BookOpen, RefreshCw, FileCheck, Calendar, Loader2 } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

interface StudyPlanCardProps {
  item: StudyPlanItem;
  onStatusChange?: (itemId: number, newStatus: StudyStatus) => Promise<void>;
  readonly?: boolean;
}

export function StudyPlanCard({ item, onStatusChange, readonly = false }: StudyPlanCardProps) {
  const [isUpdating, setIsUpdating] = useState(false);
  const [optimisticStatus, setOptimisticStatus] = useState<StudyStatus | null>(null);
  
  // Use optimistic status if available, otherwise use actual status
  const displayStatus = optimisticStatus || item.status;
  const isCompleted = displayStatus === StudyStatus.COMPLETED;
  const isSkipped = displayStatus === StudyStatus.SKIPPED;

  const getActivityIcon = () => {
    switch (item.activity_type) {
      case ActivityType.STUDY:
        return <BookOpen className="h-5 w-5 text-blue-600" />;
      case ActivityType.REVISION:
        return <RefreshCw className="h-5 w-5 text-purple-600" />;
      case ActivityType.MOCK_TEST:
        return <FileCheck className="h-5 w-5 text-green-600" />;
      default:
        return <BookOpen className="h-5 w-5" />;
    }
  };

  const getActivityColor = () => {
    switch (item.activity_type) {
      case ActivityType.STUDY:
        return "bg-blue-50 border-blue-200";
      case ActivityType.REVISION:
        return "bg-purple-50 border-purple-200";
      case ActivityType.MOCK_TEST:
        return "bg-green-50 border-green-200";
      default:
        return "bg-gray-50 border-gray-200";
    }
  };

  const handleCheckboxChange = async (checked: boolean) => {
    if (readonly || !onStatusChange || isUpdating) return;

    const newStatus = checked ? StudyStatus.COMPLETED : StudyStatus.PENDING;
    
    // Optimistic update
    setOptimisticStatus(newStatus);
    setIsUpdating(true);

    try {
      await onStatusChange(item.id, newStatus);
      // Success - clear optimistic state
      setOptimisticStatus(null);
    } catch (error) {
      // Error - rollback optimistic update
      console.error("Failed to update status:", error);
      setOptimisticStatus(null);
      // You could show a toast notification here
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <Card
      className={cn(
        "transition-all hover:shadow-md",
        getActivityColor(),
        isCompleted && "opacity-75",
        isSkipped && "opacity-50",
        isUpdating && "opacity-70"
      )}
    >
      <CardContent className="p-4">
        <div className="flex items-start gap-4">
          {/* Checkbox with loading state */}
          {!readonly && (
            <div className="mt-1 relative">
              {isUpdating ? (
                <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
              ) : (
                <Checkbox
                  checked={isCompleted}
                  onCheckedChange={handleCheckboxChange}
                  disabled={isSkipped || isUpdating}
                />
              )}
            </div>
          )}

          {/* Icon */}
          <div className="flex-shrink-0">{getActivityIcon()}</div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2 mb-2">
              <div>
                <h3 className="font-semibold text-gray-900">
                  Day {item.day_number}
                </h3>
                <p className="text-sm text-gray-600 flex items-center gap-1 mt-1">
                  <Calendar className="h-3 w-3" />
                  {format(new Date(item.study_date), "MMM dd, yyyy")}
                </p>
              </div>
              <Badge
                variant={isCompleted ? "default" : "outline"}
                className={cn(
                  isCompleted && "bg-green-600",
                  isSkipped && "bg-gray-400"
                )}
              >
                {displayStatus}
              </Badge>
            </div>

            <div className="space-y-1">
              <p className="text-sm font-medium text-gray-700">
                {item.activity_type}
              </p>
              {item.chapter_name && (
                <p className="text-sm text-gray-600">{item.chapter_name}</p>
              )}
              <p className="text-xs text-gray-500">
                {item.allocated_hours} {item.allocated_hours === 1 ? "hour" : "hours"}
              </p>
              {item.completed_at && isCompleted && (
                <p className="text-xs text-green-600">
                  ✓ Completed {format(new Date(item.completed_at), "MMM dd, h:mm a")}
                </p>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
