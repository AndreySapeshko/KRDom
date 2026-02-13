from backend.domain.ar.schemas.concept_issues import ConceptIssue


def validate_room_requirements(intent, concept):

    rooms = concept.detected_rooms or []

    # площади всех комнат по убыванию
    available = sorted([r.net_area_m2 for r in rooms], reverse=True)

    # требования тоже по убыванию min_area
    requirements = sorted(intent.rooms_required, key=lambda r: r.min_area, reverse=True)

    issues = []

    for req in requirements:

        matched = 0
        still_available = []

        for area in available:
            if area >= req.min_area and matched < req.count:
                matched += 1
            else:
                still_available.append(area)

        if matched < req.count:
            issues.append(
                ConceptIssue(
                    code="ROOM_REQUIREMENT_FAILED",
                    severity="error",
                    path="/walls",
                    message=(f"Required {req.count} rooms " f">= {req.min_area} m², " f"but found only {matched}"),
                )
            )

        # оставшиеся комнаты идут дальше
        available = still_available

    return issues
