from uuid import UUID

from pydantic import BaseModel


class SearchResultItem(BaseModel):
    id: UUID | None
    title: str
    result_type: str
    target_user_id: UUID | None = None
    score: float
