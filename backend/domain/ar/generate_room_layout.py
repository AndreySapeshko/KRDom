from backend.domain.ar.schemas.room_layout_v2 import RoomLayoutV2
from backend.domain.ar.validators.validate_layout import validate_layout_polygons
from backend.domain.brief.schemas.main_brief import ProjectBriefV1
from backend.llm.open_router_client import get_open_router_client
from backend.llm.prompts.room_layout_prompt_v1 import ROOM_LAYOUT_PROMPT_V1
from backend.llm.prompts.user_layout_prompt import USER_LAYOUT_PROMPT

client = get_open_router_client()


async def generate_room_layout(brief: ProjectBriefV1):
    layout_json = await client.llm_complete_json(
        prompt=ROOM_LAYOUT_PROMPT_V1 + USER_LAYOUT_PROMPT,
        input_data={
            "footprint": [0, 0, 12, 10],
        },
    )

    layout = RoomLayoutV2.model_validate(layout_json)

    issues = validate_layout_polygons(layout, brief.building.footprint.points)

    if issues:
        raise RuntimeError(f"Invalid layout: {issues}")

    return layout
