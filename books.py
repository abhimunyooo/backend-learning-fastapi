from fastapi import FastAPI, Body

app = FastAPI()

Books = {
    1: {"name":"book1", "author":"author1","date":"date1"},
    2: {"name":"book2", "author":"author2","date":"date2"},
    3: {"name":"book3", "author":"author3","date":"date3"},
    4: {"name":"book4", "author":"author3","date":"date4"},
    5: {"name":"book5", "author":"author3","date":"date5"},
    6: {"name":"book6", "author":"author3","date":"date6"},
}

@app.get("/")
async def status():
    return {"status":"healthy"}

@app.get("/books")
async def get_all_books():
    return Books

@app.get("/books/")
async def by_authors(author: str):
    results = {}
    for i in Books.keys():
        if(Books[i]["author"]==author):
            results[i]=Books[i]
    return results

@app.get("/books/{num}")
async def get_book_by_id(num: int):
    # num = int(num)
    if(num in Books.keys()):
        return Books[num]
    else:
        return {"status":"not found"}
    
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    Books[len(Books)+1] = new_book

@app.put("/books/{num}")
async def change_by_id(num: int, new_book=Body()):
    if(num in Books.keys()):
        Books[num] = new_book
        return Books[num]
    else:
        return {"status":"not found"}
    
@app.delete("/books/{num}")
async def delete_by_id(num: int):
    del(Books[num])