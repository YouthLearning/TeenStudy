import time
from typing import Optional
import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from nonebot import logger, get_bot
from nonebot.adapters.onebot.v11.bot import Bot

from .login import admin_authentication
from ..utils.status import get_status
from ...models.accuont import Commit, AddUser, User
from ...models.dxx import Answer, PushList
from ...utils.utils import to_hash
from ...utils.path import getConfig, saveConfig

route = APIRouter()


@route.get('/status', response_class=JSONResponse, dependencies=[admin_authentication()])
async def status():
    return await get_status()


@route.delete("/delete_all", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_all(type: str) -> JSONResponse:
    if type == "records":
        await Commit.all().delete()
    elif type == "answers":
        await Answer.all().delete()
    elif type == "requests":
        await AddUser.all().delete()
    else:
        return JSONResponse({"status": 500, "msg": "删除失败！"})
    return JSONResponse({"status": 0, "msg": "删除成功！"})


@route.delete("/delete_record", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_record(id: int) -> JSONResponse:
    try:
        await Commit.filter(id=id).delete()
        return JSONResponse({
            "status": 0,
            "msg": "删除成功！"
        })
    except Exception as e:
        logger.error(e)
        return JSONResponse({
            "status": 500,
            "msg": "删除失败！"
        })


@route.delete("/delete_records", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_records(ids: str) -> JSONResponse:
    for id in ids.split(","):
        await Commit.filter(id=id).delete()
    return JSONResponse({
        "status": 0, "msg": "删除成功！"
    })


@route.delete("/delete_answer", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_answer(id: int) -> JSONResponse:
    try:
        await Answer.filter(id=id).delete()
        return JSONResponse({
            "status": 0,
            "msg": "删除成功！"
        })
    except Exception as e:
        logger.error(e)
        return JSONResponse({
            "status": 500,
            "msg": "删除失败！"
        })


@route.delete("/delete_answers", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_answers(ids: str) -> JSONResponse:
    for id in ids.split(","):
        await Answer.filter(id=id).delete()
    return JSONResponse({"status": 0, "msg": "删除成功！"})


@route.get("/get_settings", response_class=JSONResponse, dependencies=[admin_authentication()])
async def get_answers() -> JSONResponse:
    result = getConfig()
    result["auto"] = time.mktime(datetime.datetime(year=2023, month=1, day=1, hour=result["AUTO_SUBMIT_HOUR"],
                                                   minute=result["AUTO_SUBMIT_MINUTE"], second=0).timetuple())
    result["remind"] = time.mktime(datetime.datetime(year=2023, month=1, day=1, hour=result["DXX_REMIND_HOUR"],
                                                     minute=result["DXX_REMIND_MINUTE"], second=0).timetuple())
    return JSONResponse({"status": 0, "msg": "数据加载成功！", "data": result
                         })


@route.put("/change_settings", response_class=JSONResponse, dependencies=[admin_authentication()])
async def change_settings(data: dict) -> JSONResponse:
    try:
        if data["password"]:
            data["PASSWORD"] = await to_hash(data["password"])
        data["DXX_REMIND_HOUR"] = datetime.datetime.fromtimestamp(float(data["remind"])).hour
        data["DXX_REMIND_MINUTE"] = datetime.datetime.fromtimestamp(float(data["remind"])).minute
        data["AUTO_SUBMIT_HOUR"] = datetime.datetime.fromtimestamp(float(data["auto"])).hour
        data["AUTO_SUBMIT_MINUTE"] = datetime.datetime.fromtimestamp(float(data["auto"])).minute
        data.pop("password")
        data.pop("auto")
        data.pop("remind")
        saveConfig(data=data)
        return JSONResponse({
            "status": 0,
            "msg": "修改成功！"
        })
    except Exception as e:
        logger.error(e)
        return JSONResponse({
            "status": 500,
            "msg": f"修改失败{e}"
        })


@route.delete("/delete_request", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_request(id: int) -> JSONResponse:
    try:
        await AddUser.filter(id=id).delete()
        return JSONResponse({
            "status": 0,
            "msg": "删除成功！"
        })
    except Exception as e:
        logger.error(e)
        return JSONResponse({
            "status": 500,
            "msg": "删除失败！"
        })


@route.delete("/delete_requests", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_requests(ids: str) -> JSONResponse:
    for id in ids.split(","):
        await AddUser.filter(id=id).delete()
    return JSONResponse({
        "status": 0, "msg": "删除成功！"
    })


@route.delete("/delete_answer", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_answer(id: int) -> JSONResponse:
    try:
        await Answer.filter(id=id).delete()
        return JSONResponse({
            "status": 0,
            "msg": "删除成功！"
        })
    except Exception as e:
        logger.error(e)
        return JSONResponse({
            "status": 500,
            "msg": "删除失败！"
        })


@route.get("/get_requests", response_class=JSONResponse, dependencies=[admin_authentication()])
async def get_requests(
        page: int = 1,
        perPage: int = 10,
        orderBy: str = 'time',
        orderDir: str = 'desc',
        group_id: Optional[str] = None,
        user_id: Optional[str] = None,
        area: Optional[str] = None,
        status: Optional[str] = None) -> JSONResponse:
    orderBy = (orderBy or 'time') if (orderDir or 'desc') == 'asc' else f'-{orderBy or "time"}'
    filter_args = {f'{k}__contains': v for k, v in
                   {'group_id': group_id, 'user_id': user_id, "area": area, "status": status}.items() if v}
    return JSONResponse({
        'status': 0,
        'msg': 'ok',
        'data': {
            'items': await AddUser.filter(**filter_args).order_by(orderBy).offset((page - 1) * perPage).limit(
                perPage).values(),
            'total': await AddUser.filter(**filter_args).count()
        }
    })


@route.get("/get_members", response_class=JSONResponse, dependencies=[admin_authentication()])
async def get_members() -> JSONResponse:
    result = await User.all().values()
    return JSONResponse({
        'status': 0,
        'msg': 'ok',
        'data': {
            'rows': result,
            'total': len(result)
        }
    })


@route.delete('/delete_member', response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_member(user_id: int) -> JSONResponse:
    try:
        await User.filter(user_id=user_id).delete()
        return JSONResponse({
            "status": 0,
            "msg": "删除成功！"
        })
    except Exception as e:
        logger.error(e)
        return JSONResponse({
            "status": 500,
            "msg": f"删除失败!{e}"
        })


@route.get("/get_push_list", response_class=JSONResponse, dependencies=[admin_authentication()])
async def get_push_list(
        page: int = 1,
        perPage: int = 10,
        orderBy: str = 'time',
        orderDir: str = 'desc',
        group_id: Optional[str] = None,
        self_id: Optional[str] = None,
        user_id: Optional[str] = None,
        status: Optional[str] = None) -> JSONResponse:
    orderBy = (orderBy or 'time') if (orderDir or 'desc') == 'asc' else f'-{orderBy or "time"}'
    filter_args = {f'{k}__contains': v for k, v in
                   {'group_id': group_id, "user_id": user_id, "self_id": self_id, "status": status}.items() if v}
    return JSONResponse({
        'status': 0,
        'msg': 'ok',
        'data': {
            'items': await PushList.filter(**filter_args).order_by(orderBy).offset((page - 1) * perPage).limit(
                perPage).values(),
            'total': await PushList.filter(**filter_args).count()
        }
    })


@route.get('/get_group_list', response_class=JSONResponse, dependencies=[admin_authentication()])
async def get_group_list() -> JSONResponse:
    try:
        group_list = await get_bot().get_group_list()
        group_list = [{'label': f'{group["group_name"]}({group["group_id"]})', 'value': group['group_id']} for group in
                      group_list]
        return JSONResponse({
            'status': 0,
            'msg': 'ok',
            'data': {"options": group_list}
        })
    except ValueError:
        return JSONResponse({
            'status': 500,
            'msg': '获取群和好友列表失败，请确认已连接go-cqhttp'
        })


@route.get('/get_member_list', response_class=JSONResponse, dependencies=[admin_authentication()])
async def get_member_list(group_id: Optional[str] = None) -> JSONResponse:
    if not group_id:
        return JSONResponse({
            'status': 0,
            'msg': 'ok',
            'data': {"options": []}
        })
    try:
        member_list = await get_bot().get_group_member_list(group_id=int(group_id))
        member_list = [{'label': f'{member["nickname"]}-{member["user_id"]}', 'value': member['user_id']} for member in
                       member_list]
        return JSONResponse({
            'status': 0,
            'msg': 'ok',
            'data': {"options": member_list}
        })
    except ValueError:
        return JSONResponse({
            'status': 500,
            'msg': '获取群和好友列表失败，请确认已连接go-cqhttp'
        })


@route.post("/add_push", response_class=JSONResponse, dependencies=[admin_authentication()])
async def add_push(data: dict) -> JSONResponse:
    bot: Bot = get_bot()
    self_id = int(bot.self_id)
    user_id = self_id
    group_ids = data["groups"]
    for group_id in group_ids:
        try:
            if await PushList.filter(group_id=group_id).count():
                continue
            await PushList.create(
                time=time.time(),
                self_id=self_id,
                user_id=user_id,
                group_id=group_id,
                status=True
            )
        except Exception as e:
            logger.error(e)
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败！{e}"
            })
    return JSONResponse({
        "status": 0,
        "msg": "添加成功！"
    })


@route.delete("/delete_push", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_push(id: int) -> JSONResponse:
    try:
        await PushList.filter(id=id).delete()
        return JSONResponse({
            "status": 0,
            "msg": "删除成功！"
        })
    except Exception as e:
        logger.error(e)
        return JSONResponse({
            "status": 500,
            "msg": "删除失败！"
        })


@route.delete("/delete_pushs", response_class=JSONResponse, dependencies=[admin_authentication()])
async def delete_pushs(ids: str) -> JSONResponse:
    for id in ids.split(","):
        await PushList.filter(id=id).delete()
    return JSONResponse({
        "status": 0, "msg": "删除成功！"
    })
