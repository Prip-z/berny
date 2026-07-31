from pydantic import BaseModel, Field


class SearchChannelPayload(BaseModel):
    search_query: str = Field(min_length=3, max_length=50)
