import json
import random
import re
import secrets
import time

from anti_useragent import UserAgent
from httpx import AsyncClient
from nonebot import logger

from ..models.accuont import User, Commit
from ..models.dxx import Answer

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


async def hubei(user_id: int) -> dict:
    """
    青春湖北
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
        name = result[0]["name"]
        openid = result[0]["openid"]
        university = result[0]["university"]
        college = result[0]["college"]
        organization = result[0]["organization"]
        answer = await Answer.all().order_by("time").values()
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
        url += "&lesson_name=" + answer[-1]["catalogue"]
        try:
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url)
            response_json = json.loads(response.text)
            if response_json.get('code') == 1:
                await User.filter(user_id=user_id).update(
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
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
            }


async def jiangxi(user_id: int) -> dict:
    """
    江西共青团
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
        name = result[0]["name"]
        nid = result[0]["dxx_id"]
        openid = result[0]["openid"]
        if result[0]["mobile"]:
            suborg = result[0]["mobile"]
        else:
            suborg = ''
        answer = await Answer.all().order_by("time").values()
        try:
            url = f"http://www.jxqingtuan.cn/pub/vol/volClass/index?userId={random.randint(4363000, 4364000)}"
            headers.update({
                'Cookie': 'JSESSIONID=' + secrets.token_urlsafe(40),
                'Host': 'www.jxqingtuan.cn',
                'Origin': 'http://www.jxqingtuan.cn',
                'Referer': 'http://www.jxqingtuan.cn/html/h5_index.html?&accessToken=' + openid,
            })
            async with AsyncClient(headers=headers) as client:
                course = await client.get(url=url)
            course.encoding = course.charset_encoding
            if json.loads(course.text).get('code') == 0:
                title = json.loads(course.text).get("list")[0].get("title")
                course = json.loads(course.text).get('list')[0].get('id')
                resp_url = 'http://www.jxqingtuan.cn/pub/vol/volClass/join?accessToken='
                data = {"course": course, "nid": nid, "cardNo": name, "subOrg": suborg}
                async with AsyncClient(headers=headers) as client:
                    res = await client.post(url=resp_url, json=data)
                    res.encoding = res.charset_encoding
                resp = json.loads(res.text)
                if resp.get("status") == 200:
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
                        "msg": "提交失败！"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
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
            async with AsyncClient(headers=headers, max_redirects=5, timeout=10) as client:
                response = await client.get(url=study_url)
            response.encoding = response.charset_encoding
            if response.json()['status'] == 200:
                title = response.json()["result"]['title']
                course = response.json()['result']['id']
                commit_url = f"https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join?accessToken={accessToken}"
                params = {
                    "course": course,
                    "subOrg":suborg,
                    "nid": nid,
                    "cardNo": name
                }
                async with AsyncClient(headers=headers, timeout=10, max_redirects=5) as client:
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
                        "msg": "提交失败！"
                    }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
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
            async with AsyncClient(headers=headers, max_redirects=5, timeout=10) as client:
                response = await client.get(url=study_url)
            response.encoding = response.charset_encoding
            if response.json()['status'] == 200:
                title = response.json()["result"]['title']
                course = response.json()['result']['id']
                commit_url = f"https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/join?accessToken={accessToken}"
                params = {
                    "course": course,
                    "subOrg": suborg,
                    "nid": nid,
                    "cardNo": name
                }
                async with AsyncClient(headers=headers, timeout=10, max_redirects=5) as client:
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
                        "msg": "提交失败！"
                    }
         except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
            }
