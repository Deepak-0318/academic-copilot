import cors from "cors";
import express from "express";

import healthRoutes from "./routes/health.routes.js";
import plannerRoutes from "./routes/planner.routes.js";

const app = express();

app.use(
  cors({
    origin: process.env.FRONTEND_URL ?? "http://localhost:5173",
  }),
);

app.use(express.json());

app.get("/", (_req, res) => {
  res.json({
    name: "Academic Co-Pilot API",
    status: "ok",
  });
});

app.use("/api/v1/health", healthRoutes);
app.use("/api/v1/planner", plannerRoutes);

export default app;