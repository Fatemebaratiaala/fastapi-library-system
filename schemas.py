from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=150)
    published_year: Optional[int] = Field(default=None, ge=0, le=9999)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=150)
    published_year: Optional[int] = Field(default=None, ge=0, le=9999)


class Book(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
