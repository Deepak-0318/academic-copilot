import {
  BookOpen,
  FileText,
  GraduationCap,
  Sparkles,
} from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const features = [
  {
    title: "Lesson Plans",
    description:
      "Create structured lesson plans for your courses.",
    icon: FileText,
  },
  {
    title: "CO-PO Mapping",
    description:
      "Generate course outcome and program outcome mappings.",
    icon: GraduationCap,
  },
  {
    title: "Teaching Plans",
    description:
      "Organize your teaching schedule and classroom activities.",
    icon: BookOpen,
  },
  {
    title: "AI Academic Assistant",
    description:
      "Use AI to plan, generate and improve academic content.",
    icon: Sparkles,
  },
];

function Dashboard() {
  return (
    <div className="mx-auto w-full max-w-7xl p-6 lg:p-8">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">
          Welcome to Academic Co-Pilot
        </h1>

        <p className="mt-2 max-w-2xl text-muted-foreground">
          Your AI-powered workspace for academic planning,
          teaching preparation and course management.
        </p>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {features.map((feature) => {
          const Icon = feature.icon;

          return (
            <Card key={feature.title}>
              <CardHeader>
                <Icon className="size-5 text-primary" />

                <CardTitle className="mt-2 text-base">
                  {feature.title}
                </CardTitle>
              </CardHeader>

              <CardContent>
                <p className="text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

export default Dashboard;