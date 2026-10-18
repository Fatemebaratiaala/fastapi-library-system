from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import itertools

app = FastAPI(
    title="Library Management System API",
    description="A simple API for managing books without a database",
    version="1.0.0"
)

class BookBase(BaseModel):
    title: str
    author: str
    year: int
    isbn: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None

class Book(BookBase):
    id: int

books_db: dict[int, Book] = {}
id_counter = itertools.count(1)

@app.get("/books", response_model=List[Book], summary="Get all books")
async def get_all_books():
    return list(books_db.values())

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Create a new book")
async def create_book(book: BookCreate):
    new_id = next(id_counter)
    new_book = Book(id=new_id, **book.model_dump())
    books_db[new_id] = new_book
    return new_book

@app.get("/books/{book_id}", response_model=Book, summary="Get a specific book")
async def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return books_db[book_id]

@app.patch("/books/{book_id}", response_model=Book, summary="Update a specific book")
async def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    stored_book = books_db[book_id]
    update_data = book_update.model_dump(exclude_unset=True)
    updated_book = stored_book.model_copy(update=update_data)
    books_db[book_id] = updated_book
    return updated_book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a specific book")
async def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    del books_db[book_id]
    return None