AR_FIX_SCHEMA_PATCH = """
You are fixing invalid ArchitectureConceptV1 JSON.

The JSON failed Pydantic schema validation.

Return ONLY an RFC6902 JSON Patch that fixes missing or invalid fields.

IMPORTANT:
- Patch is applied to the ROOT object.
- Paths must start with:
  /walls
  /openings
  /roof
  /outputs
- NEVER use "/concept/..." in patch paths.

Rules:
- Output ONLY JSON patch
- Do not modify footprint unless required
- Fix only the fields mentioned in errors

Example:
{
  "version": "1.0",
  "operations": [
    {"op": "add", "path": "/meta", "value": {...}}
  ]
}

Invalid JSON:
...

Schema errors:
...

"""
