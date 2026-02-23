from pydantic import ValidationError

from backend.domain.ar.concept_builder import build_concept
from backend.domain.ar.detect_rooms import detect_rooms_from_walls
from backend.domain.ar.patch_engine import apply_patch_to_dict
from backend.domain.ar.patch_guard import PatchSafetyError, validate_patch_safety
from backend.domain.ar.patch_loop import apply_patch
from backend.domain.ar.render.svg_renderer_v2 import SvgRenderOptions, render_concept_to_svg_v2
from backend.domain.ar.schemas.patch_models import ArchitectureConceptPatchV1
from backend.domain.ar.validators.validate_concept import validate_concept
from backend.domain.brief.schemas.main_brief import ProjectBriefV1
from backend.llm.open_router_client import get_open_router_client
from backend.llm.prompts.ar_fix_patch import AR_FIX_PATCH
from backend.llm.prompts.ar_fix_schema_patch import AR_FIX_SCHEMA_PATCH
from backend.llm.prompts.ar_generate_concept import AR_GENERATE_CONCEPT

MAX_ITER = 10
client = get_open_router_client()


def convert_pydantic_error(e: ValidationError) -> list[dict]:
    issues = []
    for err in e.errors():
        issues.append({"loc": list(err["loc"]), "msg": err["msg"], "type": err["type"]})
    return issues


async def generate_valid_concept(brief: ProjectBriefV1):

    # 1) draft generation
    draft_json = await client.llm_complete_json(prompt=AR_GENERATE_CONCEPT, input_data=brief.model_dump())
    concept = None

    for _ in range(3):
        try:
            concept = build_concept(draft_json)

            break
        except ValidationError as e:
            schema_issues = convert_pydantic_error(e)
            patch_json = await client.llm_complete_json(
                prompt=AR_FIX_SCHEMA_PATCH,
                input_data={
                    "raw_json": draft_json,
                    "errors": schema_issues,
                },
            )
            try:
                patch = ArchitectureConceptPatchV1.model_validate(patch_json)
                validate_patch_safety(patch)
                draft_json = apply_patch_to_dict(draft_json, patch)

            except PatchSafetyError as e:
                print("PATCH SAFETY VIOLATION:", e)
                continue

            except ValidationError:
                continue

    if not concept:
        concept = build_concept(draft_json)

    # 2) patch loop
    i = 0
    for _ in range(MAX_ITER):
        i += 1
        svg = render_concept_to_svg_v2(concept, SvgRenderOptions(scale=70))
        with open(f"plan_{i}.svg", "w", encoding="utf-8") as f:
            f.write(svg)

        concept.detected_rooms = detect_rooms_from_walls(concept.building_geometry.footprint.points, concept.walls)

        issues = validate_concept(brief, concept)
        if not issues.issues:
            return concept
        print(f"ISSUES: {issues}")
        patch_json = await client.llm_complete_json(
            prompt=AR_FIX_PATCH,
            input_data={
                "current_concept": concept.model_dump(),
                "issues": [i.model_dump() for i in issues.issues],
            },
        )
        print(f"PATCH_JSON: {patch_json}")

        for _ in range(3):
            try:
                patch = ArchitectureConceptPatchV1.model_validate(patch_json)
                print(f"PATCH: {patch}")
                validate_patch_safety(patch)
                concept = apply_patch(concept, patch)
                break
            except ValidationError:
                continue

            except PatchSafetyError as e:
                print("PATCH SAFETY VIOLATION:", e)
                continue

    raise RuntimeError("LLM could not converge to valid concept")
