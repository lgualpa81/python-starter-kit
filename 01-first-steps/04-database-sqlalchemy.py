import os
import random
from datetime import datetime, timezone
from math import ceil
from dotenv import load_dotenv
from faker import Faker


from fastapi import FastAPI, Query, HTTPException, Path, status, Depends
from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from typing import Optional, List, Union, Literal

from sqlalchemy import create_engine, Integer, String, Text, DateTime, select, func, UniqueConstraint, ForeignKey, Table, Column
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column, relationship, selectinload, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, future=True, **engine_kwargs)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=Session)

fake = Faker()


class Base(DeclarativeBase):
    pass


# Tabla intermedia (n:n), entre entidades (PostORM y TagORM)
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


class AuthorORM(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    # relacion 1:n
    posts: Mapped[List["PostORM"]] = relationship(back_populates="author")


class TagORM(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # relacion n:n
    posts: Mapped[List["PostORM"]] = relationship(
        secondary=post_tags,  # gestionada por la tabla intermedia
        back_populates="tags",
        lazy="selectin"
    )


class PostORM(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("title", name="unique_post_title"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc))

    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Optional["AuthorORM"]] = relationship(
        back_populates="posts")

    tags: Mapped[List["TagORM"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
        lazy="selectin",
        passive_deletes=True
    )


Base.metadata.create_all(bind=engine)  # dev


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Mini blog")


class Tag(BaseModel):
    name: str = Field(..., min_length=2, max_length=30,
                      description="Nombre de la etiqueta")

    model_config = ConfigDict(from_attributes=True)


class Author(BaseModel):
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[Tag]] = Field(default_factory=list)  # []
    author: Optional[Author] = None

    model_config = ConfigDict(from_attributes=True)


class PostCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Titulo del post (mínimo 3 caracteres, máximo 100)",
        examples=["Mi primer post con FastAPI"]
    )
    content: Optional[str] = Field(
        default="Contenido no disponible",
        min_length=10,
        description="Contenido del post (mínimo 10 caracteres)",
        examples=["Este es un contenido válido porque tiene 10 caracteres o más"]
    )
    tags: List[Tag] = Field(default_factory=list)  # []
    author: Optional[Author] = None

    @field_validator("title")
    @classmethod
    def not_allowed_title(cls, value: str) -> str:
        if "spam" in value.lower():
            raise ValueError("El título no puede contener la palabra: 'spam'")
        return value


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = None


class PostPublic(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PostSummary(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedPost(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "title"]
    direction: Literal["asc", "desc"]
    search: Optional[str] = None
    items: List[PostPublic]


@app.get("/")
def home():
    return {'message': "Bienvenidos a Mini Blog"}


@app.get("/generate_fake_data/")
def generate_fake_data(db: Session = Depends(get_db), num_authors: int = 30, num_posts: int = 30):
    # Crear algunos autores de ejemplo
    authors = []
    for _ in range(num_authors):
        authors.append(
            AuthorORM(
                name=fake.name(),
                email=fake.unique.email()
            )
        )

    # Agregar los autores a la base de datos
    db.add_all(authors)
    db.commit()

    # Crear algunas etiquetas de ejemplo
    tags = [
        TagORM(name="Python"),
        TagORM(name="FastAPI"),
        TagORM(name="SQLAlchemy"),
        TagORM(name="Django"),
        TagORM(name="Postgres"),
    ]

    # Agregar las etiquetas a la base de datos
    db.add_all(tags)
    db.commit()

    # Crear algunos posts de ejemplo, asociándolos con autores y etiquetas
    posts = []
    for _ in range(num_posts):
        author = fake.random_element(authors)
        num_tags = random.randint(1, len(tags))
        random_tags = fake.random_elements(
            elements=tags, length=num_tags, unique=True)
        posts.append(
            PostORM(
                title=fake.sentence(nb_words=6),
                content=fake.text(max_nb_chars=100),
                created_at=datetime.now(timezone.utc),
                author_id=author.id,
                tags=random_tags
            )
        )

    # Agregar los posts a la base de datos
    db.add_all(posts)
    db.commit()

    # Retornar una respuesta con éxito
    return {"message": f"{num_authors} autores y {num_posts} posts generados correctamente"}


@app.get("/posts", response_model=PaginatedPost)
def list_posts(
    query: Optional[str] = Query(
        default=None,
        description="Texto para buscar por titulo",
        alias="search",
        min_length=3,
        max_length=50,
        pattern=r"^[\w\sáéíóúÁÉÍÓÚüÜ-]+$"
    ),
    per_page: int = Query(
        10, ge=1, le=50, description="Numero de resultados (1-50)"),
    page: int = Query(1, ge=1, description="Numero de pagina (>=1)"),
    order_by: Literal["id", "title"] = Query(
        "id", description="Campo de orden"),
    direction: Literal["asc", "desc"] = Query(
        "asc", description="Direccion de orden"),
    db: Session = Depends(get_db)
):
    results = select(PostORM)
    if query:
        results = results.where(PostORM.title.ilike(f"%{query}%"))

    total = db.scalar(select(func.count()).select_from(
        results.subquery())) or 0
    total_pages = ceil(total/per_page) if total > 0 else 0
    current_page = 1 if total_pages == 0 else min(page, total_pages)
    order_col = PostORM.id if order_by == "id" else func.lower(PostORM.title)
    results = results.order_by(
        order_col.asc() if direction == "asc" else order_col.desc())
    # results = sorted(
    #     results, key=lambda post: post[order_by], reverse=(direction == 'desc'))
    if total_pages == 0:
        # items = List[PostORM] = [] #genera error cuando no hay datos
        items = []
    else:
        start = (current_page-1)*per_page
        items = db.execute(results.limit(
            per_page).offset(start)).scalars().all()

    has_prev = current_page > 1
    has_next = current_page < total_pages if total_pages > 0 else False

    return PaginatedPost(
        page=current_page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        order_by=order_by,
        direction=direction,
        search=query,
        items=items
    )


@app.get("/posts/by-tags", response_model=List[PostPublic])
def filter_by_tags(
    tags: List[str] = Query(
        ...,
        min_length=1,
        description="Una o más etiquetas. Ejemplo: ?tags=python&tags=fastapi"
    ),
    db: Session = Depends(get_db)
):
    normalized_tag_names = [tag.strip().lower() for tag in tags if tag.strip()]

    if not normalized_tag_names:
        return []

    post_list = (
        select(PostORM)
        .options(
            selectinload(PostORM.tags),
            joinedload(PostORM.author),
        ).where(PostORM.tags.any(func.lower(TagORM.name).in_(normalized_tag_names)))
        .order_by(PostORM.id.asc())
    )

    posts = db.execute(post_list).scalars().all()

    return posts


@app.get("/posts/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Post encontrado")
def get_post(post_id: int = Path(
    ...,
    ge=1,
    title="ID del post",
    description="Identificador entero del post. Debe ser mayor a 1",
    example=1
), include_content: bool = Query(default=True, description="Incluir o no el contenido"), db: Session = Depends(get_db)):

    post_find = select(PostORM).where(PostORM.id == post_id)
    post = db.execute(post_find).scalar_one_or_none()

    # post = db.get(PostORM, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    if include_content:
        return PostPublic.model_validate(post, from_attributes=True)

    return PostSummary.model_validate(post, from_attributes=True)


@app.post("/posts", response_model=PostPublic, response_description="Post creado (OK)", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    author_obj = None
    if post.author:
        author_obj = db.execute(
            select(AuthorORM).where(AuthorORM.email == post.author.email)
        ).scalar_one_or_none()

        if not author_obj:
            author_obj = AuthorORM(name=post.author.name,
                                   email=post.author.email)
            db.add(author_obj)
            db.flush()

    new_post = PostORM(
        title=post.title, content=post.content, author=author_obj)

    for tag in post.tags:
        tag_obj = db.execute(
            select(TagORM).where(TagORM.name.ilike(tag.name))
        ).scalar_one_or_none()
        if not tag_obj:
            tag_obj = TagORM(name=tag.name)
            db.add(tag_obj)
            db.flush()
        new_post.tags.append(tag_obj)

    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="El título ya existe, prueba con otro")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el post")


@app.put("/posts/{post_id}", response_model=PostPublic, response_description="Post actualizado", response_model_exclude_none=True)
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):

    post = db.get(PostORM, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(PostORM, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    db.delete(post)
    db.commit()

    return
