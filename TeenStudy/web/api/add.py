from typing import Optional

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from ..pages.add import hubei_page, jiangxi_page
from ..utils.add import write_to_database
from ...models.accuont import User, AddUser
from ...models.dxx import JiangXi

route = APIRouter()


@route.post("/add", response_class=JSONResponse)
async def add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        status = await write_to_database(data=data)
        if status:
            return JSONResponse(
                {
                    "status": 0,
                    "msg": "添加成功！"
                }
            )
        else:
            return JSONResponse({
                "status": 500,
                "msg": "添加失败！"
            })


@route.get("/hubei", response_class=HTMLResponse)
async def hubei(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return hubei_page.render(
            site_title='青春湖北 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.get("/jiangxi", response_class=HTMLResponse)
async def jiangxi(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return jiangxi_page.render(
            site_title='江西共青团 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.get("/organization", response_class=JSONResponse)
async def organization(type: str, university: Optional[str] = None, college: Optional[str] = None) -> JSONResponse:
    if type == "jx":
        if university and college == "":
            result = await JiangXi.filter(university=university).values()
            if result:
                options = []
                for item in result:
                    x = {
                        "label": item["college"],
                        "value": item["college"]
                    }
                    if x in options:
                        continue
                    options.append({
                        "label": item["college"],
                        "value": item["college"]
                    })
                return JSONResponse({
                    "status": 0,
                    "msg": "数据加载成功！",
                    "data": {
                        "university": university,
                        "options": options
                    }
                })
        else:
            result = await JiangXi.filter(university=university, college=college).values()
            if result:
                options = []
                for item in result:
                    options.append({
                        "label": item["organization"],
                        "value": item["organization_id"]
                    })
                return JSONResponse({
                    "status": 0,
                    "msg": "数据加载成功！",
                    "data": {
                        "university": university,
                        "options": options,
                    }
                })
    return JSONResponse({
        "status": 0,
        "msg": "数据加载成功！",
        "data": {
            "university": university,
            "options": []
        }
    })
