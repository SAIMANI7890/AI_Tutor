/**
 * Evaluation History Table Component
 * Displays list of evaluations with actions
 */

"use client";

import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Eye, Trash2 } from "lucide-react";
import type { Evaluation } from "@/types/evaluation";
import {
  calculatePercentage,
  getScoreStatus,
  getScoreStatusColor,
  getScoreStatusLabel,
  formatEvaluationDate,
  truncateText,
} from "@/lib/evaluation-utils";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface EvaluationHistoryTableProps {
  evaluations: Evaluation[];
  onViewDetails: (evaluation: Evaluation) => void;
  onDelete: (evaluationId: string) => Promise<void>;
  isDeleting?: string | null;
}

export function EvaluationHistoryTable({
  evaluations,
  onViewDetails,
  onDelete,
  isDeleting,
}: EvaluationHistoryTableProps) {
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  const handleDeleteClick = (evaluationId: string) => {
    setDeleteConfirm(evaluationId);
  };

  const handleConfirmDelete = async () => {
    if (deleteConfirm) {
      await onDelete(deleteConfirm);
      setDeleteConfirm(null);
    }
  };

  if (evaluations.length === 0) {
    return (
      <div className="text-center py-12 border rounded-lg bg-muted/50">
        <p className="text-muted-foreground">No evaluations found</p>
        <p className="text-sm text-muted-foreground mt-2">
          Submit your first answer to see your evaluation history
        </p>
      </div>
    );
  }

  return (
    <>
      {/* Desktop Table */}
      <div className="hidden md:block border rounded-lg overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Chapter</TableHead>
              <TableHead className="max-w-md">Question</TableHead>
              <TableHead>Score</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {evaluations.map((evaluation) => {
              const percentage = calculatePercentage(
                evaluation.marks_awarded,
                evaluation.total_marks
              );
              const status = getScoreStatus(percentage);
              const statusColor = getScoreStatusColor(status);
              const statusLabel = getScoreStatusLabel(status);

              return (
                <TableRow key={evaluation.id}>
                  <TableCell className="whitespace-nowrap">
                    {formatEvaluationDate(evaluation.created_at)}
                  </TableCell>
                  <TableCell>
                    {evaluation.chapter_name || (
                      <span className="text-muted-foreground">—</span>
                    )}
                  </TableCell>
                  <TableCell className="max-w-md">
                    <span className="line-clamp-2">
                      {truncateText(evaluation.question, 100)}
                    </span>
                  </TableCell>
                  <TableCell>
                    <span className="font-semibold">
                      {evaluation.marks_awarded} / {evaluation.total_marks}
                    </span>
                    <span className="text-muted-foreground text-sm ml-2">
                      ({percentage}%)
                    </span>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className={statusColor}>
                      {statusLabel}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onViewDetails(evaluation)}
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDeleteClick(evaluation.id)}
                        disabled={isDeleting === evaluation.id}
                      >
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      {/* Mobile Cards */}
      <div className="md:hidden space-y-4">
        {evaluations.map((evaluation) => {
          const percentage = calculatePercentage(
            evaluation.marks_awarded,
            evaluation.total_marks
          );
          const status = getScoreStatus(percentage);
          const statusColor = getScoreStatusColor(status);
          const statusLabel = getScoreStatusLabel(status);

          return (
            <div
              key={evaluation.id}
              className="border rounded-lg p-4 space-y-3"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <p className="font-medium line-clamp-2">
                    {truncateText(evaluation.question, 80)}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    {formatEvaluationDate(evaluation.created_at)}
                  </p>
                </div>
                <Badge variant="outline" className={statusColor}>
                  {statusLabel}
                </Badge>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  {evaluation.chapter_name && (
                    <p className="text-sm text-muted-foreground">
                      {evaluation.chapter_name}
                    </p>
                  )}
                  <p className="font-semibold">
                    {evaluation.marks_awarded} / {evaluation.total_marks}
                    <span className="text-muted-foreground text-sm ml-2">
                      ({percentage}%)
                    </span>
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onViewDetails(evaluation)}
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    View
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeleteClick(evaluation.id)}
                    disabled={isDeleting === evaluation.id}
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </Button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Delete Confirmation Dialog */}
      <AlertDialog
        open={deleteConfirm !== null}
        onOpenChange={() => setDeleteConfirm(null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Evaluation</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete this evaluation? This action
              cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleConfirmDelete}
              className="bg-red-600 hover:bg-red-700"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
