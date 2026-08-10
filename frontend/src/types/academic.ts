export type CourseRole =
  | "Faculty"
  | "Course Lead"
  | "HOD";

export interface AcademicPlannerInput {
  subject: string;
  courseCode?: string;
  branch: string;
  semester: number;
  courseRole: CourseRole;
  credits?: number;
  hoursPerWeek?: number;
  university?: string;
  regulation?: string;
  additionalRequirements?: string;
}