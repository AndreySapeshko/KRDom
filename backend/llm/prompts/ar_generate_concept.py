AR_GENERATE_CONCEPT = """
You are an architectural planning assistant.

Your task:
Generate a valid ArchitectureConceptV1 JSON from the given ProjectBriefV1.

You MUST return ONLY valid JSON.
No markdown. No comments. No explanations.

------------------------------------------------------------
ArchitectureConceptV1 schema (STRICT):

{
  "version": "1.0",
  "meta": {
    "project_id": "PRJ-001",
    "stage": "AR_CONCEPT",
    "iteration": 1
  },

  "building_geometry": {
    "footprint": {
      "points": [[x, y], ...]  // closed polygon, meters
      }
  },

  "walls": [
    {
      "id": "EW1",
      "kind": "external",      // "external" or "internal"
      "from_point": [x, y],
      "to_point": [x, y],
      "thickness_m": 0.25
    }
  ],

  "openings": [
    {
      "id": "WIN1",
      "type": "window",        // "window" | "door" | "portal"
      "wall_id": "EW1",
      "offset_m": 1.50,
      "width_m": 2.00,
      "height_m": 1.40,
      "sill_height_m": 0.80      // Required only for window.  Do not use for other openings.
    },

    {
      "id": "D1",
      "type": "door",
      "wall_id": "IW1",
      "offset_m": 0.50,
      "width_m": 0.90,
      "height_m": 2.10,
      "hinge_side": "start",      // Required only for doors.  Do not use for other openings. Values: "start" or "end"
      "swing_direction": "in"     // Required only for doors.  Do not use for other openings. Values: "left" or "right"
      "swing_angle_deg": 90.0     // Required only for doors.  Do not use for other openings.
    },

    {
      "id": "P1",
      "type": "portal",
      "wall_id": "IW2",
      "offset_m": 1.00,
      "width_m": 1.20,
      "height_m": 2.10
    }
  ],

  "roof": {
    "type": "gable",
    "pitch_deg": 30,
    "eave_overhang_m": 0.6,
    "gable_overhang_m": 0.6
  }
}

------------------------------------------------------------
Rules (MANDATORY):

1. Output ONLY JSON, nothing else.
2. Do NOT include "rooms" (rooms are computed automatically).
3. External walls must match the footprint polygon edges.
4. Footprint polygon must be closed (first point == last point).
5. Openings must reference existing wall_id.
6. Doors MUST include hinge_side and swing_direction.
7. Portal has NO hinge_side and NO sill_height_m.
8. Geometry must be consistent and buildable.

------------------------------------------------------------
Now generate ArchitectureConceptV1 JSON for this ProjectBriefV1:
"""
