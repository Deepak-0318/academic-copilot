import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import DashboardLayout from "@/layouts/DashboardLayout";

import AcademicPlanner from "@/pages/AcademicPlanner";
import Dashboard from "@/pages/Dashboard";
import Settings from "@/pages/Settings";
import Subjects from "@/pages/Subjects";

export function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/planner"
            element={<AcademicPlanner />}
          />

          <Route
            path="/subjects"
            element={<Subjects />}
          />

          <Route
            path="/settings"
            element={<Settings />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}