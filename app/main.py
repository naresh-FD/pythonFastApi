from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()

MyPost = []
#     {
#
#         "id": 1,
#         "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
#         "content": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
#     },
#     {
#
#         "id": 2,
#         "title": "qui est esse",
#         "content": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
#     }]

try:
    conn = psycopg2.connect(host='localhost', database='FastapiDB', user='postgres', password='root',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('database connected')
except Exception as error:
    print('DB error')
    print(error)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def findbyid(ids):
    for p in MyPost:
        if p["id"] == ids:
            print(p)
            return p


def find_index(ids):  # type: ignore
    for i, p in enumerate(MyPost):
        if p["id"] == ids:
            print(i)
            return i


@app.get("/")
def root():
    message = {"message": "Welcome to pythons World"}
    return message


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    post = cursor.fetchall()
    return {'data': post}


@app.get("/post/latest")
def get_latest_post():
    post = MyPost[len(MyPost) - 1]
    return {'data': post}


@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    # post = findbyid(id)
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    return {'data': post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(new_post: Post):
    cursor.execute(""" INSERT INTO posts (title , content , published) VALUES (%s , %s, %s) RETURNING * """, (
        new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()
    return {'data': post}


@app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(ids: int):
    index = find_index(ids)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {ids} is not found")
    MyPost.pop(index)  # type: ignore
    return Response(status_code=status.HTTP_201_CREATED)


@app.put("/update-post/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    post_dict = post.dict()
    post_dict['id'] = id
    MyPost[index] = post_dict
    return MyPost

# if __name__ == "__main__":
#     uvicorn.run(app.main:app, host="0.0.0.0", port=8000)

#  ########## uvicorn app.main:app --reload
