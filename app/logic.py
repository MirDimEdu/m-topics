import uuid
import httpx
from fastapi import Request
from datetime import datetime, timedelta

from .db import posts, comments
from .db import _database
from .config import cfg
from . import schemas # maybe fix to from .schemas import CurrenUser
from .errors import HTTPabort


async def create_post(account_id, title, text):
    query = posts.insert().values(account_id=account_id, title=title,
                                  text=text, created=datetime.utcnow())
    return await _database.execute(query)


async def get_all_posts(offset, limit):
    query = select(posts).order_by(desc(posts.c.created))
    if offset and limit:
        if offset < 0 or limit < 1:
            HTTPabort(422, 'Offset or limit has wrong values')
        query = query.limit(limit).offset(offset)

    return await _database.fetch_all(query)


async def get_post_info(post_id):
    query = select(posts).where(posts.c.id == post_id)
    
    post = await _database.fetch_one(query)
    if not post:
        HTTPabort(404, 'Post not found')
    return post


@_database.transaction()
async def delete_post(account_id, account_role, post_id):
    query = select(posts).where(posts.c.id == post_id)
    post = await _database.fetch_one(query)
    if not post:
        HTTPabort(404, 'Post not found')
    if account_role not in ['admin', 'moderator'] or account_id != post['account_id']:
        HTTPabort(403, 'Permission denied')
    
    query = comments.delete().where(comments.c.post_id == post_id)
    await _database.execute(query)
    query = posts.delete().where(posts.c.id == post_id)
    await _database.execute(query)



async def add_comment(account_id, post_id, text):
    query = select(posts).where(posts.c.id == post_id)
    post = await _database.fetch_one(query)
    if not post:
        HTTPabort(404, 'Post not found')

    query = comments.insert().values(account_id=account_id, post_id=post_id,
                                     text=text, created=datetime.utcnow())
    return await _database.execute(query)


async def get_post_comments(post_id, offset, limit):
    query = select(posts).where(posts.c.id == post_id)
    post = await _database.fetch_one(query)
    if not post:
        HTTPabort(404, 'Post not found')

    query = select(comments).where(comments.c.post_id == post_id).order_by(desc(comments.c.created))
    
    if offset and limit:
        if offset < 0 or limit < 1:
            HTTPabort(422, 'Offset or limit has wrong values')
        else:
            query = query.limit(limit).offset(offset)

    return await _database.fetch_all(query)


async def delete_comment(account_id, account_role, comment_id):
    query = select(comments).where(comments.c.id == comment_id)
    comment = await _database.fetch_one(query)
    if not comment:
        HTTPabort(404, 'Comment not found')
    if account_role not in ['admin', 'moderator'] or account_id != comment['account_id']:
        HTTPabort(403, 'Permission denied')

    query = comments.delete().where(comments.c.id == comment_id)
    await _database.execute(query)
