import { z } from "zod";

export const academicPlannerSchema = z.object({
  subject: z.string().min(2),
  courseCode: z.string().optional(),
  branch: z.string().min(2),
  semester: z.number().int().min(1).max(12),
  courseRole: z.enum(["Faculty", "Course Lead", "HOD"]),
  credits: z.number().min(0).max(20).optional(),
  hoursPerWeek: z.number().min(1).max(40).optional(),
  university: z.string().optional(),
  regulation: z.string().optional(),
  additionalRequirements: z.string().max(2000).optional(),
});

export type AcademicPlannerInput = z.infer<
  typeof academicPlannerSchema
>;