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


async def jiangsu(user_id: int) -> dict:
    """
    江苏共青团
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
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookie
        }
        try:
            url = "https://service.jiangsugqt.org/api/lessons"
            params = {"page": 1, "limit": 5}
            async with AsyncClient(headers=headers) as client:
                response = await client.post(url=url, json=params)
            response.encoding = response.charset_encoding
            result = response.json()
            if result["status"] == 1:
                params = {
                    "lesson_id": result["data"][0]["id"]
                }
                title = result["data"][0]["title"]
                commit_url = "https://service.jiangsugqt.org/api/doLesson"
                async with AsyncClient(headers=headers) as client:
                    response = await client.post(url=commit_url, json=params)
                response.encoding = response.charset_encoding
                result = response.json()
                if result["status"] == 1:
                    await User.filter(user_id=user_id).update(
                        commit_time=time.time(),
                        catalogue=result["data"]["title"]
                    )
                    await commit(user_id=user_id, catalogue=result["data"]["title"], status=True)
                    return {
                        "status": 0,
                        "catalogue": result["data"]["title"],
                        "msg": "提交成功！"
                    }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败！"
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
            headers.update({
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
            })
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
                headers.update({
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
                })
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
                async with AsyncClient(headers=headers, timeout=30, max_redirects=5) as client:
                    commit_response = await client.post(url=commit_url, params=data)
                commit_response.encoding = commit_response.charset_encoding
                commit_response_json = commit_response.json()
                if commit_response_json['code'] == 200:
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


async def henan(user_id: int) -> dict:
    """
    河南共青团
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
        token = result[0]["openid"]
        answer = await Answer.all().order_by("time").values()
        headers.update({
            "Host": "hnqndaxuexi.dahejs.cn",
            "Connection": "keep-alive",
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3262 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.20.2100(0x28001438) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Content-Type": "application/json",
            "X-Requested-With": "com.tencent.mm",
            "Referer": "http://hnqndaxuexi.dahejs.cn/study/studyList",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookie
        })
        try:
            get_new_study_url = "http://hnqndaxuexi.dahejs.cn/stw/news/list?&pageNumber=1&pageSize=10"
            async with AsyncClient(headers=headers) as client:
                response = await client.get(url=get_new_study_url)
            if response.status_code == 200:
                response.encoding = response.charset_encoding
                dxx_list = response.json()['obj']['news']['list'][0]
                newsid = dxx_list['id']
                title = dxx_list['title']
                commit_url = f"http://hnqndaxuexi.dahejs.cn/stw/news/study/{newsid}"
                headers.update({
                    "token": token,
                })
                async with AsyncClient(headers=headers) as client:
                    response = await client.post(url=commit_url)
                if response.status_code == 200:
                    response.encoding = response.charset_encoding
                    result = response.json()
                    if result["result"] == 200:
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
                    "msg": "提交失败,cookie失效！"
                }
        except Exception as e:
            logger.error(e)
            await commit(user_id=user_id, catalogue=answer[-1]["catalogue"], status=False)
            return {
                "status": 500,
                "msg": "提交失败！"
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


async def shandong(user_id: int) -> dict:
    """
    青春山东
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
        openid = result[0]["openid"]
        cookie = result[0]["cookie"]
        answer = await Answer.all().order_by("time").values()
        title = answer[-1]["catalogue"]
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
            version_url = f'http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getNewestVersionInfo&openid={openid}'
            async with AsyncClient(headers=headers) as client:
                version_response = await client.post(url=version_url)
            if version_response.status_code == 200:
                version_response.encoding = version_response.charset_encoding
                content = version_response.json()
                if content["errcode"] == "0":
                    versionname = content['versionname']
                    version = content['version']
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
                    data = {
                        'openid': openid,
                        'version': version
                    }
                    commit_url = 'http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=studyLatest'
                    async with AsyncClient(headers=headers) as client:
                        response = await client.post(url=commit_url, params=data)
                    if response.status_code == 200:
                        response.encoding = response.charset_encoding
                        if response.json()["errcode"] == "0":
                            await User.filter(user_id=user_id).update(
                                commit_time=time.time(),
                                catalogue=versionname
                            )
                            await commit(user_id=user_id, catalogue=versionname, status=True)
                            return {
                                "status": 0,
                                "catalogue": versionname,
                                "msg": "提交成功！"
                            }
                        else:
                            await commit(user_id=user_id, catalogue=versionname, status=False)
                            return {
                                "status": 500,
                                "msg": "提交失败！"
                            }
                    else:
                        await commit(user_id=user_id, catalogue=versionname, status=False)
                        return {
                            "status": 500,
                            "msg": "提交失败！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败！"
                    }
            else:
                await commit(user_id=user_id, catalogue=title, status=False)
                return {
                    "status": 500,
                    "msg": "提交失败！"
                }
        except Exception as e:
            await commit(user_id=user_id, catalogue=title, status=False)
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
                async with AsyncClient(headers=headers) as client:
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
                            "msg": "提交失败！"
                        }
                else:
                    await commit(user_id=user_id, catalogue=title, status=False)
                    return {
                        "status": 500,
                        "msg": "提交失败！"
                    }
            else:
                await commit(user_id=user_id, catalogue=title, status=False)
                return {
                    "status": 500,
                    "msg": "提交失败！"
                }
        except Exception as e:
            logger.error(e)
            return {
                "status": 500,
                "msg": f"提交失败,{e}"
            }