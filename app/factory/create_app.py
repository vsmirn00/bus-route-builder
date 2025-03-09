from app.routes.info_router.info_router import info_router
from app.routes.health_router.health_router import health_router
from app.routes.builder_router.builder_router import builder_router
from app.routes.frontend_router.frontend_router import frontend_router
from fastapi import FastAPI
from loguru import logger
from app.context_manager.app_lifespan import lifespan


def create_app():

    app = FastAPI(lifespan=lifespan)
    logger.info("Starting application")
    @app.get("/")
    async def root():
        return {"message": "Welcome to the Bus route builder!"}

    # Add routers
    app.include_router(info_router)
    app.include_router(health_router)
    app.include_router(builder_router)
    app.include_router(frontend_router)

    return app