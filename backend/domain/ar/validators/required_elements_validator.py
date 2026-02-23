from typing import List

from backend.domain.ar.schemas.concept_issues import ConceptIssue
from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.brief.schemas.required_elements import RequiredElementV1


def exact_equal(expected, actual) -> bool:
    """
    Строгое сравнение объектов JSON-to-JSON.
    """
    return expected.model_dump() == actual.model_dump()


def validate_required_elements(
    concept: ArchitectureConceptV1,
    required: List[RequiredElementV1],
) -> List[ConceptIssue]:
    issues: List[ConceptIssue] = []

    for req in required:
        if req.element_type == "opening":
            pool = concept.openings
        elif req.element_type == "wall":
            pool = concept.walls
        elif req.element_type == "room":
            pool = concept.rooms
        else:
            pool = []

        found = any(exact_equal(req.spec, obj) for obj in pool)

        if not found:
            issues.append(
                ConceptIssue(
                    code="REQUIRED_ELEMENT_NOT_FOUND",
                    severity="error",
                    path=f"/anchors/{req.id}",
                    message=f"Required element '{req.id}' is missing.",
                    required_element={"element_type": req.element_type, "spec": req.spec.model_dump()},
                    hint="LLM must insert this object exactly as specified",
                )
            )

    return issues
