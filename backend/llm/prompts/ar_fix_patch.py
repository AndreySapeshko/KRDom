AR_FIX_PATCH = """
You are correcting an ArchitectureConceptV1 JSON.

Your task:
Return a valid RFC6902 JSON Patch to fix validation issues.

You MUST return ONLY valid JSON.
No markdown. No explanations.

If an issue contains "required_element",
you MUST insert required_element.spec exactly as given.
Do not modify any values.

IMPORTANT:
- Patch is applied to the ROOT object.
- Paths must start with:
  /walls
  /openings
  /roof
  /outputs
- NEVER use "/concept/..." in patch paths.

------------------------------------------------------------
JSON Patch format (STRICT):

{
  "version": "1.0",
  "operations": [
    {
      "op": "replace",
      "path": "/openings/0/offset_m",
      "value": 1.20
    }
  ]
}

Allowed operations:
- "add"
- "replace"
- "remove"

------------------------------------------------------------
Rules (MANDATORY):

1. Output ONLY JSON patch.
2. Apply MINIMAL changes to fix the issues.
3. NEVER modify "/footprint".
4. NEVER change "version".
5. Do NOT delete required openings or walls.
6. Only edit the fields mentioned in validation issues.

------------------------------------------------------------

Validation issues:
The issues are provided in the user input.

Return ONLY the JSON patch now.

Current ArchitectureConceptV1 JSON:
"""
