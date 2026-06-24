/**
 * AIInsightsCard – shows AI-generated performance insights (strengths, weak areas, recommendations)
 */
"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, AlertTriangle, Lightbulb, Brain } from "lucide-react";
import type { AIInsights } from "@/types/evaluation";

interface AIInsightsCardProps {
  insights: AIInsights;
}

export function AIInsightsCard({ insights }: AIInsightsCardProps) {
  const hasContent =
    insights.strengths.length > 0 ||
    insights.weak_areas.length > 0 ||
    insights.recommendations.length > 0;

  if (!hasContent) return null;

  return (
    <Card className="border border-indigo-200 bg-gradient-to-br from-indigo-50/60 to-purple-50/60 shadow-sm">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-indigo-800 text-base">
          <Brain className="h-5 w-5 text-indigo-500" />
          AI Performance Summary
        </CardTitle>
      </CardHeader>
      <CardContent className="grid gap-5 md:grid-cols-3">

        {/* Strengths */}
        {insights.strengths.length > 0 && (
          <div>
            <p className="flex items-center gap-1.5 text-sm font-semibold text-green-700 mb-2">
              <CheckCircle2 className="h-4 w-4" />
              Strengths
            </p>
            <ul className="space-y-1.5">
              {insights.strengths.map((s, i) => (
                <li key={i} className="text-sm text-green-800 flex items-start gap-1.5">
                  <span className="text-green-500 mt-0.5 shrink-0">✓</span>
                  {s}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weak Areas */}
        {insights.weak_areas.length > 0 && (
          <div>
            <p className="flex items-center gap-1.5 text-sm font-semibold text-amber-700 mb-2">
              <AlertTriangle className="h-4 w-4" />
              Weak Areas
            </p>
            <ul className="space-y-1.5">
              {insights.weak_areas.map((w, i) => (
                <li key={i} className="text-sm text-amber-800 flex items-start gap-1.5">
                  <span className="text-amber-500 mt-0.5 shrink-0">•</span>
                  {w}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {insights.recommendations.length > 0 && (
          <div>
            <p className="flex items-center gap-1.5 text-sm font-semibold text-indigo-700 mb-2">
              <Lightbulb className="h-4 w-4" />
              Recommendations
            </p>
            <ul className="space-y-1.5">
              {insights.recommendations.map((r, i) => (
                <li key={i} className="text-sm text-indigo-800 flex items-start gap-1.5">
                  <span className="text-indigo-400 mt-0.5 shrink-0">→</span>
                  {r}
                </li>
              ))}
            </ul>
          </div>
        )}

      </CardContent>
    </Card>
  );
}
