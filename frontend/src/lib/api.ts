import type { AcademicPlannerFormData } from "./validation";

const API_BASE_URL =
  import.meta.env.VITE_API_URL ??
  "http://localhost:4000/api/v1";

export interface CourseOutcome {
  code: string;
  description: string;
}

export interface LessonPlanItem {
  unit: string;
  topic: string;
  hours: number;
  learningObjectives: string[];
  teachingMethod: string;
  bloomLevel: string;
}

export interface AssessmentItem {
  type: string;
  description: string;
  weightage?: number;
}

export interface COPOMapping {
  courseOutcome: string;
  mappings: Record<string, string>;
}

export interface AcademicPlanResponse {
  courseOverview: string;
  courseOutcomes: CourseOutcome[];
  lessonPlan: LessonPlanItem[];
  assessmentPlan: AssessmentItem[];
  coPoMapping: COPOMapping[];
}

export async function generateAcademicPlan(
  input: AcademicPlannerFormData,
): Promise<AcademicPlanResponse> {
  const response = await fetch(
    `${API_BASE_URL}/planner/lesson-plan`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    },
  );

  if (!response.ok) {
    const body = await response.json().catch(() => null);

    throw new Error(
      body?.message ??
        "Failed to generate academic plan.",
    );
  }

  return response.json();
}