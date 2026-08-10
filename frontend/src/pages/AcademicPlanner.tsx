import { zodResolver } from "@hookform/resolvers/zod";
import { Sparkles } from "lucide-react";
import { useForm } from "react-hook-form";
import { useState } from "react";
import { generateAcademicPlan } from "@/lib/api";
import type { AcademicPlanResponse } from "@/lib/api";
import { AcademicPlanResult } from "@/components/planner/AcademicPlanResult";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { Button } from "@/components/ui/button";

import {
  academicPlannerSchema,
  type AcademicPlannerFormData,
} from "@/lib/validation";

function AcademicPlanner() {
  const [result, setResult] =
    useState<AcademicPlanResponse | null>(null);

  const [isGenerating, setIsGenerating] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const form = useForm<AcademicPlannerFormData>({
    resolver: zodResolver(academicPlannerSchema),
    defaultValues: {
      subject: "",
      courseCode: "",
      branch: "",
      semester: 1,
      courseRole: "Course Lead",
      credits: undefined,
      hoursPerWeek: undefined,
      university: "",
      regulation: "",
      additionalRequirements: "",
    },
  });

  const onSubmit = async (
    data: AcademicPlannerFormData,
  ) => {
    setIsGenerating(true);
    setError(null);
    setResult(null);

    try {
      const response =
        await generateAcademicPlan(data);

      setResult(response);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong.",
      );
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-5xl p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Sparkles className="size-5" />
          </div>

          <div>
            <h1 className="text-3xl font-semibold tracking-tight">
              Academic Planner
            </h1>

            <p className="text-sm text-muted-foreground">
              Tell us about your course and let AI prepare
              your academic plan.
            </p>
          </div>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Course Information</CardTitle>

          <CardDescription>
            Provide the basic details about the course you
            are teaching.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-8"
          >
            {/* Basic Information */}
            <section className="space-y-5">
              <div>
                <h2 className="text-base font-semibold">
                  Basic Information
                </h2>

                <p className="text-sm text-muted-foreground">
                  Tell us what course you are teaching.
                </p>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                {/* Subject */}
                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="subject">
                    Subject
                  </Label>

                  <Input
                    id="subject"
                    placeholder="e.g. Data Structures"
                    {...form.register("subject")}
                  />

                  {form.formState.errors.subject && (
                    <p className="text-sm text-destructive">
                      {form.formState.errors.subject.message}
                    </p>
                  )}
                </div>

                {/* Course Code */}
                <div className="space-y-2">
                  <Label htmlFor="courseCode">
                    Course Code
                  </Label>

                  <Input
                    id="courseCode"
                    placeholder="e.g. CS301"
                    {...form.register("courseCode")}
                  />
                </div>

                {/* Branch */}
                <div className="space-y-2">
                  <Label htmlFor="branch">
                    Branch / Program
                  </Label>

                  <Input
                    id="branch"
                    placeholder="e.g. CSE"
                    {...form.register("branch")}
                  />

                  {form.formState.errors.branch && (
                    <p className="text-sm text-destructive">
                      {form.formState.errors.branch.message}
                    </p>
                  )}
                </div>

                {/* Semester */}
                <div className="space-y-2">
                  <Label>Semester</Label>

                  <Select
                    defaultValue="1"
                    onValueChange={(value) =>
                      form.setValue(
                        "semester",
                        Number(value),
                        {
                          shouldValidate: true,
                        },
                      )
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select semester" />
                    </SelectTrigger>

                    <SelectContent>
                      {Array.from(
                        { length: 8 },
                        (_, index) => index + 1,
                      ).map((semester) => (
                        <SelectItem
                          key={semester}
                          value={String(semester)}
                        >
                          Semester {semester}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Role */}
                <div className="space-y-2">
                  <Label>Course Role</Label>

                  <Select
                    defaultValue="Course Lead"
                    onValueChange={(value) =>
                      form.setValue(
                        "courseRole",
                        value as AcademicPlannerFormData["courseRole"],
                        {
                          shouldValidate: true,
                        },
                      )
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select role" />
                    </SelectTrigger>

                    <SelectContent>
                      <SelectItem value="Faculty">
                        Faculty
                      </SelectItem>

                      <SelectItem value="Course Lead">
                        Course Lead
                      </SelectItem>

                      <SelectItem value="HOD">
                        HOD
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </section>

            {/* Academic Details */}
            <section className="space-y-5 border-t pt-8">
              <div>
                <h2 className="text-base font-semibold">
                  Academic Details
                </h2>

                <p className="text-sm text-muted-foreground">
                  These details help the AI create a more
                  relevant plan.
                </p>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="credits">
                    Credits
                  </Label>

                  <Input
                    id="credits"
                    type="number"
                    min={0}
                    max={20}
                    placeholder="e.g. 4"
                    {...form.register("credits", {
                      setValueAs: (value) =>
                        value === ""
                          ? undefined
                          : Number(value),
                    })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="hoursPerWeek">
                    Hours per Week
                  </Label>

                  <Input
                    id="hoursPerWeek"
                    type="number"
                    min={1}
                    max={40}
                    placeholder="e.g. 4"
                    {...form.register("hoursPerWeek", {
                      setValueAs: (value) =>
                        value === ""
                          ? undefined
                          : Number(value),
                    })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="university">
                    University
                  </Label>

                  <Input
                    id="university"
                    placeholder="e.g. VTU"
                    {...form.register("university")}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="regulation">
                    Regulation
                  </Label>

                  <Input
                    id="regulation"
                    placeholder="e.g. 2025 Regulation"
                    {...form.register("regulation")}
                  />
                </div>
              </div>
            </section>

            {/* Requirements */}
            <section className="space-y-5 border-t pt-8">
              <div>
                <h2 className="text-base font-semibold">
                  Additional Requirements
                </h2>

                <p className="text-sm text-muted-foreground">
                  Tell the AI about any specific requirements
                  or constraints.
                </p>
              </div>

              <Textarea
                placeholder="Example: Prepare a semester-wise lesson plan with practical activities, Bloom's taxonomy levels, assessment methods and CO-PO mapping."
                className="min-h-32 resize-none"
                {...form.register(
                  "additionalRequirements",
                )}
              />
            </section>

            {/* Submit */}
            <div className="flex justify-end border-t pt-6">
              <Button
                type="submit"
                size="lg"
                className="gap-2"
                disabled={isGenerating}
              >
                <Sparkles className="size-4" />

                {isGenerating
                  ? "Generating..."
                  : "Generate Academic Plan"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
      {error && (
        <div className="mt-6 rounded-lg border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
         {error}
        </div>   
      )}

      {result && (
        <AcademicPlanResult plan={result} />
      )}
    </div>
  );
}

export default AcademicPlanner;
