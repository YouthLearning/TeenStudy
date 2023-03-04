import re
import time
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from httpx import AsyncClient

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

@route.get("/shanghai/{user_id}/{group_id}", response_class=HTMLResponse)
async def shanghai(user_id: int, group_id: int, appid: str, openid: str, nickname: str, headimg: str, t: str):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        headers = {
            "Host": "qcsh.h5yunban.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Content-Type": "application/json;charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://qcsh.h5yunban.com/youth-learning/signUp.php?rv=2020",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/login/we-chat/callback?appid=wxa693f4127cc93fad&openid={openid}&nickname={nickname}&headimg={headimg}&callback=https://qcsh.h5yunban.com/youth-learning/&scope=snsapi_userinfo"
        async with AsyncClient(headers=headers) as client:
            response = await client.get(url)
        response.encoding = response.charset_encoding
        accessToken = re.findall(r"\(\'accessToken\'\,\s+\'(.+?)\'\)", response.text)[0]
        url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/last-info?accessToken={accessToken}"
        async with AsyncClient(headers=headers) as client:
            response = await client.get(url)
        response.encoding = response.charset_encoding
        result = response.json()
        if result["status"] == 200:
            data = {"dxx_id": result["result"]["nid"], "name": result["result"]["cardNo"], "user_id": user_id,
                    "group_id": group_id, "area": "上海", "openid": openid, "token": nickname, "cookie": headimg,
                    "mobile": result["result"]["subOrg"], "password": ""}
            for item in result["result"]["nodes"]:
                if len(item["id"]) <= 5:
                    data["university_type"] = item["id"]
                elif len(item["id"]) <= 9:
                    data["university_id"] = item["id"]
                    data["university"] = item["title"]
                elif len(item["id"]) <= 13:
                    data["college_id"] = item["id"]
                    data["college"] = item["title"]
                elif len(item["id"]) <= 17:
                    data["organization_id"] = item["id"]
                    data["organization"] = item["title"]
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

    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.get("/zhejiang/{user_id}/{group_id}", response_class=HTMLResponse)
async def zhejiang(user_id: int, group_id: int, appid: str, openid: str, nickname: str, headimg: str, t: str):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        headers = {
            "Host": "qczj.h5yunban.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Content-Type": "application/json;charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        url = f"https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid={openid}&nickname={nickname}&headimg={headimg}&time={int(time.time())}&source=common&sign=&t={int(time.time())}"
        async with AsyncClient(headers=headers) as client:
            response = await client.get(url)
        response.encoding = response.charset_encoding
        accessToken = re.findall(r"\(\'accessToken\'\,\s+\'(.+?)\'\)", response.text)[0]
        url = f"https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/last-info?accessToken={accessToken}"
        async with AsyncClient(headers=headers) as client:
            response = await client.get(url)
        response.encoding = response.charset_encoding
        result = response.json()
        if result["status"] == 200:
            data = {"dxx_id": result["result"]["nid"], "name": result["result"]["cardNo"], "user_id": user_id,
                    "group_id": group_id, "area": "浙江", "openid": openid, "token": nickname, "cookie": headimg,
                    "mobile": result["result"]["subOrg"], "password": ""}
            for item in result["result"]["nodes"]:
                if len(item["id"]) <= 5:
                    data["university_type"] = item["id"]
                elif len(item["id"]) <= 9:
                    data["university_id"] = item["id"]
                    data["university"] = item["title"]
                elif len(item["id"]) <= 13:
                    data["college_id"] = item["id"]
                    data["college"] = item["title"]
                elif len(item["id"]) <= 17:
                    data["organization_id"] = item["id"]
                    data["organization"] = item["title"]
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

    return RedirectResponse(
        url="/TeenStudy/login"
    )

    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return zhejiang_page.render(
            site_title='青春浙江 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )