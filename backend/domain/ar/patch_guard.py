from backend.domain.ar.schemas.patch_models import ArchitectureConceptPatchV1

FORBIDDEN_PREFIXES = ["/version", "/meta", "/building_geometry/footprint"]


def validate_patch_safety(patch: ArchitectureConceptPatchV1):
    """
    Запрещаем LLM менять критические поля.
    """
    for op in patch.operations:
        for prefix in FORBIDDEN_PREFIXES:
            if op.path.startswith(prefix):
                raise ValueError(f"Patch operation forbidden on {prefix}: {op.path}")
