import type { AcademicPlannerInput } from "../schemas/planner.schema.js";

const AI_SERVICE_URL =
  process.env.AI_SERVICE_URL ?? "http://localhost:8000";

export async function generateLessonPlan(
  input: AcademicPlannerInput,
) {
  const response = await fetch(
    `${AI_SERVICE_URL}/api/v1/planner/lesson-plan`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    },
  );

  if (!response.ok) {
    const errorBody = await response.text();

    throw new Error(
      `AI service returned ${response.status}: ${errorBody}`,
    );
  }

  return response.json();
}