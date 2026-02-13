from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field


class PatchOperationV1(BaseModel):
    op: Literal["add", "remove", "replace"]
    path: str

    value: Optional[Any] = None


class ArchitectureConceptPatchV1(BaseModel):
    version: Literal["1.0"] = "1.0"

    operations: List[PatchOperationV1] = Field(default_factory=list)
