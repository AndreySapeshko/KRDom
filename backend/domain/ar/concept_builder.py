from backend.domain.ar.detect_rooms import detect_rooms_from_walls
from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1


def build_concept(concept_json: dict) -> ArchitectureConceptV1:
    """
    Validates raw JSON and enriches it with detected rooms.
    """

    concept = ArchitectureConceptV1.model_validate(concept_json)

    # вычисляем комнаты автоматически
    rooms = detect_rooms_from_walls(
        footprint=concept.building_geometry.footprint.points,
        walls=concept.walls,
    )

    concept.detected_rooms = rooms

    return concept
