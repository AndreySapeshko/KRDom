from backend.domain.ar.schemas.rooms import Room
from backend.domain.ar.validators.validate_room_requirements import validate_room_requirements
from backend.domain.brief.schemas.intent_layer import RoomRequirement


def test_room_requirements_pass(empty_brief, valid_concept):

    # вручную задаём detected rooms
    valid_concept.detected_rooms = [
        Room(id="R1", net_area_m2=40, centroid=(0, 0), boundary_wall_ids=["EW1", "EW2", "EW3", "IW1"]),
        Room(id="R2", net_area_m2=20, centroid=(0, 0), boundary_wall_ids=["EW1", "EW2", "EW3", "IW1"]),
        Room(id="R3", net_area_m2=18, centroid=(0, 0), boundary_wall_ids=["EW1", "EW2", "EW3", "IW1"]),
    ]

    empty_brief.intent.rooms_required = [
        RoomRequirement(min_area=35, count=1, type="livin_groom"),
        RoomRequirement(min_area=15, count=2, type="bedroom"),
    ]

    issues = validate_room_requirements(empty_brief.intent, valid_concept)

    assert issues == []


def test_room_requirements_fail(empty_brief, valid_concept):

    valid_concept.detected_rooms = [
        Room(id="R1", net_area_m2=30, centroid=(0, 0), boundary_wall_ids=["EW1", "EW2", "EW3", "IW1"]),
        Room(id="R2", net_area_m2=14, centroid=(0, 0), boundary_wall_ids=["EW1", "EW2", "EW3", "IW1"]),
    ]

    empty_brief.intent.rooms_required = [
        RoomRequirement(min_area=35, count=1, type="living_room"),
        RoomRequirement(min_area=15, count=2, type="bedroom"),
    ]

    issues = validate_room_requirements(empty_brief.intent, valid_concept)

    assert len(issues) == 2
