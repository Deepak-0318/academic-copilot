import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import type { AcademicPlanResponse } from "@/lib/api";

interface Props {
  plan: AcademicPlanResponse;
}

export function AcademicPlanResult({
  plan,
}: Props) {
  return (
    <div className="mt-8 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>
            Course Overview
          </CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-sm leading-7 text-muted-foreground">
            {plan.courseOverview}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>
            Course Outcomes
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          {plan.courseOutcomes.map((outcome) => (
            <div
              key={outcome.code}
              className="rounded-lg border p-4"
            >
              <p className="font-semibold">
                {outcome.code}
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                {outcome.description}
              </p>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>
            Lesson Plan
          </CardTitle>
        </CardHeader>

        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="p-3">Unit</th>
                  <th className="p-3">Topic</th>
                  <th className="p-3">Hours</th>
                  <th className="p-3">
                    Bloom Level
                  </th>
                  <th className="p-3">
                    Teaching Method
                  </th>
                </tr>
              </thead>

              <tbody>
                {plan.lessonPlan.map(
                  (item, index) => (
                    <tr
                      key={`${item.unit}-${index}`}
                      className="border-b"
                    >
                      <td className="p-3">
                        {item.unit}
                      </td>

                      <td className="p-3 font-medium">
                        {item.topic}
                      </td>

                      <td className="p-3">
                        {item.hours}
                      </td>

                      <td className="p-3">
                        {item.bloomLevel}
                      </td>

                      <td className="p-3">
                        {item.teachingMethod}
                      </td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>
            Assessment Plan
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-3">
          {plan.assessmentPlan.map(
            (assessment, index) => (
              <div
                key={`${assessment.type}-${index}`}
                className="flex items-center justify-between rounded-lg border p-4"
              >
                <div>
                  <p className="font-medium">
                    {assessment.type}
                  </p>

                  <p className="text-sm text-muted-foreground">
                    {assessment.description}
                  </p>
                </div>

                {assessment.weightage !==
                  undefined && (
                  <span className="font-semibold">
                    {assessment.weightage}%
                  </span>
                )}
              </div>
            ),
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>
            CO-PO Mapping
          </CardTitle>
        </CardHeader>

        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="p-3">
                    Course Outcome
                  </th>

                  <th className="p-3">
                    PO Mappings
                  </th>
                </tr>
              </thead>

              <tbody>
                {plan.coPoMapping.map(
                  (mapping) => (
                    <tr
                      key={mapping.courseOutcome}
                      className="border-b"
                    >
                      <td className="p-3 font-medium">
                        {mapping.courseOutcome}
                      </td>

                      <td className="p-3">
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(
                            mapping.mappings,
                          ).map(
                            ([po, level]) => (
                              <span
                                key={po}
                                className="rounded-md border px-2 py-1"
                              >
                                {po}: {level}
                              </span>
                            ),
                          )}
                        </div>
                      </td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}