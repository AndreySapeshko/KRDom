from typing import Literal, Union

from pydantic import BaseModel

from backend.domain.ar.schemas.openings import Opening
from backend.domain.ar.schemas.rooms import Room
from backend.domain.ar.schemas.walls import Wall


class RequiredElementV1(BaseModel):
    """
    Exact обязательный элемент.
    LLM обязан вставить объект в Concept без изменений.
    """

    id: str

    element_type: Literal["wall", "opening", "room"]

    spec: Union[Wall, Opening, Room]
