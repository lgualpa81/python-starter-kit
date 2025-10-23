from fastapi import FastAPI, Query, Body, HTTPException, status
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List, Union

app = FastAPI(title="Mini Blog")

BLOG_POST = [
    {"id": 1, "title": "Hola desde FastAPI",
        "content": "Mi primer post con FastAPI"},
    {"id": 2, "title": "Mi segundo Post con FastAPI",
        "content": "Mi segundo post con FastAPI blablabla"},
    {"id": 3, "title": "Django vs FastAPI",
        "content": "FastAPI es más rápido por x razones"},
]


class Tag(BaseModel):
    name: str = Field(..., min_length=2, max_length=30,
                      description="Nombre de la etiqueta")


class Author(BaseModel):
    name: str
    email: EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[Tag]] = []
    author: Optional[Author] = None


class PostCreate(BaseModel):
    title: str = Field(...,
                       min_length=3,
                       max_length=100,
                       description="Titulo del post (minimo 3 caracteres, maximo 100)",
                       examples=["Mi primer post con FastAPI"])
    content: Optional[str] = Field(
        default="Contenido no disponible",
        min_length=10,
        description="contenido del post (minimo 10 caracteres)",
        examples=["Este es un contenido válido porque tiene 10 caracteres o más"]
    )
    tags: List[Tag] = []
    author: Optional[Author] = None

    @field_validator("title")
    @classmethod
    def not_allowed_title(cls, value: str) -> str:
        if "spam" in value.lower():
            raise ValueError("El titulo no puede contener la palabra: 'spam'")
        return value


class PostUpdate(BaseModel):
    title: str
    content: Optional[str] = None


class PostPublic(PostBase):
    id: int


class PostSummary(BaseModel):
    id: int
    title: str


@app.get("/")
def home():
    return {'message': "Bienvenidos a Mini Blog"}


@app.get("/posts", response_model=List[PostPublic])
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por titulo")):
    if query:
        return [post for post in BLOG_POST if query.lower()
                in post["title"].lower()]

    return BLOG_POST


@app.get("/posts/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Post encontrado")
def get_post(post_id: int, include_content: bool = Query(default=True, description="Incluir o no el contenido")):
    post = next((post for post in BLOG_POST if post["id"] == post_id), None)

    if post:
        if not include_content:
            return {"id": post["id"], "title": post["title"]}
        return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Post no encontrado")


@app.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_id = max([p["id"] for p in BLOG_POST], default=0) + 1
    new_post = {"id": new_id,
                "title": post.title,
                "content": post.content,
                "tags": [tag.model_dump() for tag in post.tags],
                "author": post.author.model_dump() if post.author else None
                }

    # Añadir el nuevo post a la lista
    BLOG_POST.append(new_post)
    return new_post


@app.put("/posts/{post_id}", response_model=PostPublic, response_description="Post actualizado")
def update_post(post_id: int, data: PostUpdate):
    for post in BLOG_POST:
        if post["id"] == post_id:
            payload = data.model_dump(exclude_unset=True)  # convierte a dict
            print(type(payload), payload)
            if "title" in payload:
                post["title"] = payload.get("title")
            if "content" in payload:
                post["content"] = payload.get("content")
            return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Post no encontrado")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for index, post in enumerate(BLOG_POST):
        if post["id"] == post_id:
            BLOG_POST.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Post no encontrado")


# https://github.com/DevTalles-corp/fastapi-first-steps/blob/section-5-path-query-params/main.py
# https://fastapi.tiangolo.com/tutorial/body/#use-the-model
# https://www.tutorialspoint.com/fastapi/fastapi_openapi.htm
# https://www.dataquest.io/cheat-sheet/pandas-cheat-sheet/


