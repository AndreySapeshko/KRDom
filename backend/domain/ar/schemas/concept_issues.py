from typing import List, Literal, Optional

from pydantic import BaseModel


class ConceptIssue(BaseModel):
    code: str
    severity: Literal["error", "warning", "info"]
    path: str
    message: str
    hint: Optional[str] = None
    required_element: Optional[dict] = None


class ConceptIssuesV1(BaseModel):
    version: Literal["1.0"] = "1.0"
    issues: List[ConceptIssue] = []
