SYSTEM_PROMPT = """
You are Academic Co-Pilot, an AI academic planning assistant.

You help university faculty create academically structured
course plans.

Your responsibilities include:

1. Creating course outcomes.
2. Creating semester-wise lesson plans.
3. Aligning learning objectives with Bloom's taxonomy.
4. Suggesting appropriate teaching methods.
5. Suggesting assessment methods.
6. Creating CO-PO mappings.

Important rules:

- Do not invent university-specific regulations.
- Use only the information provided in the request.
- If required information is missing, make a reasonable
  academic assumption and clearly reflect it.
- Keep course outcomes measurable.
- Use action verbs appropriate to Bloom's taxonomy.
- Ensure the lesson plan is realistic for the available
  hours per week.
- Return a single JSON object matching the requested schema.
- Do not return Markdown.
- Do not wrap the JSON in code fences.
- Do not include explanations outside the JSON object.
"""


def build_user_prompt(course: dict) -> str:
    return f"""
Create an academic plan for the following course:

Subject:
{course.get("subject")}

Course Code:
{course.get("courseCode")}

Branch:
{course.get("branch")}

Semester:
{course.get("semester")}

Course Role:
{course.get("courseRole")}

Credits:
{course.get("credits")}

Hours Per Week:
{course.get("hoursPerWeek")}

University:
{course.get("university")}

Regulation:
{course.get("regulation")}

Additional Requirements:
{course.get("additionalRequirements")}

Return JSON with exactly this structure:

{{
  "courseOverview": "string",

  "courseOutcomes": [
    {{
      "code": "CO1",
      "description": "string"
    }}
  ],

  "lessonPlan": [
    {{
      "unit": "Unit 1",
      "topic": "string",
      "hours": 4,
      "learningObjectives": [
        "string"
      ],
      "teachingMethod": "string",
      "bloomLevel": "Remember"
    }}
  ],

  "assessmentPlan": [
    {{
      "type": "string",
      "description": "string",
      "weightage": 10
    }}
  ],

  "coPoMapping": [
    {{
      "courseOutcome": "CO1",
      "mappings": {{
        "PO1": "3",
        "PO2": "2"
      }}
    }}
  ]
}}
"""