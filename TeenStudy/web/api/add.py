import json
import re
import time
import urllib.parse

from bs4 import BeautifulSoup
from ddddocr import DdddOcr
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from httpx import AsyncClient
from nonebot import logger

from ..pages.add import hubei_page, jiangxi_page, anhui_page, sichuan_page, shandong_page, \
    chongqing_page, jilin_page, guangdong_page, beijing_page, tianjin_page
from ..utils.add import write_to_database
from ...models.accuont import User, AddUser
from ...utils.utils import encrypt

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
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
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
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.get("/organization", response_class=JSONResponse)
async def organization(pid: str) -> JSONResponse:
    base_url = f'http://www.jxqingtuan.cn/pub/pub/vol/config/organization?pid={pid}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
    }
    if pid:
        async with AsyncClient(headers=headers) as client:
            response = await client.get(base_url)
        if response.status_code == 200:
            if response.json()["status"] == 200:
                options = []
                for item in response.json()["result"]:
                    x = {
                        "label": item["title"],
                        "value": item["title"] + "-" + item["id"]
                    }
                    if x in options:
                        continue
                    options.append({
                        "label": item["title"],
                        "value": item["title"] + "-" + item["id"]
                    })
                return JSONResponse({
                    "status": 0,
                    "msg": "数据加载成功！",
                    "data": {
                        "options": options
                    }
                })
    return JSONResponse({
        "status": 0,
        "msg": "数据加载成功！",
        "data": {
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
            try:
                data = {"dxx_id": result["result"]["nid"], "name": result["result"]["cardNo"], "user_id": user_id,
                        "group_id": group_id, "area": "上海", "openid": openid, "token": nickname, "cookie": headimg,
                        "mobile": result["result"]["subOrg"], "password": ""}
                for item in result["result"]["nodes"]:
                    if len(item["id"]) <= 5:
                        data["university_type"] = item["id"]
                    if len(item["id"]) <= 9:
                        data["university_id"] = item["id"]
                        data["university"] = item["title"]
                    if len(item["id"]) <= 13:
                        data["college_id"] = item["id"]
                        data["college"] = item["title"]
                    if len(item["id"]) <= 17:
                        data["organization_id"] = item["id"]
                        data["organization"] = item["title"]
            except Exception as e:
                return JSONResponse({"status": 500, "msg": f"请选择好个人信息再重新扫码,错误信息：{e}"})
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
            try:
                data = {"dxx_id": result["result"]["nid"], "name": result["result"]["cardNo"], "user_id": user_id,
                        "group_id": group_id, "area": "浙江", "openid": openid, "token": nickname, "cookie": headimg,
                        "mobile": result["result"]["subOrg"], "password": ""}
                for item in result["result"]["nodes"]:
                    if len(item["id"]) <= 5:
                        data["university_type"] = item["id"]
                    if len(item["id"]) <= 9:
                        data["university_id"] = item["id"]
                        data["university"] = item["title"]
                    if len(item["id"]) <= 13:
                        data["college_id"] = item["id"]
                        data["college"] = item["title"]
                    if len(item["id"]) <= 17:
                        data["organization_id"] = item["id"]
                        data["organization"] = item["title"]
            except Exception as e:
                return JSONResponse({
                    "status": 500,
                    "msg": f"请选择好个人信息再扫码,错误信息：{e}"
                })
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


@route.post("/anhui/add", response_class=JSONResponse)
async def anhui_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 0,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        url = data["url"]
        token = url.split("=")[-1]
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
        try:
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url=url)
            response.encoding = response.charset_encoding
            start = "//从数据库调用"
            end = "this.level1 = one"
            start = response.text.find(start) + 8
            end = response.text.find(end)
            content = response.text[start:end].strip().split("\n")
            username = content[0].split("=")[-1].replace('"', "").strip()
            gender = content[1].split("=")[-1].replace('"', "").strip()
            mobile = content[2].split("=")[-1].replace('"', "").strip()
            level1 = content[3].split("=")[-1].replace('"', "").strip()
            level2 = content[4].split("=")[-1].replace('"', "").strip()
            level3 = content[5].split("=")[-1].replace('"', "").strip()
            level4 = content[6].split("=")[-1].replace('"', "").strip()
            level5 = content[7].split("=")[-1].replace('"', "").strip()
            if level5 == "默认":
                level5 = ""
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
                data.pop("url")
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
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
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
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
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
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
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
                    data["organization"] = content["data"]["user_league_name"]["name4"] + \
                                           content["data"]["user_league_name"]["name5"]
                    data["organization_id"] = content["data"]["league_id"]
                    data["university_type"] = content["data"]["user_league_name"]["name1"]
                    data["university"] = content["data"]["user_league_name"]["name2"]
                    data["college"] = content["data"]["user_league_name"]["name3"]
                    data["college_id"] = content["data"]["league_id4"]
                    data["university_id"] = content["data"]["league_id2"]
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
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/jilin/add", response_class=HTMLResponse)
async def jilin_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 500,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        try:
            openid = data["openid"]
            headers = {
                "Host": "jqfy.jl54.org",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "X-Requested-With": "com.tencent.mm",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            url = "http://jqfy.jl54.org/jltw/wechat/updateStudentInfo"
            params = {
                "openid_u": openid
            }
            async with AsyncClient(headers=headers) as client:
                response = await client.post(url=url, params=params)
            if response.status_code == 200:
                response.encoding = response.charset_encoding
                start = "var studentInfo ="
                end = 'var ctxPath = "\/jltw\/"'
                content = json.loads(
                    response.text[response.text.find(start):response.text.find(end)].split("=")[-1].replace(";",
                                                                                                            "").strip())
                data["mobile"] = content["telNum"]
                data["name"] = content["name"]
                data["organization_id"] = content["typeInfoId"]
                data["dxx_id"] = content["id"]
                data["gender"] = content["sex"]
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
        except Exception as e:
            return JSONResponse({
                "status": 500,
                "msg": f"添加失败,{e}"
            })


@route.get("/jilin", response_class=HTMLResponse)
async def jilin(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return jilin_page.render(
            site_title='吉青飞扬 | TeenStudy',
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/guangdong/add", response_class=HTMLResponse)
async def guangdong_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 500,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        try:
            url = data["url"]
            dxx_id = re.findall(r"memberId=(.*?)&showMemberAdditionNames", url)[0]
            token_headers = {
                'Host': 'tuanapi.12355.net',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'https://tuan.12355.net',
                'User-Agent': 'MicroMessenger',
                'X-Requested-With': 'com.tencent.mm',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Referer': 'https://tuan.12355.net/wechat/view/YouthLearning/page.html',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            ger_param_url = f"https://tuanapi.12355.net/questionnaire/getYouthLearningUrl?mid={dxx_id}"
            async with AsyncClient(headers=token_headers, timeout=30, max_redirects=5) as client:
                param_response = await client.get(url=ger_param_url)
                if param_response.json()["status"] == 200:
                    content = param_response.json()["youthLearningUrl"].split("=")[-1]
                    token_url = "https://youthstudy.12355.net/apih5/api/user/get"
                    token_headers = {
                        'Host': 'youthstudy.12355.net',
                        'Connection': 'keep-alive',
                        'Origin': 'https://youthstudy.12355.net',
                        'X-Litemall-Token': '',
                        'X-Litemall-IdentiFication': 'young',
                        'User-Agent': 'MicroMessenger',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': '*/*',
                        'X-Requested-With': 'com.tencent.mm',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-Mode': 'cors',
                        'Referer': 'https://youthstudy.12355.net/h5/',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                    }
                    async with AsyncClient(headers=token_headers, timeout=30, max_redirects=5) as client:
                        token_response = await client.post(url=token_url, data="sign=" + urllib.parse.quote(content))
                    if token_response.json()["errno"] == 0:
                        token = token_response.json()['data']['entity']['token']
                        name = token_response.json()['data']['entity']['nickName']
                        organization_id = token_response.json()['data']['entity']['organizeId']
                        data["name"] = name
                        data["organization_id"] = organization_id
                        data["dxx_id"] = dxx_id
                        data["token"] = token
                        data.pop("url")
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


@route.get("/guangdong", response_class=HTMLResponse)
async def guangdong(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return guangdong_page.render(
            site_title='广东共青团 | TeenStudy',
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/beijing/add", response_class=HTMLResponse)
async def beijing_add(data: dict) -> JSONResponse:
    user_id = data["user_id"]
    if await User.filter(user_id=user_id).count():
        return JSONResponse({
            "status": 500,
            "msg": "添加失败！，用户信息存在！"
        })
    else:
        token = data["token"]
        cookie = data["cookie"]
        login_url = "https://m.bjyouth.net/site/login"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/113.0.0.0", }
        try:
            async with AsyncClient(headers=headers) as client:
                login_rsp = await client.get(login_url)
                if login_rsp.status_code == 200:
                    login_rsp.encoding = login_rsp.charset_encoding
                    soup = BeautifulSoup(login_rsp.text, "lxml")
                    code_url = "https://m.bjyouth.net" + soup.select("#verifyCode-image")[0].get("src")
                    code_rsp = await client.get(code_url)
                    code_text = DdddOcr(show_ad=False).classification(code_rsp.content)
                    login_response = await client.post(
                        url=login_url,
                        data={
                            '_csrf_mobile': client.cookies['_csrf_mobile'],
                            'Login[password]': await encrypt(token),
                            'Login[username]': await encrypt(cookie),
                            'Login[verifyCode]': code_text
                        }
                    )
                    logger.debug(login_response.text)
                    if login_response.status_code == 200:
                        login_response.encoding = login_response.charset_encoding
                        if login_response.text == '8':
                            return JSONResponse({"status": 500, "msg": "添加失败,验证码错误！"})
                        if 'fail' in login_response.text:
                            return JSONResponse({"status": 500, "msg": "添加失败,账号或密码错误！"})
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
                "msg": f"# 添加失败,{e}"
            })


@route.get("/beijing", response_class=HTMLResponse)
async def beijing(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return beijing_page.render(
            site_title='北京共青团 | TeenStudy',
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )


@route.post("/tianjin/add", response_class=JSONResponse)
async def tianjin_add(data: dict) -> JSONResponse:
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


@route.get("/tianjin", response_class=HTMLResponse)
async def hubei(user_id: int, group_id: int):
    result = await AddUser.filter(user_id=user_id, group_id=group_id, status="未通过").count()
    if result:
        return tianjin_page.render(
            site_title='津彩青春 | TeenStudy',
            site_icon="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
        )
    return RedirectResponse(
        url="/TeenStudy/login"
    )
