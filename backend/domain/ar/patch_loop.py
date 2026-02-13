from backend.domain.ar.patch_engine import apply_patch
from backend.domain.ar.patch_guard import validate_patch_safety
from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.schemas.patch_models import ArchitectureConceptPatchV1
from backend.domain.ar.validators.validate_concept import validate_concept
from backend.domain.brief.schemas.main_brief import ProjectBriefV1


def run_patch_cycle(
    brief: ProjectBriefV1,
    concept: ArchitectureConceptV1,
    patch: ArchitectureConceptPatchV1,
) -> dict:
    """
    Один шаг patch-цикла:

    Concept → ApplyPatch → Validate → Issues
    """

    # 1) Safety guard
    validate_patch_safety(patch)

    # 2) Apply patch
    updated_concept = apply_patch(concept, patch)

    # 3) Revalidate
    issues = validate_concept(brief, updated_concept)

    return {"concept": updated_concept, "issues": issues}
