import re
import time
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from httpx import AsyncClient

from ..pages.add import hubei_page, jiangxi_page, jiangsu_page, anhui_page, henan_page, sichuan_page, shandong_page, \
    chongqing_page
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


@route.post("/jiangsu/add", response_class=JSONResponse)
async def jiangsu_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        cookie = data["cookie"]
        headers = {
            "Host": "service.jiangsugqt.org",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": '1',
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "X-Requested-With": "com.tencent.mm",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Referer": "https://service.jiangsugqt.org/youth-h5/",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookie
        }
        try:
            url = "https://service.jiangsugqt.org/api/my"
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url)
            response.encoding = response.charset_encoding
            result = response.json()
            if result["status"] == 1:
                data["dxx_id"] = result["data"]["user_id"]
                data["name"] = result["data"]["username"]
                if result["data"]["orga"]:
                    data["university"] = result["data"]["orga"].split("-")[0].strip()[:-2]
                    if "学院" in result["data"]["orga"].split("-")[1].strip():
                        data["college"] = result["data"]["orga"].split("-")[1].strip()
                    else:
                        data["college"] = result["data"]["orga"].split("-")[-1].strip()
                else:
                    data["university"] = ""
                    data["college"] = ""
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
            else:
                return JSONResponse({
                    "status": 500,
                    "msg": "添加失败！"
                })
        except Exception as e:
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败!{e}"
            })


@route.get("/jiangsu", response_class=HTMLResponse)
async def jiangsu(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return jiangsu_page.render(
            site_title='江苏共青团 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/anhui/add", response_class=JSONResponse)
async def anhui_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        username = data['name']
        gender = data['gender']
        mobile = data['mobile']
        level1 = data['university_type']
        level2 = data['university']
        level3 = data['college']
        level4 = data['organization']
        level5 = data['organization_id']
        token = data["token"]
        headers = {
            "Host": "dxx.ahyouth.org.cn",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3234 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "http://dxx.ahyouth.org.cn/",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Content-Type': 'application/x-www-form-urlencoded',
            "X-Requested-With": 'com.tencent.mm',
            "Origin": 'http://dxx.ahyouth.org.cn',
            "token": token
        }
        params = {
            'username': username,
            'gender': gender,
            'mobile': mobile,
            'level1': level1,
            'level2': level2,
            'level3': level3,
            'level4': level4,
            'level5': level5
        }
        try:
            get_infor_url = 'http://dxx.ahyouth.org.cn/api/saveUserInfo'
            async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                infor_response = await client.post(url=get_infor_url, params=params)
            infor_response.encoding = infor_response.charset_encoding
            infor_response_json = infor_response.json()
            if infor_response_json['code'] == 200:
                data["name"] = infor_response_json['content']['username']
                data["token"] = infor_response_json['content']['token']
                data["gender"] = infor_response_json['content']['gender']
                data["mobile"] = infor_response_json['content']['mobile']
                data['university_type'] = infor_response_json['content']['level1']
                data['university'] = infor_response_json['content']['level2']
                data['college'] = infor_response_json['content']['level3']
                data['organization'] = infor_response_json['content']['level4']
                data['organization_id'] = infor_response_json['content']['level5']
                data["openid"] = infor_response_json["content"]["openid"]
                data["dxx_id"] = infor_response_json["content"]["id"]
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
            else:
                return JSONResponse({
                    "status": 500,
                    "msg": "添加失败！"
                })
        except Exception as e:
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败!{e}"
            })


@route.get("/anhui", response_class=HTMLResponse)
async def jiangsu(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return anhui_page.render(
            site_title='安徽共青团 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/henan/add", response_class=HTMLResponse)
async def henan_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        cookie = data["cookie"]
        headers = {
            "Host": "hnqndaxuexi.dahejs.cn",
            "Connection": "keep-alive",
            "Content-Length": "2",
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Content-Type": "application/json",
            "Origin": "http://hnqndaxuexi.dahejs.cn",
            "X-Requested-With": "com.tencent.mm",
            "Referer": "http://hnqndaxuexi.dahejs.cn/study/personalSet",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookie
        }
        params = {}
        try:
            get_user_info_url = "http://hnqndaxuexi.dahejs.cn/stw/front-user/info"
            async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                infor_response = await client.post(url=get_user_info_url, json=params)
            if infor_response.status_code == 200:
                infor_response.encoding = infor_response.charset_encoding
                infor_response_json = infor_response.json()
                if infor_response_json["result"] == 200:
                    data["name"] = infor_response_json["obj"]["trueName"]
                    data["openid"] = infor_response_json["obj"]["openId"]
                    data["dxx_id"] = infor_response_json["obj"]["id"]
                    data["gender"] = infor_response_json["obj"]["gender"]
                    data["mobile"] = infor_response_json["obj"]["phone"]
                    data["university_id"] = infor_response_json["obj"]["orgArrList"][0]["id"]
                    data["university"] = infor_response_json["obj"]["orgArrList"][0]["name"]
                    data["college_id"] = infor_response_json["obj"]["orgArrList"][1]["id"]
                    data["college"] = infor_response_json["obj"]["orgArrList"][1]["name"]
                    data["organization_id"] = infor_response_json["obj"]["orgType"]
                    data["organization"] = infor_response_json["obj"]["clazz"]
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
                else:
                    return JSONResponse({
                        "status": 500,
                        "msg": "添加失败，cookie无效"
                    })
            else:
                return JSONResponse({"status": 500, "msg": "添加失败，cookie无效！"})
        except Exception as e:
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败!{e}"
            })


@route.get("/henan", response_class=HTMLResponse)
async def henan(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return henan_page.render(
            site_title='河南共青团 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/sichuan/add", response_class=HTMLResponse)
async def sichuan_add(result: dict) -> JSONResponse:
    user_id = result["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        try:
            data = {"name": result["name"], "mobile": result["mobile"], "dxx_id": result["org"].split("#")[1],
                    "university_type": result["allOrgName"].split("#")[1], "university_id": result["org"].split("#")[2],
                    "university": result["allOrgName"].split("#")[2], "college_id": result["org"].split("#")[3],
                    "college": result["allOrgName"].split("#")[3], "organization_id": result["org"].split("#")[4],
                    "organization": result["allOrgName"].split("#")[4], "password": result["password"], "area": "四川",
                    "group_id": result["group_id"], "user_id": result["user_id"], "token": result["token"]}
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
        except Exception as e:
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败,{e}"
            })


@route.get("/sichuan", response_class=HTMLResponse)
async def sichuan(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return sichuan_page.render(
            site_title='天府新青年 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/shandong/add", response_class=HTMLResponse)
async def shandong_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        try:
            openid = data["openid"]
            cookie = data["cookie"]
            headers = {
                "Host": "qndxx.youth54.cn",
                "Connection": "keep-alive",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3234 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "http://qndxx.youth54.cn",
                "Referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=enterIndexPage&fxopenid=&fxversion=",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cookie": cookie
            }
            url = "http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getUserBasicInfo"
            data_json = {
                "openid": openid
            }
            async with AsyncClient(headers=headers) as client:
                response = await client.post(url=url, params=data_json)
            if response.status_code == 200:
                response.encoding = response.charset_encoding
                content = response.json()
                if content["errcode"] == "0":
                    data["mobile"] = content["sjh"]
                    data["name"] = content["xm"]
                    data["organization"] = content["tzzmc"]
                    data["organization_id"] = content["tzzbh"]
                    data["university_type"] = content["tzzxx"].split(",")[0]
                    data["university"] = content["tzzxx"].split(",")[1]
                    data["college"] = content["tzzxx"].split(",")[2]
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
                else:
                    return JSONResponse({"status": 500, "msg": "添加失败！"})
            else:
                return JSONResponse({"status": 500, "msg": "添加失败！"})
        except Exception as e:
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败,{e}"
            })


@route.get("/shandong", response_class=HTMLResponse)
async def shandong(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return shandong_page.render(
            site_title='青春山东 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/chongqing/add", response_class=HTMLResponse)
async def chongqing_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        try:
            openid = data["openid"]
            headers = {
                "Host": "qndxx.cqyouths.com",
                "Connection": "keep-alive",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                "X-Requested-With": "com.tencent.mm",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            url = f"http://qndxx.cqyouths.com/api/user/userInfo?openid={openid}"
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url=url)
            if response.status_code == 200:
                response.encoding = response.charset_encoding
                content = response.json()
                if content["status"] == 200:
                    data["mobile"] = content["data"]["mobile"]
                    data["name"] = content["data"]["real_name"]
                    data["organization"] = content["data"]["user_league_name"]["name4"]+content["data"]["user_league_name"]["name5"]
                    data["organization_id"] = content["data"]["league_id"]
                    data["university_type"] = content["data"]["user_league_name"]["name1"]
                    data["university"] = content["data"]["user_league_name"]["name2"]
                    data["college"] = content["data"]["user_league_name"]["name3"]
                    data["college_id"]=content["data"]["league_id4"]
                    data["university_id"]=content["data"]["league_id2"]
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
                else:
                    return JSONResponse({"status": 500, "msg": "添加失败！"})
            else:
                return JSONResponse({"status": 500, "msg": "添加失败！"})
        except Exception as e:
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败,{e}"
            })


@route.get("/chongqing", response_class=HTMLResponse)
async def chongqing(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return chongqing_page.render(
            site_title='重庆共青团 | TeenStudy',
            site_icon="https://i.328888.xyz/2023/02/23/xIh5k.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )
