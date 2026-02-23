import json
from pathlib import Path

import pytest

from backend.domain.ar.concept_builder import build_concept
from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.schemas.openings import Opening
from backend.domain.ar.schemas.room_layout_v1 import RoomLayoutV1
from backend.domain.brief.schemas.anchors_layer import AnchorsLayer
from backend.domain.brief.schemas.main_brief import BuildingInfo, ProjectBriefV1, WallSpec
from backend.domain.brief.schemas.polygon import PolygonFootprint
from backend.domain.brief.schemas.required_elements import RequiredElementV1

BASE_DIR = Path(__file__).parent / "concepts"


# ----------------------------
# Load Concept JSON
# ----------------------------


def load_test_concept() -> dict:
    path = BASE_DIR / "concept_test_v2.json"
    if not path.exists():
        raise FileNotFoundError("concept_test_v2.json not found in project root")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_layout_rooms() -> dict:
    path = BASE_DIR / "layout_rooms_test.json"
    if not path.exists():
        raise FileNotFoundError("layout_rooms_test.json not found in project root")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------
# Fixtures
# ----------------------------


@pytest.fixture
def concept_dict():
    return load_test_concept()


@pytest.fixture
def valid_concept() -> ArchitectureConceptV1:
    concept_json = load_test_concept()
    concept = build_concept(concept_json)
    return concept


@pytest.fixture
def layout_rooms():
    layout_json = load_layout_rooms()
    return RoomLayoutV1.model_validate(layout_json)


@pytest.fixture
def concept_missing_window() -> ArchitectureConceptV1:
    concept_json = load_test_concept()

    # удаляем окно WIN1
    concept_json["openings"] = [op for op in concept_json["openings"] if op["id"] != "WIN1"]

    concept = build_concept(concept_json)
    return concept


@pytest.fixture
def empty_brief() -> ProjectBriefV1:
    """
    Минимальный Brief stub.
    Используется когда anchors/required не нужны.
    """
    return ProjectBriefV1(
        version="1.0",
        building=BuildingInfo(
            footprint=PolygonFootprint(
                type="polygon",
                points=[(0.0, 0.0), (12.0, 0.0), (12.0, 8.0), (0.0, 8.0)],
            ),
            floors=1,
            wall_height=2.7,
            wall_spec=WallSpec(structural_type="frame", thickness_m=0.35),
        ),
        anchors=AnchorsLayer(required_elements=[]),
    )


@pytest.fixture
def brief_with_required_window() -> ProjectBriefV1:
    """
    Brief с RequiredElement: окно WIN1 обязательно.
    """
    return ProjectBriefV1(
        version="1.0",
        building=BuildingInfo(
            footprint=PolygonFootprint(
                type="polygon",
                points=[(0.0, 0.0), (12.0, 0.0), (12.0, 8.0), (0.0, 8.0)],
            ),
            floors=1,
            wall_height=2.7,
            wall_spec=WallSpec(structural_type="frame", thickness_m=0.35),
        ),
        anchors=AnchorsLayer(
            required_elements=[
                RequiredElementV1(
                    id="REQ_WIN1",
                    element_type="opening",
                    spec=Opening(
                        id="WIN1",
                        type="window",
                        wall_id="EW1",
                        offset_m=1.6,
                        width_m=2.6,
                        height_m=1.6,
                        sill_height_m=0.4,
                    ),
                )
            ]
        ),
    )
