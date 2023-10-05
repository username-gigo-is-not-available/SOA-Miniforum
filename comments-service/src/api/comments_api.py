from fastapi import APIRouter, Depends
from src.database import get_collection
from src.crud import *
from src.schemas import *
from src.database_models import *

router = APIRouter(tags=["comments"], prefix="/comments")


@router.post("/", response_model=Comment)
async def create_comment(comment: CommentCreate, collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await create(comment=comment, collection=collection)


@router.get("/{comment_id}", response_model=Comment)
async def get_comment_by_id(comment_id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await get(comment_id=comment_id, collection=collection)


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(comment_id: str, comment: CommentUpdate,
                         collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await update(comment_id=comment_id, comment=comment, collection=collection)


@router.delete("/{comment_id}", response_model=Comment)
async def delete_comment(comment_id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await delete(comment_id=comment_id, collection=collection)


@router.post("/search", response_model=list[Comment])
async def list_comments(
        parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None] = DEFAULT_PARAMETERS,
        collection: AsyncIOMotorCollection = Depends(get_collection)
):
    return await query(collection=collection, parameters=parameters)


@router.post("/count", response_model=int)
async def count_number_of_comments(
        parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None] = DEFAULT_PARAMETERS,
        collection: AsyncIOMotorCollection = Depends(get_collection),
):
    return await count(collection=collection, parameters=parameters)


@router.get("/posts/{post_id}", response_model=list[Comment])
async def get_comments_by_post(post_id: str,
                               collection: AsyncIOMotorCollection = Depends(get_collection),
                               ):
    return await comments_by_post(post_id=post_id, collection=collection)


@router.get("/posts/{post_id}/count", response_model=int)
async def count_comments_by_post(post_id: str,
                                 collection: AsyncIOMotorCollection = Depends(get_collection),
                                 ):
    return await comments_by_post_count(post_id=post_id, collection=collection)


@router.get("/users/{user_id}", response_model=list[Comment])
async def get_comments_by_user(user_id: int,
                               collection: AsyncIOMotorCollection = Depends(get_collection)
                               ):
    return await comments_by_user(user_id=user_id, collection=collection)


@router.get("/users/{user_id}/count", response_model=int)
async def count_comments_by_user(user_id: int,
                                 collection: AsyncIOMotorCollection = Depends(get_collection),
                                 ):
    return await comments_by_user_count(user_id=user_id, collection=collection)
