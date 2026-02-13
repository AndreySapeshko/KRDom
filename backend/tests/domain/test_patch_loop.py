from backend.domain.ar.patch_loop import run_patch_cycle
from backend.domain.ar.schemas.patch_models import ArchitectureConceptPatchV1


def test_patch_adds_missing_required_window(concept_missing_window, brief_with_required_window):
    patch = ArchitectureConceptPatchV1.model_validate(
        {
            "version": "1.0",
            "operations": [
                {
                    "op": "add",
                    "path": "/openings/-",
                    "value": {
                        "id": "WIN1",
                        "type": "window",
                        "wall_id": "EW1",
                        "offset_m": 1.6,
                        "width_m": 2.6,
                        "height_m": 1.6,
                        "sill_height_m": 0.4,
                    },
                }
            ],
        }
    )

    result = run_patch_cycle(brief_with_required_window, concept_missing_window, patch)

    updated = result["concept"]
    issues = result["issues"]

    # окно добавлено
    assert any(o.id == "WIN1" for o in updated.openings)

    # issues устранены
    assert issues.issues == []
