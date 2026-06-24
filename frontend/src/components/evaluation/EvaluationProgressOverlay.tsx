/**
 * EvaluationProgressOverlay – animated overlay shown while AI is evaluating
 */
"use client";

import { useEffect, useState } from "react";
import { Brain, Sparkles, BookOpen, Cpu } from "lucide-react";

const STEPS = [
  { icon: BookOpen, text: "Retrieving textbook context via RAG…" },
  { icon: Brain, text: "Analysing student answers…" },
  { icon: Cpu, text: "Generating AI evaluation…" },
  { icon: Sparkles, text: "Computing marks and feedback…" },
];

export function EvaluationProgressOverlay() {
  const [stepIdx, setStepIdx] = useState(0);
  const [dotCount, setDotCount] = useState(1);

  useEffect(() => {
    const stepTimer = setInterval(() => {
      setStepIdx((prev) => (prev + 1) % STEPS.length);
    }, 2500);
    const dotTimer = setInterval(() => {
      setDotCount((prev) => (prev % 3) + 1);
    }, 500);
    return () => {
      clearInterval(stepTimer);
      clearInterval(dotTimer);
    };
  }, []);

  const { icon: Icon, text } = STEPS[stepIdx];

  return (
    <div className="fixed inset-0 bg-white/80 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-2xl border border-indigo-100 p-10 max-w-md w-full mx-4 text-center">
        {/* Pulsing icon */}
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="w-20 h-20 rounded-full bg-indigo-100 flex items-center justify-center animate-pulse">
              <Icon className="h-10 w-10 text-indigo-600" />
            </div>
            <div className="absolute -top-1 -right-1">
              <span className="flex h-4 w-4">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-4 w-4 bg-indigo-500" />
              </span>
            </div>
          </div>
        </div>

        {/* Title */}
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          AI Evaluation in Progress
        </h2>
        <p className="text-sm text-gray-500 mb-6">
          This may take a moment for long-answer questions
        </p>

        {/* Animated step text */}
        <div className="bg-indigo-50 rounded-xl px-5 py-3 min-h-[48px] flex items-center justify-center">
          <p className="text-sm text-indigo-700 font-medium transition-all">
            {text}
            {".".repeat(dotCount)}
          </p>
        </div>

        {/* Progress dots */}
        <div className="flex justify-center gap-2 mt-6">
          {STEPS.map((_, i) => (
            <div
              key={i}
              className={`h-2 rounded-full transition-all duration-500 ${
                i === stepIdx
                  ? "w-6 bg-indigo-500"
                  : i < stepIdx
                  ? "w-2 bg-indigo-300"
                  : "w-2 bg-gray-200"
              }`}
            />
          ))}
        </div>

        <p className="mt-6 text-xs text-gray-400">
          Please do not close this page
        </p>
      </div>
    </div>
  );
}
