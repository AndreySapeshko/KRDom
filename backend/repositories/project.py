from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from backend.db.models.project import Project


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        user_id: UUID | None,
        calculation_id: UUID | None,
        parent_project_id: UUID | None = None,
        status: str = "draft",
    ) -> Project:
        project = Project(
            id=uuid4(),
            user_id=user_id,
            calculation_id=calculation_id,
            parent_project_id=parent_project_id,
            status=status,
        )

        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

        return project
