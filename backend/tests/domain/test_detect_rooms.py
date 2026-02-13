from backend.domain.ar.detect_rooms import detect_rooms_from_walls
from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.schemas.walls import Wall


def test_detect_rooms_single_space(concept_dict):
    concept = ArchitectureConceptV1.model_validate(concept_dict)

    rooms = detect_rooms_from_walls(
        footprint=concept.building_geometry.footprint.points,
        walls=concept.walls,
    )

    assert len(rooms) == 2
    assert rooms[0].net_area_m2 > 30


def test_detect_rooms_split_by_internal_wall(concept_dict):
    concept = ArchitectureConceptV1.model_validate(concept_dict)

    # добавляем перегородку
    concept.walls.append(Wall(id="IW_NEW", kind="internal", from_point=(0, 4), to_point=(6, 4), thickness_m=0.15))

    rooms = detect_rooms_from_walls(
        footprint=concept.building_geometry.footprint.points,
        walls=concept.walls,
    )

    assert len(rooms) == 3
