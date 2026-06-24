"use client";

import { useState } from "react";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { DashboardHeader } from "@/components/layout/dashboard-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/auth.context";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { format } from "date-fns";
import { User, Mail, Calendar, ArrowLeft } from "lucide-react";
import { useRouter } from "next/navigation";

const profileSchema = z.object({
  full_name: z.string().min(2, "Name must be at least 2 characters"),
});

type ProfileFormData = z.infer<typeof profileSchema>;

export default function ProfilePage() {
  const { user, updateProfile, isLoading } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      full_name: user?.full_name || "",
    },
  });

  const onSubmit = async (data: ProfileFormData) => {
    try {
      setError("");
      setSuccess("");
      await updateProfile(data);
      setSuccess("Profile updated successfully!");
      setIsEditing(false);
    } catch (err: any) {
      setError(err.response?.data?.message || "Update failed. Please try again.");
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), "MMMM dd, yyyy");
    } catch {
      return dateString;
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <DashboardHeader />

        <main className="container mx-auto px-4 py-8 max-w-3xl">
          <Button
            variant="ghost"
            className="mb-6"
            onClick={() => router.push("/dashboard")}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Dashboard
          </Button>

          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Profile Settings</h2>
            <p className="text-gray-600 mt-2">
              Manage your account information
            </p>
          </div>

          {success && (
            <div className="mb-6 bg-green-50 text-green-600 p-4 rounded-md border border-green-200">
              {success}
            </div>
          )}

          {error && (
            <div className="mb-6 bg-red-50 text-red-600 p-4 rounded-md border border-red-200">
              {error}
            </div>
          )}

          <div className="space-y-6">
            {/* Profile Information Card */}
            <Card className="shadow-md border-0">
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
                <CardDescription>
                  Update your profile details
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                  <div className="space-y-4">
                    <div className="flex items-start space-x-4">
                      <div className="bg-primary/10 p-3 rounded-full mt-1">
                        <User className="h-6 w-6 text-primary" />
                      </div>
                      <div className="flex-1">
                        <Label htmlFor="full_name">Full Name</Label>
                        <Input
                          id="full_name"
                          type="text"
                          {...register("full_name")}
                          disabled={!isEditing}
                          className="mt-2"
                        />
                        {errors.full_name && (
                          <p className="text-red-500 text-sm mt-1">
                            {errors.full_name.message}
                          </p>
                        )}
                      </div>
                    </div>

                    <div className="flex items-start space-x-4">
                      <div className="bg-primary/10 p-3 rounded-full mt-1">
                        <Mail className="h-6 w-6 text-primary" />
                      </div>
                      <div className="flex-1">
                        <Label>Email Address</Label>
                        <Input
                          type="email"
                          value={user?.email}
                          disabled
                          className="mt-2 bg-gray-50"
                        />
                        <p className="text-xs text-muted-foreground mt-1">
                          Email cannot be changed
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start space-x-4">
                      <div className="bg-primary/10 p-3 rounded-full mt-1">
                        <Calendar className="h-6 w-6 text-primary" />
                      </div>
                      <div className="flex-1">
                        <Label>Account Created</Label>
                        <Input
                          type="text"
                          value={user?.created_at ? formatDate(user.created_at) : ""}
                          disabled
                          className="mt-2 bg-gray-50"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="flex space-x-3 pt-4">
                    {!isEditing ? (
                      <Button
                        type="button"
                        onClick={() => setIsEditing(true)}
                        className="flex-1"
                      >
                        Edit Profile
                      </Button>
                    ) : (
                      <>
                        <Button
                          type="submit"
                          disabled={isLoading}
                          className="flex-1"
                        >
                          {isLoading ? "Saving..." : "Save Changes"}
                        </Button>
                        <Button
                          type="button"
                          variant="outline"
                          onClick={() => {
                            setIsEditing(false);
                            setError("");
                            setSuccess("");
                          }}
                          className="flex-1"
                        >
                          Cancel
                        </Button>
                      </>
                    )}
                  </div>
                </form>
              </CardContent>
            </Card>

            {/* Account Stats Card */}
            <Card className="shadow-md border-0">
              <CardHeader>
                <CardTitle>Account Statistics</CardTitle>
                <CardDescription>
                  Your learning progress overview
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <p className="text-3xl font-bold text-primary">1</p>
                    <p className="text-sm text-gray-600 mt-1">Active Subject</p>
                  </div>
                  <div className="text-center p-4 bg-indigo-50 rounded-lg">
                    <p className="text-3xl font-bold text-indigo-600">0</p>
                    <p className="text-sm text-gray-600 mt-1">Completed Lessons</p>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <p className="text-3xl font-bold text-purple-600">0</p>
                    <p className="text-sm text-gray-600 mt-1">Hours Studied</p>
                  </div>
                </div>
                <p className="text-xs text-center text-muted-foreground mt-4">
                  Stats will be available in Phase 2+
                </p>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
