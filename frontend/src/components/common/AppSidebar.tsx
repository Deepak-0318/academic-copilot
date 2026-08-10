import {
  BookOpen,
  LayoutDashboard,
  Settings,
  Sparkles,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Academic Planner",
    href: "/planner",
    icon: Sparkles,
  },
  {
    name: "Subjects",
    href: "/subjects",
    icon: BookOpen,
  },
];

function AppSidebar() {
  return (
    <aside className="flex h-screen w-64 flex-col border-r bg-background">
      {/* Brand */}
      <div className="flex h-16 items-center gap-3 border-b px-6">
        <div className="flex size-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Sparkles className="size-5" />
        </div>

        <div>
          <h1 className="text-sm font-semibold">
            Academic Co-Pilot
          </h1>

          <p className="text-xs text-muted-foreground">
            Faculty Assistant
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.href}
              to={item.href}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground",
                ].join(" ")
              }
            >
              <Icon className="size-4" />
              {item.name}
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom Navigation */}
      <div className="border-t p-4">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            [
              "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
              isActive
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-muted hover:text-foreground",
            ].join(" ")
          }
        >
          <Settings className="size-4" />
          Settings
        </NavLink>

        <div className="mt-4 px-3 text-xs text-muted-foreground">
          Academic Co-Pilot v1.0
        </div>
      </div>
    </aside>
  );
}

export default AppSidebar;