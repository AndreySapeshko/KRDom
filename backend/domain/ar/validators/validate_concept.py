from typing import List

from backend.domain.ar.schemas.concept_issues import ConceptIssue, ConceptIssuesV1
from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.validators.geometry_validators import run_geometry_validations
from backend.domain.ar.validators.required_elements_validator import validate_required_elements
from backend.domain.ar.validators.validate_room_requirements import validate_room_requirements
from backend.domain.brief.schemas.main_brief import ProjectBriefV1

# ----------------------------
# Main Validation Pipeline
# ----------------------------


def validate_concept(
    brief: ProjectBriefV1,
    concept: ArchitectureConceptV1,
) -> ConceptIssuesV1:
    """
    Главная точка входа для проверки ArchitectureConcept.

    Проверяет:
    1) Exact Anchors (Required Elements)
    2) Geometry correctness
    3) Consistency rules (будет расширяться)

    Возвращает ConceptIssuesV1.
    """

    issues: List[ConceptIssue] = []

    # ----------------------------
    # 1) Required Elements (Anchors)
    # ----------------------------

    issues += validate_required_elements(concept=concept, required=brief.anchors.required_elements)

    issues += validate_room_requirements(brief.intent, concept)

    # ----------------------------
    # 2) Geometry validations
    # ----------------------------

    issues += run_geometry_validations(concept)

    # ----------------------------
    # Final Result
    # ----------------------------

    return ConceptIssuesV1(version="1.0", issues=issues)
