from fastapi import FastAPI

from .config import cfg
from .config import YamlConfigManager
from .errors import exception_handlers


ConfigManager = YamlConfigManager(interval=60)

app = FastAPI(exception_handlers=exception_handlers)


@app.on_event('startup')
async def startup():
    await ConfigManager.start(cfg)

    from . import db

    await db._database.connect()
    if cfg.STARTUP_DB_ACTION:
        db.create_tables()

    from .router import router_posts, router_posts_multiple, router_comments
    app.include_router(router_posts)
    app.include_router(router_posts_multiple)
    app.include_router(router_comments)


@app.on_event('shutdown')
async def shutdown():
    await db._database.disconnect()
