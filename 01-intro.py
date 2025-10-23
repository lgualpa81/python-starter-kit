from fastapi import FastAPI, Query, Body, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Mini Blog")

BLOG_POST = [
    {"id": 1, "title": "Hola desde FastAPI",
        "content": "Mi primer post con FastAPI"},
    {"id": 2, "title": "Mi 2do post con FastAPI",
     "content": "Mi segundo post con FastAPI"},
    {"id": 3, "title": "Django vs FastAPI",
     "content": "FastAPI es mas rapido por x razones"},
]
# ... ellipsis


class Post(BaseModel):
    title: str = Field(..., min_length=1, max_length=100,
                       description="Titulo del post")
    content: str = Field(..., min_length=1, description="Contenido del post")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Datos de entrada inválidos",
                 "errors": exc.errors()},
    )


@app.get("/")
def home():
    return {'message': "Bienvenidos a Mini Blog"}


@app.get("/posts")
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por titulo")):
    '''
    http://localhost:8000/posts?query=django
    http://localhost:8000/docs
    '''
    if query:
        results = [post for post in BLOG_POST if query.lower()
                   in post["title"].lower()]
        return {"data": results, "query": query}
    return {"data": BLOG_POST}


@app.get("/posts/{post_id}")
def get_post(post_id: int, include_content: bool = Query(default=True, description="Incluir o no el contenido")):
    # for post in BLOG_POST:
    #     if post["id"] == post_id:
    #         if not include_content:
    #             return {"id": post["id"], "title": post["title"]}
    #         return {"data": post}
    # Utilizamos next() para buscar el post y evitar recorrer toda la lista
    post = next((post for post in BLOG_POST if post["id"] == post_id), None)

    if post:
        if not include_content:
            return {"id": post["id"], "title": post["title"]}
        return {"data": post}

    return {"error": "Post no encontrado"}


# @app.post("/posts")
# def create_post(post: dict = Body(...)):
#     if "title" not in post or "content" not in post:
#         raise HTTPException(
#             status_code=400, detail="Title y Content son requeridos")
#     title = str(post["title"]).strip()
#     if not title:
#         raise HTTPException(
#             status_code=400, detail="Title no puede estar vacio")
#     content = post["content"].strip()
#     if not content:
#         raise HTTPException(
#             status_code=400, detail="Content no puede estar vacio")

#     new_id = max([p["id"] for p in BLOG_POST], default=0)+1
#     new_post = {"id": new_id, "title": title, "content": content}
#     BLOG_POST.append(new_post)
#     return {"message": "Post creado", "data": new_post}

# pydantic
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_id = max([p["id"] for p in BLOG_POST], default=0) + 1
    # Crear el nuevo post
    new_post = post.model_dump()  # Convertimos el modelo Pydantic a diccionario
    new_post["id"] = new_id

    # Añadir el nuevo post a la lista
    BLOG_POST.append(new_post)
    return {"message": "Post creado", "data": new_post}


@app.put("/posts/{post_id}")
def update_post(post_id: int, data: Post):
    for post in BLOG_POST:
        if post["id"] == post_id:
            if data.title:
                post["title"] = data.title  # data is pydantic model
            if data.content:
                post["content"] = data.content
            return {"message": "Post actualizado", "data": post}

    raise HTTPException(status_code=404, detail="Post no encontrado")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for index, post in enumerate(BLOG_POST):
        if post["id"] == post_id:
            BLOG_POST.pop(index)
            return
    raise HTTPException(status_code=404, detail="Post no encontrado")
