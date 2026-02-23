from backend.domain.ar.schemas.patch_models import ArchitectureConceptPatchV1

FORBIDDEN_PREFIXES = ["/version", "/meta", "/building_geometry/footprint"]


class PatchSafetyError(Exception):
    pass


def validate_patch_safety(patch: ArchitectureConceptPatchV1):
    """
    Запрещаем LLM менять критические поля.
    """
    for op in patch.operations:

        if op.path.startswith("/concept/"):
            raise PatchSafetyError(f"Invalid patch root: {op.path}. Use /walls not /concept/walls")

        for prefix in FORBIDDEN_PREFIXES:
            if op.path.startswith(prefix):
                raise PatchSafetyError(f"Patch operation forbidden on {prefix}: {op.path}")
