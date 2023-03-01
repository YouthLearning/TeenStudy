import nonebot
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from nonebot import get_driver
from nonebot.log import logger

from . import api, pages, utils
from .pages.admin import admin_app
from .pages.home import home_app
from .pages.login import login_page

requestAdaptor = '''
requestAdaptor(api) {
    api.headers["token"] = localStorage.getItem("token");
    api.headers["role"] = localStorage.getItem("role");
    api.headers["user_id"] = localStorage.getItem("user_id");
    return api;
},
'''
responseAdaptor = '''
responseAdaptor(api, payload, query, request, response) {
    if (response.data.detail == '登录验证失败或已失效，请重新登录') {
        window.location.href = '/TeenStudy/login'
        window.localStorage.clear()
        window.sessionStorage.clear()
        window.alert('登录验证失败或已失效，请重新登录')
    }
    return payload
},
'''
DRIVER = get_driver()
icon_path = 'https://i.328888.xyz/2023/02/23/xIh5k.png'


@DRIVER.on_startup
async def init_web():
    app: FastAPI = nonebot.get_app()
    logger.opt(colors=True).info(
        f'<u><y>[大学习提交 Web UI]</y></u><g>启用成功</g>，默认地址为:<m>http://127.0.0.1:{DRIVER.config.port}/TeenStudy/login</m>')
    app.include_router(api.BaseApiRouter)

    @app.get("/TeenStudy/login", response_class=HTMLResponse)
    async def login():
        return login_page.render(
            site_title='TeenStudy | 登录',
            site_icon=icon_path
        )

    @app.get('/TeenStudy/home', response_class=HTMLResponse)
    async def home(user_id: int):
        return home_app.render(
            site_title='TeenStudy 首页',
            site_icon=icon_path,
            requestAdaptor=requestAdaptor,
            responseAdaptor=responseAdaptor
        )

    @app.get("/TeenStudy/admin", response_class=HTMLResponse)
    async def admin():
        return admin_app.render(
            site_title='TeenStudy | 管理后台',
            site_icon=icon_path,
            requestAdaptor=requestAdaptor,
            responseAdaptor=responseAdaptor
        )
