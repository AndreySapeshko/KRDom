import pytest

from backend.domain.ar.patch_guard import PatchSafetyError, validate_patch_safety
from backend.domain.ar.schemas.patch_models import ArchitectureConceptPatchV1


def test_patch_cannot_modify_version():

    patch = ArchitectureConceptPatchV1.model_validate(
        {"version": "1.0", "operations": [{"op": "replace", "path": "/version", "value": "999"}]}
    )

    with pytest.raises(PatchSafetyError):
        validate_patch_safety(patch)
