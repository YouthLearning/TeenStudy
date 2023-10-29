import json
import re
import secrets
import time
import urllib.parse
from typing import Optional

from anti_useragent import UserAgent
from bs4 import BeautifulSoup
from ddddocr import DdddOcr
from httpx import AsyncClient
from nonebot import logger

from .utils import encrypt
from ..models.accuont import User, Commit
from ..models.dxx import Answer, JiangXiDxx, ShanDongDxx, ShanXiDxx

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': UserAgent(platform="iphone", min_version=1, max_version=5).wechat,
    'X-Requested-With': 'XMLHttpRequest'
}


async def commit(user_id: int, catalogue: str, status: bool = False) -> None:
    """
    记录提交状态
    :param catalogue: 提交期数
    :param user_id: 用户ID
    :param status:提交状态，默认为False
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    await Commit.create(
        time=time.time(),
        user_id=user_id,
        area=result[0]["area"],
        status=status,
        name=result[0]["name"],
        university=result[0]["university"],
        college=result[0]["college"],
        organization=result[0]["organization"],
        catalogue=catalogue
    )


async def hubei(user_id: int, catalogue: Optional[str] = None) -> dict:
    """
    青春湖北
    :param catalogue: 期数
    :param user_id:用户ID
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        if not catalogue:
            resp_url = 'https://h5.cyol.com/special/weixin/sign.json'
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url=resp_url, timeout=10)
            response.encoding = response.charset_encoding
            result = response.json()
            code_result = list(result)[-1]
            answer = await Answer.filter(code=code_result).values()
            catalogue = answer[-1]["catalogue"]
        name = result[0]["name"]
        openid = result[0]["openid"]
        university = result[0]["university"]
        college = result[0]["college"]
        organization = result[0]["organization"]
        headers.update({
            "Host": "cp.fjg360.cn",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        url = "https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="
        url += "&username=" + name
        url += "&phone=" + "未知"
        url += "&city=" + university
        url += "&danwei2=" + organization
        url += "&danwei=" + college
        url += "&openid=" + openid
        url += "&num=10"
        url += "&lesson_name=" + catalogue
        try:
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url)
            response_json = json.loads(response.text)
            if response_json.get('code') == 1:
                await User.filter(user_id=user_id).update(
                    commit_time=time.time(),
                    catalogue=catalogue
                )
                await commit(user_id=user_id, catalogue=catalogue, status=True)
                return {
                    "status": 0,
                    "catalogue": catalogue,
                    "msg": "提交成功！"
                }
            else:
                await commit(user_id=user_id, catalogue=catalogue, status=False)
                return {
                    "status": 500,
                    "msg": "提交失败！"
                }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=catalogue, status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
            }


async def jiangxi(user_id: int, catalogue: Optional[str] = None) -> dict:
    """
    江西共青团
    :param catalogue:
    :param user_id:用户ID
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if catalogue:
        filterArg = {
            "title": catalogue
        }
    else:
        filterArg = {}
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        name = result[0]["name"]
        nid = result[0]["dxx_id"]
        openid = result[0]["openid"]
        token = result[0]["token"]
        if result[0]["mobile"]:
            suborg = result[0]["mobile"]
        else:
            suborg = ''
        code = await JiangXiDxx.filter(**filterArg).order_by("code").values()
        if not code:
            return {
                "status": 404,
                "msg": f"江西共青团没有找到青年大学习{catalogue}"
            }
        try:
            headers.update({
                'Cookie': 'JSESSIONID=' + secrets.token_urlsafe(40),
                'Host': 'www.jxqingtuan.cn',
                'Origin': 'http://www.jxqingtuan.cn',
                'Referer': 'http://www.jxqingtuan.cn/html/h5_index.html?&accessToken=' + openid,
                'openid': openid
            })
            async with AsyncClient(headers=headers) as client:
                course = code[-1]["code"]
                resp_url = 'http://www.jxqingtuan.cn/pub/pub/vol/volClass/join?accessToken='
                data = {"course": course, "nid": nid, "cardNo": name, "subOrg": suborg}
                res = await client.post(url=resp_url, json=data)
                res.encoding = res.charset_encoding
                resp = json.loads(res.text)
                if resp.get("status") == 200:
                    await User.filter(user_id=user_id).update(
                        commit_time=time.time(),
                        catalogue=catalogue
                    )
                    await commit(user_id=user_id, catalogue=catalogue, status=True)
                    data = {
                        "check": 1,
                        "type": 3,
                        "title": "青年大学习",
                        "url": code[-1]['url'],
                        "openid": openid,
                        "userId": token
                    }
                    response = await client.post('http://www.jxqingtuan.cn/pub/pub/vol/member/addScoreInfo',
                                                 params=data)
                    if response.json()["code"] == "200" or response.json()["code"] == "-1":
                        return {
                            "status": 0,
                            "catalogue": catalogue,
                            "msg": "提交成功！"
                        }
                    return {
                        "status": 0,
                        "catalogue": catalogue,
                        "msg": "提交成功！"
                    }
                else:
                    await commit(user_id=user_id, catalogue=catalogue, status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败,信息错误！"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=catalogue, status=False)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def zhejiang(user_id: int) -> dict:
    """
    青春浙江
    :param user_id:
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        nickname = result[0]["token"]
        name = result[0]["name"]
        nid = result[0]["dxx_id"]
        openid = result[0]["openid"]
        cookie = result[0]["cookie"]
        if result[0]["mobile"]:
            suborg = result[0]["mobile"]
        else:
            suborg = None
        answer = await Answer.all().order_by("time").values()
        try:
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
            url = f"https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid={openid}&nickname={nickname}&headimg={cookie}&time={int(time.time())}&source=common&sign=&t={int(time.time())}"
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url)
                response.encoding = response.charset_encoding
                accessToken = re.findall(r"\(\'accessToken\'\,\s+\'(.+?)\'\)", response.text)[0]
                study_url = f"https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current?accessToken={accessToken}"
                response = await client.get(url=study_url)
                response.encoding = response.charset_encoding
                if response.json()['status'] == 200:
                    title = response.json()["result"]['title']
                    course = response.json()['result']['id']
                    commit_url = f"https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join?accessToken={accessToken}"
                    params = {
                        "course": course,
                        "subOrg": suborg,
                        "nid": nid,
                        "cardNo": name
                    }
                    response = await client.post(url=commit_url, json=params)
                    response.encoding = response.charset_encoding
                    if response.json()['status'] == 200:
                        await User.filter(user_id=user_id).update(
                            commit_time=time.time(),
                            catalogue=title
                        )
                        await commit(user_id=user_id, catalogue=title, status=True)
                        return {
                            "status": 0,
                            "catalogue": title,
                            "msg": "提交成功！"
                        }
                    else:
                        await commit(user_id=user_id, catalogue=title, status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败，信息错误！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败，青春浙江访问失败！"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def shanghai(user_id: int) -> dict:
    """
    青春上海
    :param user_id:
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        nickname = result[0]["token"]
        name = result[0]["name"]
        nid = result[0]["dxx_id"]
        openid = result[0]["openid"]
        cookie = result[0]["cookie"]
        if result[0]["mobile"]:
            suborg = result[0]["mobile"]
        else:
            suborg = None
        answer = await Answer.all().order_by("time").values()
        try:
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
            url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/login/we-chat/callback?appid=wxa693f4127cc93fad&openid={openid}&nickname={nickname}&headimg={cookie}&callback=https://qcsh.h5yunban.com/youth-learning/&scope=snsapi_userinfo"
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url)
                response.encoding = response.charset_encoding
                accessToken = re.findall(r"\(\'accessToken\'\,\s+\'(.+?)\'\)", response.text)[0]
                study_url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/course/current?accessToken={accessToken}"
                response = await client.get(url=study_url)
                response.encoding = response.charset_encoding
                if response.json()['status'] == 200:
                    title = response.json()["result"][0]['title']
                    course = response.json()['result'][0]['id']
                    commit_url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/join?accessToken={accessToken}"
                    params = {
                        "course": course,
                        "subOrg": suborg,
                        "nid": nid,
                        "cardNo": name
                    }
                    response = await client.post(url=commit_url, json=params)
                    response.encoding = response.charset_encoding
                    if response.json()['status'] == 200:
                        await User.filter(user_id=user_id).update(
                            commit_time=time.time(),
                            catalogue=title
                        )
                        await commit(user_id=user_id, catalogue=title, status=True)
                        return {
                            "status": 0,
                            "catalogue": title,
                            "msg": "提交成功！"
                        }
                    else:
                        await commit(user_id=user_id, catalogue=title, status=False)
                        return {
                            "status": response.json()["status"],
                            "msg": response.json()["message"]
                        }
                else:
                    await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败，青春上海访问失败！"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
            }


async def anhui(user_id: int) -> dict:
    """
    安徽共青团
    :param user_id:用户ID
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        username = result[0]['name']
        gender = result[0]['gender']
        mobile = result[0]['mobile']
        level1 = result[0]['university_type']
        level2 = result[0]['university']
        level3 = result[0]['college']
        level4 = result[0]['organization']
        level5 = result[0]['organization_id']
        token = result[0]["token"]
        answer = await Answer.all().order_by("time").values()
        try:
            headers = {
                "Host": "dxx.ahyouth.org.cn",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "http://dxx.ahyouth.org.cn/",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                'Content-Type': 'application/x-www-form-urlencoded',
                "X-Requested-With": 'com.tencent.mm',
                "Origin": 'http://dxx.ahyouth.org.cn',
                "token": token
            }
            data = {
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
                infor_response = await client.post(url=get_infor_url, params=data)
                infor_response.encoding = infor_response.charset_encoding
                infor_response_json = infor_response.json()
                if infor_response_json['code'] == 200:
                    username = infor_response_json['content']['username']
                    token = infor_response_json['content']['token']
                    gender = infor_response_json['content']['gender']
                    mobile = infor_response_json['content']['mobile']
                    level1 = infor_response_json['content']['level1']
                    level2 = infor_response_json['content']['level2']
                    level3 = infor_response_json['content']['level3']
                    level4 = infor_response_json['content']['level4']
                    level5 = infor_response_json['content']['level5']
                    data = {
                        'username': username,
                        'gender': gender,
                        'mobile': mobile,
                        'level1': level1,
                        'level2': level2,
                        'level3': level3,
                        'level4': level4,
                        'level5': level5
                    }
                    commit_url = 'http://dxx.ahyouth.org.cn/api/newLearn'
                    commit_response = await client.post(url=commit_url, params=data)
                    commit_response.encoding = commit_response.charset_encoding
                    commit_response_json = commit_response.json()
                    if commit_response_json['code'] == 200:
                        await User.filter(user_id=user_id).update(
                            token=token,
                            commit_time=time.time(),
                            catalogue=answer[-1]["catalogue"]
                        )
                        await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=True)
                        return {
                            "status": 0,
                            "catalogue": answer[-1]["catalogue"],
                            "msg": "提交成功！"
                        }
                    else:
                        await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败，token失效！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败,token获取失败！"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def sichuan(user_id: int) -> dict:
    """
    天府新青年
    :param user_id:
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        token = result[0]["token"]
        university_type = result[0]["university_type"]
        university_id = result[0]["university_id"]
        university = result[0]["university"]
        name = result[0]["name"]
        mobile = result[0]["mobile"]
        college_id = result[0]["college_id"]
        college = result[0]["college"]
        organization_id = result[0]["organization_id"]
        organization = result[0]["organization"]
        dxx_id = result[0]["dxx_id"]
        data_json = {
            "name": name,
            "tel": mobile,
            "org": f"#{dxx_id}#{university_id}#{college_id}#{organization_id}#",
            "lastOrg": organization_id,
            "orgName": organization,
            "allOrgName": f"#{university_type}#{university}#{college}#{organization}#"
        }
        headers.update({
            "Referer": 'http://scyol.com/v_prod6.02/',
            "Host": "dxx.scyol.com",
            "Connection": "keep-alive",
            "Content_Length": '9',
            "Content_Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3224 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Origin": "http://scyol.com",
            "X-Requested-With": "com.tencent.mm",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "token": token,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        answer = await Answer.all().order_by("time").values()
        title = answer[-1]["catalogue"]
        url = 'https://dxx.scyol.com/api/student/commit'
        try:
            async with AsyncClient(headers=headers) as client:
                response = await client.post(url=url, json=data_json)
                if response.status_code == 200:
                    response.encoding = response.charset_encoding
                    if response.json()["code"] == 2:
                        await User.filter(user_id=user_id).update(
                            commit_time=time.time(),
                            catalogue=title
                        )
                        await commit(user_id=user_id, catalogue=title, status=True)
                        return {
                            "status": 0,
                            "catalogue": title,
                            "msg": "你已经提交了，请勿重复提交哦"
                        }
                    elif response.json()["code"] == 200:
                        await User.filter(user_id=user_id).update(
                            commit_time=time.time(),
                            catalogue=title
                        )
                        await commit(user_id=user_id, catalogue=title, status=True)
                        return {
                            "status": 0,
                            "catalogue": title,
                            "msg": "提交成功！"
                        }
                    else:
                        await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败！"
                        }
                else:
                    return {
                        "status": 500,
                        "msg": "提交失败,cookie失效！"
                    }
        except Exception as e:
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def shandong(user_id: int, catalogue: Optional[str] = None) -> dict:
    """
    青春山东
    :param catalogue:
    :param user_id: 用户ID
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        if catalogue:
            filterArg = {
                "title": catalogue
            }
            answer = await ShanDongDxx.filter(**filterArg).order_by("time").values()
            version = answer[-1]["version"]
            title = catalogue
        else:
            new_version_url = f'http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getNewestVersionInfo'
            async with AsyncClient(headers=headers) as client:
                version_response = await client.post(url=new_version_url)
                version_response.encoding = version_response.charset_encoding
                content = version_response.json()
                if content["errcode"] == "0":
                    version = content["version"]
                    title = content["versionname"]
                else:
                    return {
                        "status": 404,
                        "msg": "获取青年大学习失败！"
                    }
        openid = result[0]["openid"]
        cookie = result[0]["cookie"]
        headers.update({
            "Host": "qndxx.youth54.cn",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3234 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://qndxx.youth54.cn",
            "Referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=pageSdtwdt",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookie
        })
        try:
            async with AsyncClient(headers=headers) as client:
                data = {
                    'openid': openid,
                    'version': version
                }
                if not catalogue:
                    commit_url = 'http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=studyLatest'
                else:
                    commit_url = "http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getLearnPastVersion"
                response = await client.post(url=commit_url, params=data, headers=headers)
                if response.status_code == 200:
                    response.encoding = response.charset_encoding
                    if response.json()["errcode"] == "0":
                        await User.filter(user_id=user_id).update(
                            commit_time=time.time(),
                            catalogue=title
                        )
                        await commit(user_id=user_id, catalogue=title, status=True)
                        return {
                            "status": 0,
                            "catalogue": title,
                            "msg": "提交成功！"
                        }
                    else:
                        await commit(user_id=user_id, catalogue=title, status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败,cookie失效！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败，cookie失效！"
                    }
        except Exception as e:
            await commit(user_id=user_id, catalogue=catalogue, status=False)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def chongqing(user_id: int) -> dict:
    """
    重庆共青团
    :param user_id:
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        openid = result[0]["openid"]
        answer = await Answer.all().order_by("time").values()
        title = answer[-1]["catalogue"]
        headers.update(
            {
                "Host": "qndxx.cqyouths.com",
                "Connection": "keep-alive",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                "X-Requested-With": "com.tencent.mm",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            }
        )
        try:
            new_url = f"http://qndxx.cqyouths.com/new_course.json?time={int(time.time())}"
            async with AsyncClient(headers=headers) as client:
                new_response = await client.get(url=new_url)
                if new_response.status_code == 200:
                    new_response.encoding = new_response.charset_encoding
                    course_id = new_response.json()['data'][0]['id']
                    commit_url = f"http://qndxx.cqyouths.com/api/course/studyCourse?openid={openid}&id={course_id}"
                    response = await client.get(url=commit_url)
                    if response.status_code == 200:
                        response.encoding = response.charset_encoding
                        if response.json()["status"] == 200:
                            await User.filter(user_id=user_id).update(
                                commit_time=time.time(),
                                catalogue=title
                            )
                            await commit(user_id=user_id, catalogue=title, status=True)
                            return {
                                "status": 0,
                                "catalogue": title,
                                "msg": "提交成功！"
                            }
                        elif response.json()["status"] == 201:
                            await User.filter(user_id=user_id).update(
                                commit_time=time.time(),
                                catalogue=title
                            )
                            await commit(user_id=user_id, catalogue=title, status=True)
                            return {
                                "status": 0,
                                "catalogue": title,
                                "msg": "提交成功！"
                            }
                        else:
                            await commit(user_id=user_id, catalogue=title, status=False)
                            return {
                                "status": 500,
                                "msg": "提交失败，openid错误！"
                            }
                    else:
                        await commit(user_id=user_id, catalogue=title, status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败，openid错误！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败，重庆共青团访问失败！"
                    }
        except Exception as e:
            logger.error(e)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def jilin(user_id: int) -> dict:
    """
    吉青飞扬
    :param user_id:
    :return:
    """

    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        openid = result[0]["openid"]
        dxx_id = result[0]["dxx_id"]
        answer = await Answer.all().order_by("time").values()
        title = answer[-1]["catalogue"]
        headers.update(
            {
                "Host": "jqfy.jl54.org",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "X-Requested-With": "com.tencent.mm",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            }
        )
        try:
            commit_url = f"http://jqfy.jl54.org/jltw/wechat/editStudyRecord/{dxx_id}"
            data = {
                "openid": openid
            }
            async with AsyncClient(headers=headers) as client:
                response = await client.post(url=commit_url, params=data)
            if response.status_code == 200:
                response.encoding = response.charset_encoding
                if response.json()["code"] == '0001':
                    await User.filter(user_id=user_id).update(
                        commit_time=time.time(),
                        catalogue=title
                    )
                    await commit(user_id=user_id, catalogue=title, status=True)
                    return {
                        "status": 0,
                        "catalogue": title,
                        "msg": "提交成功！"
                    }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": f"提交失败，openid错误！"
                    }
            else:
                await commit(user_id=user_id, catalogue=title, status=False)
                return {
                    "status": 500,
                    "msg": "提交失败，吉青飞扬访问失败！"
                }
        except Exception as e:
            logger.error(e)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def guangdong(user_id: int) -> dict:
    """
    广东共青团
    :param user_id:用户ID
    :return:
    """

    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        dxx_id = result[0]['dxx_id']
        token = result[0]["token"]
        answer = await Answer.all().order_by("time").values()
        try:
            study_headers = {
                'Host': 'youthstudy.12355.net',
                'Connection': 'keep-alive',
                'X-Litemall-Token': token,
                'X-Litemall-IdentiFication': 'young',
                'User-Agent': 'MicroMessenger',
                'Accept': '*/*',
                'Origin': 'https://youthstudy.12355.net',
                'X-Requested-With': 'com.tencent.mm',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://youthstudy.12355.net/h5/',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            new_study_url = "https://youthstudy.12355.net/saomah5/api/young/chapter/new"
            async with AsyncClient(headers=study_headers, timeout=30, max_redirects=5) as client:
                study_response = await client.get(url=new_study_url)
            study_response.encoding = study_response.charset_encoding
            if study_response.json()["errno"] == 0:
                chapterId = study_response.json().get('data').get('entity').get('id')
                title = study_response.json().get('data').get('entity').get('name').replace('“青年大学习”', "").strip()
                commit_url = "https://youthstudy.12355.net/saomah5/api/young/course/chapter/saveHistory"
                async with AsyncClient(headers=study_headers, timeout=30, max_redirects=5) as client:
                    commit_response = await client.post(url=commit_url, data={
                        "chapterId": chapterId
                    })
                if commit_response.json()["errno"] == 0:
                    await User.filter(user_id=user_id).update(
                        token=token,
                        commit_time=time.time(),
                        catalogue=title
                    )
                    await commit(user_id=user_id, catalogue=title, status=True)
                    return {
                        "status": 0,
                        "catalogue": title,
                        "msg": "提交成功！"
                    }
                else:
                    await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败！"
                    }
            else:
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
                            'Content-Length': '134',
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
                            token_response = await client.post(url=token_url,
                                                               data="sign=" + urllib.parse.quote(content))
                        if token_response.json()["errno"] == 0:
                            token = token_response.json()['data']['entity']['token']
                            study_headers = {
                                'Host': 'youthstudy.12355.net',
                                'Connection': 'keep-alive',
                                'X-Litemall-Token': token,
                                'X-Litemall-IdentiFication': 'young',
                                'User-Agent': 'MicroMessenger',
                                'Accept': '*/*',
                                'Origin': 'https://youthstudy.12355.net',
                                'X-Requested-With': 'com.tencent.mm',
                                'Sec-Fetch-Site': 'same-origin',
                                'Sec-Fetch-Mode': 'cors',
                                'Sec-Fetch-Dest': 'empty',
                                'Referer': 'https://youthstudy.12355.net/h5/',
                                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                            }
                            new_study_url = "https://youthstudy.12355.net/saomah5/api/young/chapter/new"
                            async with AsyncClient(headers=study_headers, timeout=30, max_redirects=5) as client:
                                study_response = await client.get(url=new_study_url)
                            if study_response.json()["errno"] == 0:
                                chapterId = study_response.json().get('data').get('entity').get('id')
                                title = study_response.json().get('data').get('entity').get('name').replace(
                                    '"青年大学习”', "").strip()
                                commit_url = "https://youthstudy.12355.net/saomah5/api/young/course/chapter/saveHistory"
                                async with AsyncClient(headers=study_headers, timeout=30, max_redirects=5) as client:
                                    commit_response = await client.post(url=commit_url, data={
                                        "chapterId": chapterId
                                    })
                                if commit_response.json()["errno"] == 0:
                                    await User.filter(user_id=user_id).update(
                                        token=token,
                                        commit_time=time.time(),
                                        catalogue=title
                                    )
                                    await commit(user_id=user_id, catalogue=title, status=True)
                                    return {
                                        "status": 0,
                                        "catalogue": title,
                                        "msg": "提交成功！"
                                    }
                                else:
                                    await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                                    return {
                                        "status": 500,
                                        "msg": "提交失败！"
                                    }
                        else:
                            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                            return {
                                "status": 500,
                                "msg": "提交失败，token获取失效！"
                            }
                    else:
                        await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败，token获取失效！"
                        }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
            }


async def beijing(user_id: int) -> dict:
    """
    青春北京
    :param user_id:用户ID
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        cookie = result[0]['cookie']
        token = result[0]["token"]
        answer = await Answer.all().order_by("time").values()
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/113.0.0.0", }
        login_url = "https://m.bjyouth.net/site/login"
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
                    if login_response.status_code == 200:
                        login_response.encoding = login_response.charset_encoding
                        if login_response.text == '8':
                            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                            return {
                                "status": 500,
                                "msg": "提交失败，验证码识别失败！"
                            }
                        if 'fail' in login_response.text:
                            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                            return {
                                "status": 500,
                                "msg": "提交失败，账号或密码错误！"
                            }
                        course_url = "https://m.bjyouth.net/dxx/index"
                        course_rsp = await client.get(course_url)
                        if course_rsp.json()["code"] == 200:
                            title = course_rsp.json()['newCourse']['title']
                            courseId = course_rsp.json()['newCourse']['id']
                            organization_rsp = await client.get('https://m.bjyouth.net/dxx/is-league')
                            organization_id = int(organization_rsp.text)
                            study_url = "https://m.bjyouth.net/dxx/check"
                            study_response = await client.post(url=study_url, json={
                                "id": str(courseId),
                                "org_id": organization_id
                            })
                            if study_response.status_code == 200:
                                learnedInfo_url = 'https://m.bjyouth.net/dxx/my-study?page=1&limit=15&year=' + time.strftime(
                                    "%Y",
                                    time.localtime())
                                haveLearned = await client.get(learnedInfo_url)
                                if haveLearned.json()["code"] == 200:
                                    if f"学习课程：《{title}》" in list(
                                            map(lambda x: x['text'], haveLearned.json()['data'])):
                                        await User.filter(user_id=user_id).update(
                                            token=token,
                                            commit_time=time.time(),
                                            catalogue=answer[-1]["catalogue"]
                                        )
                                        await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=True)
                                        return {
                                            "status": 0,
                                            "catalogue": answer[-1]["catalogue"],
                                            "msg": "提交成功！"
                                        }
                                    else:
                                        await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                                        return {
                                            "status": 500,
                                            "msg": "提交失败！"
                                        }
                                else:
                                    await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                                    return {
                                        "status": 500,
                                        "msg": "提交失败,获取历史提交信息失败！"
                                    }
                            else:
                                await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                                return {
                                    "status": 500,
                                    "msg": "提交失败！"
                                }
                    else:
                        await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败，登录失败！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败，北京共青团官网异常"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def tianjin(user_id: int) -> dict:
    """
    津彩青春
    :param user_id:用户ID
    :return:
    """

    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        cookie = result[0]["cookie"]
        answer = await Answer.all().order_by("time").values()
        title = answer[-1]["catalogue"]
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/113.0.0.0",
            "Cookie": cookie,
        }
        try:
            commit_url = "http://admin.ddy.tjyun.com/zm/jump/1"
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url=commit_url)
            if response.status_code == 302:
                response.encoding = response.charset_encoding
                if "weui_text_area" not in response.text:
                    await User.filter(user_id=user_id).update(
                        commit_time=time.time(),
                        catalogue=title
                    )
                    await commit(user_id=user_id, catalogue=title, status=True)
                    return {
                        "status": 0,
                        "catalogue": title,
                        "msg": "提交成功！"
                    }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": f"提交失败，Cookie失效！"
                    }
            else:
                await commit(user_id=user_id, catalogue=title, status=False)
                return {
                    "status": 500,
                    "msg": "提交失败，地址请求失败！"
                }
        except Exception as e:
            logger.error(e)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }


async def shanxi(user_id: int, catalogue: Optional[str] = None) -> dict:
    """
    三秦青年
    :param catalogue:
    :param user_id:用户ID
    :return:
    """
    result = await User.filter(user_id=user_id).values()
    if not result:
        return {
            "status": 500,
            "msg": "用户数据不存在！"
        }
    else:
        if catalogue:
            filterArg = {
                "name": catalogue
            }
            answer = await ShanXiDxx.filter(**filterArg).order_by("code").values()
            code = answer[-1]["code"]
            title = catalogue
        else:
            answer = await ShanXiDxx.all().order_by("code").values()
            code = answer[-1]["code"]
            title = answer[-1]["name"]
        token = result[0]["token"]
        headers = {
            "Host": "api.sxgqt.org.cn",
            "accept": "application/json",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Linux; Android 13; 23049RAD8C Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5317 MMWEBSDK/20230701 MMWEBID/6170 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "version": "H5_3.2.0",
            "token": token,
            "origin": "https://h5.sxgqt.org.cn"
        }
        try:
            commit_url = f"https://api.sxgqt.org.cn/h5sxapiv2/study/statistics?type=new&id={code}"
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url=commit_url)
                if response.status_code == 200:
                    if response.json()["code"] == 0:
                        await User.filter(user_id=user_id).update(
                            commit_time=time.time(),
                            catalogue=title
                        )
                        await commit(user_id=user_id, catalogue=title, status=True)
                        return {
                            "status": 0,
                            "catalogue": title,
                            "msg": "提交成功！"
                        }
                    else:
                        await commit(user_id=user_id, catalogue=title, status=False)
                        return {
                            "status": 500,
                            "msg": f"提交失败，token失效！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败，地址请求失败！"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=title, status=False)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }
