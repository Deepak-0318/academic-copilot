import { Router } from "express";

import {
  createLessonPlan,
} from "../controllers/planner.controller.js";

const router = Router();

router.post(
  "/lesson-plan",
  createLessonPlan,
);

export default router;