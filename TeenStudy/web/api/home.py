import datetime
from typing import Optional

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from .login import authentication, get_userInfo
from ...models.accuont import User, Commit
from ...models.dxx import Answer
from ...utils.rule import check_time
from ...utils.utils import distribute_area
from ...utils.utils import to_hash

route = APIRouter()


@route.get("/get_user", response_class=JSONResponse, dependencies=[authentication()])
async def get_user(token: Optional[str] = Header(...)) -> JSONResponse:
    userinfo = await get_userInfo(token=token)
    user_id = userinfo["user_id"]
    result = await User.filter(user_id=user_id).values()
    if result:
        data = result[0]
        try:
            data["commit_time"] = datetime.datetime.fromtimestamp(data['commit_time']).strftime(
                "%Y-%m-%d %H:%M:%S")
        except TypeError:
            data["commit_time"] = "暂未提交"
        if data["catalogue"] is None:
            data["catalogue"] = "暂未提交"
        return JSONResponse(
            data)


@route.put("/change", response_class=JSONResponse, dependencies=[authentication()])
async def change(user_id: int, data: dict) -> JSONResponse:
    if await User.filter(user_id=user_id).values():
        password = data["Password"]
        if password:
            data["password"] = await to_hash(password)
        data.pop("Password")
        if data["leader"] == "":
            data["leader"] = None
        await User.filter(user_id=user_id).update(**data)
        return JSONResponse({
            "status": 0,
            "msg": "修改成功！"
        })
    else:
        return JSONResponse({
            "status": 422,
            "msg": "用户不存在！"
        })


@route.get("/get_records", response_class=JSONResponse, dependencies=[authentication()])
async def get_records(
        token: Optional[str] = Header(...),
        page: int = 1,
        perPage: int = 10,
        orderBy: str = 'time',
        orderDir: str = 'desc',
        group_id: Optional[str] = None,
        user_id: Optional[str] = None,
        name: Optional[str] = None,
        college: Optional[str] = None,
        organization: Optional[str] = None,
        catalogue: Optional[str] = None,
        status: Optional[str] = None,
        area: Optional[str] = None
) -> JSONResponse:
    userinfo = await get_userInfo(token=token)
    if not user_id:
        if userinfo["role"]:
            user_id = ""
        else:
            user_id = userinfo["user_id"]
    orderBy = (orderBy or 'time') if (orderDir or 'desc') == 'asc' else f'-{orderBy or "time"}'
    filter_args = {f'{k}__contains': v for k, v in
                   {'group_id': group_id, 'user_id': user_id, "area": area, "name": name, "college": college,
                    "organization": organization, "catalogue": catalogue, "status": status}.items() if v}
    return JSONResponse({
        'status': 0,
        'msg': 'ok',
        'data': {
            'items': await Commit.filter(**filter_args).order_by(orderBy).offset((page - 1) * perPage).limit(
                perPage).values(),
            'total': await Commit.filter(**filter_args).count()
        }
    })


@route.get('/get_answers', response_class=JSONResponse, dependencies=[authentication()])
async def get_answers(page: int = 1,
                      perPage: int = 10,
                      orderBy: str = 'time',
                      orderDir: str = 'desc',
                      catalogue: Optional[str] = None
                      ) -> JSONResponse:
    orderBy = (orderBy or 'time') if (orderDir or 'desc') == 'asc' else f'-{orderBy or "time"}'
    filter_args = {f'{k}__contains': v for k, v in
                   {'catalogue': catalogue}.items() if v}
    items = await Answer.filter(**filter_args).order_by(orderBy).offset((page - 1) * perPage).limit(
        perPage).values()
    for item in items:
        item.pop("cover")
    return JSONResponse({
        'status': 0,
        'msg': 'ok',
        'data': {
            'items': items,
            'total': await Answer.filter(**filter_args).count()
        }
    })


@route.get('/commit', response_class=JSONResponse, dependencies=[authentication()])
async def commit(user_id: int, area: str) -> JSONResponse:
    if not await check_time():
        return JSONResponse({
            "status": 500,
            "msg": "当前时间段禁止提交青年大学习，请在周一11:00之后再提交哦(｡･ω･｡)"
        })
    data = await distribute_area(user_id=user_id, area=area)
    return JSONResponse({
        "status": data["status"],
        "msg": data["msg"]
    })


@route.put("/set_auto_submit", response_class=JSONResponse, dependencies=[authentication()])
async def set_auto_submit(data: dict) -> JSONResponse:
    await User.filter(id=data["id"]).update(auto_submit=data["status"])
    return JSONResponse({"status": 0})
