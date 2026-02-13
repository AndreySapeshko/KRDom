from fastapi import APIRouter

from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.validators.validate_concept import validate_concept
from backend.domain.brief.schemas.main_brief import ProjectBriefV1

router = APIRouter()


@router.post("/concept/validate")
async def validate_architecture_concept(
    brief: ProjectBriefV1,
    concept: ArchitectureConceptV1,
):
    issues = validate_concept(brief, concept)

    return issues.model_dump()
