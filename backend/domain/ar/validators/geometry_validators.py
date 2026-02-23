from typing import List

from backend.domain.ar.schemas.concept_issues import ConceptIssue
from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.validators.geometry_extra import point_in_polygon


def validate_internal_walls_inside_footprint(
    concept: ArchitectureConceptV1,
) -> List[ConceptIssue]:
    issues = []
    footprint = concept.building_geometry.footprint.points

    for wall in concept.walls:
        if wall.kind != "internal":
            continue

        if not point_in_polygon(wall.from_point, footprint):
            issues.append(
                ConceptIssue(
                    code="INTERNAL_WALL_OUTSIDE",
                    severity="error",
                    path=f"/walls/{wall.id}/from_point",
                    message=f"Internal wall {wall.id} starts outside footprint",
                    hint="Move wall start inside building",
                )
            )

        if not point_in_polygon(wall.to_point, footprint):
            issues.append(
                ConceptIssue(
                    code="INTERNAL_WALL_OUTSIDE",
                    severity="error",
                    path=f"/walls/{wall.id}/to_point",
                    message=f"Internal wall {wall.id} ends outside footprint",
                    hint="Move wall end inside building",
                )
            )

    return issues


def validate_openings_corner_clearance(
    concept: ArchitectureConceptV1,
    min_clearance_m: float = 0.3,
) -> List[ConceptIssue]:
    issues = []

    wall_map = {w.id: w for w in concept.walls}

    for op in concept.openings:
        wall = wall_map[op.wall_id]
        wall_len = wall.length()

        if op.offset_m < min_clearance_m:
            issues.append(
                ConceptIssue(
                    code="OPENING_TOO_CLOSE_TO_CORNER",
                    severity="error",
                    path=f"/openings/{op.id}/offset_m",
                    message=f"Opening {op.id} too close to wall start corner",
                    hint=f"Offset must be >= {min_clearance_m}m",
                )
            )

        if wall_len - (op.offset_m + op.width_m) < min_clearance_m:
            issues.append(
                ConceptIssue(
                    code="OPENING_TOO_CLOSE_TO_CORNER",
                    severity="error",
                    path=f"/openings/{op.id}",
                    message=f"Opening {op.id} too close to wall end corner",
                    hint=f"Leave at least {min_clearance_m}m clearance",
                )
            )

    return issues


def compute_room_adjacency(concept: ArchitectureConceptV1):
    """
    Заполняет adjacency список для каждой комнаты.
    """
    adjacency = {r.id: set() for r in concept.rooms}

    # Пока упрощение: если комнаты имеют одинаковую internal wall в notes
    for wall in concept.walls:
        if wall.kind != "internal":
            continue

        connected_rooms = [r for r in concept.rooms if wall.id in (r.notes or "")]

        for i in range(len(connected_rooms)):
            for j in range(i + 1, len(connected_rooms)):
                r1 = connected_rooms[i].id
                r2 = connected_rooms[j].id
                adjacency[r1].add(r2)
                adjacency[r2].add(r1)

    return adjacency


def run_geometry_validations(concept: ArchitectureConceptV1) -> List[ConceptIssue]:
    issues = []

    issues += validate_internal_walls_inside_footprint(concept)
    issues += validate_openings_corner_clearance(concept)

    return issues
