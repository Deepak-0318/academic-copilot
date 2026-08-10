import { Outlet } from "react-router-dom";

import AppHeader from "@/components/common/AppHeader";
import AppSidebar from "@/components/common/AppSidebar";

function DashboardLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <AppSidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <AppHeader />

        <main className="min-h-0 flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default DashboardLayout;