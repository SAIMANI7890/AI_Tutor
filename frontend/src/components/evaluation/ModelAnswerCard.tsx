/**
 * Model Answer Card Component
 * Displays the AI-generated ideal answer
 */

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb } from "lucide-react";

interface ModelAnswerCardProps {
  modelAnswer: string;
}

export function ModelAnswerCard({ modelAnswer }: ModelAnswerCardProps) {
  return (
    <Card className="border-blue-200 bg-blue-50/50">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2 text-blue-700">
          <Lightbulb className="w-5 h-5" />
          Model Answer
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          This is the ideal answer generated from your textbook content
        </p>
      </CardHeader>
      <CardContent>
        <div className="prose prose-sm max-w-none">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {modelAnswer}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
