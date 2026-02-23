from typing import List, Literal, Optional

from pydantic import BaseModel


class ReviewIssue(BaseModel):
    code: str
    severity: Literal["error", "warning", "info"]
    path: str
    message: str
    suggestion: Optional[str] = None


class ClarificationQuestion(BaseModel):
    id: str
    question: str
    options: Optional[List[str]] = None


class BriefReviewV1(BaseModel):
    version: Literal["1.0"] = "1.0"

    status: Literal["accepted", "needs_clarification", "invalid"]

    issues: List[ReviewIssue] = []
    questions: List[ClarificationQuestion] = []

    summary: Optional[str] = None
