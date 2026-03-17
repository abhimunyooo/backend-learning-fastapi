from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    category: str

    def __init__(self, id, title, author, category):
        self.id = id
        self.title = title
        self.author = author
        self.category = category


class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, gt=0, description="ID is not needed to create")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1, max_length=100)
    category: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "book title",
                "author": "name of author",
                "category": "book category"
            }
        }
    }


Books = [
    Book(1, "Harry Potter", "J.K. Rowling", "Fantasy"),
    Book(2, "The Song of Ice & Fire", "George R.R. Martin", "History"),
    Book(3, "Pydantic: for Data Validation", "S.S. Looney", "Computer Science")
]


@app.get("/", status_code=status.HTTP_200_OK)
async def get_status():
    return {"status": "healthy"}


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books(
    limit: int = Query(default=10, gt=0, le=50, description="Number of books to return"),
    offset: int = Query(default=0, ge=0, description="Pagination offset")
):
    return Books[offset: offset + limit]


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(
    id: int = Path(gt=0, description="ID of the book to fetch", example=1)
):
    for book in Books:
        if book.id == id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_author(
    author: str = Query(min_length=1, max_length=100, description="Author name to search")
):
    books_to_return = []

    for book in Books:
        if book.author == author:
            books_to_return.append(book)

    if not books_to_return:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found for this author"
        )

    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    Books.append(find_book_id(new_book))
    return {"message": "Book created successfully"}


def find_book_id(book: Book):
    book.id = len(Books) + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_200_OK)
async def update_book(book: BookRequest):

    if book.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID must be provided for update"
        )

    for i in range(len(Books)):
        if Books[i].id == book.id:
            updated_book = Book(**book.model_dump())
            Books[i] = updated_book
            return {"message": "Book updated successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    id: int = Path(gt=0, description="ID of the book to delete", example=1)
):
    for i in range(len(Books)):
        if Books[i].id == id:
            Books.pop(i)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )