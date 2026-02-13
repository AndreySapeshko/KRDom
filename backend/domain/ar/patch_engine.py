import jsonpatch

from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.schemas.patch_models import ArchitectureConceptPatchV1


def apply_patch(
    concept: ArchitectureConceptV1,
    patch: ArchitectureConceptPatchV1,
) -> ArchitectureConceptV1:
    """
    Применяет JSON Patch к ArchitectureConcept.

    Возвращает новый объект Concept (immutability).
    """

    concept_dict = concept.model_dump()

    patch_ops = [op.model_dump(exclude_none=True) for op in patch.operations]

    patched_dict = jsonpatch.apply_patch(concept_dict, patch_ops, in_place=False)

    return ArchitectureConceptV1.model_validate(patched_dict)
