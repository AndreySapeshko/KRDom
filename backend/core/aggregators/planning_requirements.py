from backend.api.v1.schemas.calc_input import CalcInputV1
from backend.core.calc.context import InternalWall, Opening
from backend.core.models.planning import PlanningRequirementsV1


def get_planning_requirements_list(input_data: CalcInputV1) -> dict[str:InternalWall]:
    result = {}
    for n, wall in enumerate(input_data.internal_walls, 1):
        openings = {}
        iw = {"length": wall.length, "openings": openings}
        if wall.openings:
            for i, op in enumerate(wall.openings, 1):
                w_op = {"type": op.type, "width": op.width, "height": op.height, "quantity": op.quantity}
                openings[f"opening_{i}"] = w_op
        result[f"internal_wall_{n}"] = iw
    return result


def get_external_openings_list(input_data: CalcInputV1) -> dict[str:Opening]:
    result = {}
    for i, op in enumerate(input_data.external_openings, 1):
        e_op = {"type": op.type, "width": op.width, "height": op.height, "quantity": op.quantity}
        result[f"opening_{i}"] = e_op
    return result


def build_planning_requirements(input_data: CalcInputV1) -> PlanningRequirementsV1:
    return PlanningRequirementsV1(
        version="1.0",
        building={
            "length": input_data.length,
            "width": input_data.width,
            "floors": input_data.total_floors,
        },
        structural_params={
            "wall_height": input_data.wall_height,
            "frame": {
                "stud_spacing": input_data.stud_spacing,
                "wall_section": input_data.wall_section_id,
            },
            "floors": {
                "ground": {
                    "has_ground_overlap": input_data.has_ground_overlap,
                    "joist_spacing": input_data.joist_spacing,
                    "section": input_data.ground_overlap_section_id,
                },
                "interfloor": {
                    "has_interfloor_overlap": input_data.has_interfloor_overlap,
                    "joist_spacing": input_data.joist_spacing,
                    "section": input_data.interfloor_overlap_section_id,
                },
                "attic": {
                    "has_attic_overlap": input_data.has_attic_overlap,
                    "joist_spacing": input_data.joist_spacing,
                    "section": input_data.attic_overlap_section_id,
                },
            },
            "roof": {
                "type": "gable",
                "pitch_deg": input_data.roof_pitch_deg,
                "eave_overhang": input_data.eave_overhang,
                "gable_overhang": input_data.gable_overhang,
                "rafter_spacing": input_data.rafter_spacing,
                "section": input_data.roof_section_id,
                "ties_enabled": input_data.ties_enabled,
            },
            "external_openings": get_external_openings_list(input_data),
        },
        planning_requirements=get_planning_requirements_list(input_data),
        assumptions=[
            "Internal walls positions are not defined at calculator stage.",
            "Internal walls are treated as bearing for material estimation.",
            "Planning decisions are part of project stage, not calculator.",
            "One-floor rectangular frame house.",
            "Only gable roof is supported in v1.0.",
        ],
    )
