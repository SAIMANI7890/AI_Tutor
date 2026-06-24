"use client";

import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BookOpen, ArrowRight } from "lucide-react";
import { useAuth } from "@/contexts/auth.context";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const { user } = useAuth();
  const router = useRouter();

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />

        <main className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900">
              Welcome back, {user?.full_name?.split(" ")[0]}! 👋
            </h2>
            <p className="text-gray-600 mt-2">
              Let's continue your learning journey today
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Social Studies Card */}
            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md group">
              <CardHeader className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-3 rounded-lg shadow-md">
                    <BookOpen className="h-8 w-8 text-white" />
                  </div>
                </div>
                <div>
                  <CardTitle className="text-2xl">Social Studies</CardTitle>
                  <CardDescription className="mt-2">
                    Master history, geography, and civic education with AI-powered assistance
                  </CardDescription>
                </div>
              </CardHeader>
              <CardContent>
                <Button 
                  className="w-full group-hover:bg-primary/90 transition-all" 
                  size="lg"
                  onClick={() => router.push("/dashboard/social/chat")}
                >
                  Start Learning
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>

            {/* Placeholder for future subjects */}
            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md opacity-60">
              <CardHeader className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="bg-gradient-to-br from-gray-400 to-gray-500 p-3 rounded-lg shadow-md">
                    <BookOpen className="h-8 w-8 text-white" />
                  </div>
                </div>
                <div>
                  <CardTitle className="text-2xl">More Subjects</CardTitle>
                  <CardDescription className="mt-2">
                    Additional subjects will be available in future updates
                  </CardDescription>
                </div>
              </CardHeader>
              <CardContent>
                <Button 
                  className="w-full" 
                  size="lg"
                  disabled
                  variant="outline"
                >
                  Coming Soon
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Info Section */}
          {/* <div className="mt-12 bg-white rounded-lg shadow-md p-6 border-l-4 border-primary">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              🎯 Your Learning Platform
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-600">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Phase 1 Features:</h4>
                <ul className="space-y-1 text-sm">
                  <li>✅ User Authentication</li>
                  <li>✅ Dashboard Access</li>
                  <li>✅ Profile Management</li>
                  <li>✅ Subject Overview</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Coming in Phase 2+:</h4>
                <ul className="space-y-1 text-sm">
                  <li>🚀 AI Study Planner</li>
                  <li>🚀 Examination Generator</li>
                  <li>🚀 AI Tutor Chat</li>
                  <li>🚀 Progress Tracking</li>
                </ul>
              </div>
            </div>
          </div> */}
        </main>
      </div>
    </ProtectedRoute>
  );
}
