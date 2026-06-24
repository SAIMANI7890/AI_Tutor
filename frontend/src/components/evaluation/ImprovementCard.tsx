/**
 * Improvement Card Component
 * Displays areas for improvement from AI evaluation
 */

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle } from "lucide-react";

interface ImprovementCardProps {
  improvements: string[];
}

export function ImprovementCard({ improvements }: ImprovementCardProps) {
  if (!improvements || improvements.length === 0) {
    return null;
  }

  return (
    <Card className="border-amber-200 bg-amber-50/50">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2 text-amber-700">
          <AlertCircle className="w-5 h-5" />
          Areas for Improvement
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {improvements.map((improvement, index) => (
            <li key={index} className="flex items-start gap-2">
              <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
              <span className="text-sm text-gray-700">{improvement}</span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
