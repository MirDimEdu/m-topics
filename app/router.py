from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from . import schemas
from . import logic
from .m_utils import get_current_user


router_p = APIRouter(
    prefix='/post'
)

router_p_m = APIRouter(
    prefix='/posts'
)

router_c = APIRouter(
    prefix='/comment'
)


def HTTPanswer(status_code, description):
    return JSONResponse(
        status_code=status_code,
        content={'content': description},
    )


# external routes for manage posts

@router_p.post('/create')
async def create_post(post: schemas.CreatePost,
                      current_user = Depends(get_current_user)):
    post_id = await logic.create_post(current_user.account_id, post.title, post.text)
    return HTTPanswer(201, post_id)


@router_p_m.get('/all')
async def get_all_posts(offset: Optional[int] = Query(None), limit: Optional[int] = Query(None)):
    return await logic.get_all_posts(offset, limit)


@router_p.get('/{post_id}')
async def get_post_info(post_id: int):
    return await logic.get_post_info(post_id)


@router_p.delete('/{post_id}/delete')
async def delete_post(post_id: int,
                      current_user = Depends(get_current_user)):
    await logic.delete_post(current_user.account_id, current_user.role, post_id)
    return HTTPanswer(200, 'Post was deleted')


# external routes for manage comments

@router_p.post('/{post_id}/comment/add')
async def add_comment(post_id: int, comment: schemas.AddComment,
                      current_user = Depends(get_current_user)):
    comment_id = await logic.add_comment(current_user.account_id, post_id, comment.text)
    return HTTPanswer(201, comment_id)


@router_p.get('/{post_id}/comments/all')
async def get_post_comments(post_id: int,
                            offset: Optional[int] = Query(None), limit: Optional[int] = Query(None)):
    return await logic.get_post_comments(post_id, offset, limit)


@router_c.delete('/{comment_id}/delete')
async def delete_comment(comment_id: int,
                         current_user = Depends(get_current_user)):
    await logic.delete_comment(current_user.account_id, current_user.role, comment_id)
    return HTTPanswer(200, 'Comment was deleted')
