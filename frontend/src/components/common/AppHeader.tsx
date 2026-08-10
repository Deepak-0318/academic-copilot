import { Bell } from "lucide-react";
import { Button } from "@/components/ui/button";

function AppHeader() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-background px-6">
      <div>
        <h2 className="text-sm font-medium">
          Academic Workspace
        </h2>

        <p className="text-xs text-muted-foreground">
          Plan smarter. Teach better.
        </p>
      </div>

      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          aria-label="Notifications"
        >
          <Bell className="size-4" />
        </Button>

        <div className="flex items-center gap-3 border-l pl-3">
          <div className="flex size-8 items-center justify-center rounded-full bg-muted text-sm font-medium">
            F
          </div>

          <div className="hidden text-right sm:block">
            <p className="text-sm font-medium">
              Faculty
            </p>

            <p className="text-xs text-muted-foreground">
              Course Lead
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}

export default AppHeader;