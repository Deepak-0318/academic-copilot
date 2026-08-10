import type { Request, Response } from "express";

import {
  academicPlannerSchema,
} from "../schemas/planner.schema.js";

import {
  generateLessonPlan,
} from "../services/ai.service.js";

export async function createLessonPlan(
  req: Request,
  res: Response,
) {
  const result = academicPlannerSchema.safeParse(
    req.body,
  );

  if (!result.success) {
    return res.status(400).json({
      message: "Invalid academic planner request.",
      errors: result.error.flatten(),
    });
  }

  try {
    const academicPlan =
      await generateLessonPlan(result.data);

    return res.status(200).json(academicPlan);
  } catch (error) {
    console.error(
      "Lesson plan generation failed:",
      error,
    );

    return res.status(502).json({
      message:
        "Unable to generate academic plan.",
    });
  }
}