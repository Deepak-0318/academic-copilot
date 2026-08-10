import { z } from "zod";

export const academicPlannerSchema = z.object({
  subject: z
    .string()
    .min(2, "Subject name is required."),

  courseCode: z
    .string()
    .optional(),

  branch: z
    .string()
    .min(2, "Branch / Program is required."),

  semester: z
    .number()
    .min(1)
    .max(12),

  courseRole: z.enum([
    "Faculty",
    "Course Lead",
    "HOD",
  ]),

  credits: z
    .number()
    .min(0)
    .max(20)
    .optional(),

  hoursPerWeek: z
    .number()
    .min(1)
    .max(40)
    .optional(),

  university: z
    .string()
    .optional(),

  regulation: z
    .string()
    .optional(),

  additionalRequirements: z
    .string()
    .max(2000)
    .optional(),
});

export type AcademicPlannerFormData =
  z.infer<typeof academicPlannerSchema>;