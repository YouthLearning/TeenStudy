from fastapi import APIRouter
from .add import route as add_api
from .login import route as login_api
from .home import route as home_api
from .admin import route as admin_api

BaseApiRouter = APIRouter(prefix="/TeenStudy/api")
BaseApiRouter.include_router(add_api)
BaseApiRouter.include_router(login_api)
BaseApiRouter.include_router(home_api)
BaseApiRouter.include_router(admin_api)
