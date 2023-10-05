from fastapi import APIRouter, Depends, Header
from src.crud import *
from src.database import get_collection
from src.schemas import *
from src.database_models import *

router = APIRouter(tags=["posts"], prefix="/posts")


@router.post("/", response_model=Post)
async def create_post(post: PostCreate, collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await create(post=post, collection=collection)


@router.get("/{post_id}", response_model=Post)
async def get_post_by_id(post_id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await get(post_id=post_id, collection=collection)


@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: str, post: PostUpdate,
                      collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await update(post_id=post_id, post=post, collection=collection)


@router.delete("/{post_id}", response_model=Post)
async def delete_post(post_id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await delete(post_id=post_id, collection=collection)


@router.post("/search", response_model=list[Post])
async def list_posts(
        parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None] = DEFAULT_PARAMETERS,
        collection: AsyncIOMotorCollection = Depends(get_collection)
):
    return await query(collection=collection, parameters=parameters)


@router.post("/count", response_model=int)
async def count_number_of_posts(
        parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None] = DEFAULT_PARAMETERS,
        collection: AsyncIOMotorCollection = Depends(get_collection),
):
    return await count(collection=collection, parameters=parameters)


@router.get("/users/{user_id}", response_model=list[Post])
async def get_posts_by_user(user_id: int,
                            collection: AsyncIOMotorCollection = Depends(get_collection),
                            ):
    return await posts_by_user(user_id=user_id, collection=collection)


@router.get("/users/{user_id}/count", response_model=int)
async def count_posts_by_user(user_id: int,
                              collection: AsyncIOMotorCollection = Depends(get_collection),
                              ):
    return await posts_by_user_count(user_id=user_id, collection=collection)


@router.get("/example/new", response_model=None)
async def test_(header: str | None = Header()):
    return {"header": header}
