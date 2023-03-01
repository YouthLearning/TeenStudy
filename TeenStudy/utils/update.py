import asyncio
import json
import time

from bs4 import BeautifulSoup
from httpx import AsyncClient
from nonebot import logger, require, get_bot, get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageSegment

from ..models.dxx import Answer, Resource, Area
from ..models.accuont import Admin, AddUser, User

scheduler = require('nonebot_plugin_apscheduler').scheduler
super_id = get_driver().config.superusers  # 超管id
headers = {
    "Host": "h5.cyol.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Origin": "http://h5.cyol.com",
    "X-Requested-With": "com.tencent.mm",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}


async def crawl_answer(url: str) -> dict:
    """
    获取青年大学习的期数，答案和完成截图链接
    :param url: 最新一期大学习的地址
    :return:
    """
    async with AsyncClient(headers=headers, max_redirects=5) as client:
        resp = await client.get(url=url, timeout=10)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    title = soup.find('title').text[7:].strip()
    start_div = resp.text.find('<div class="section0 topindex">')
    end_div = resp.text.find('<script type="text/javascript" src="js/index.js')
    soup = BeautifulSoup(resp.text[start_div:end_div], 'lxml')
    tmp = []
    answer_attrs = {"required": [], "optional": []}
    option = "ABCDEF"
    template = "{num}. {check}"
    for div in soup.find("body"):
        if div == "\n":
            continue
        answer = []
        if div.name == "div":
            for i in div.find_all("div"):
                check = i.get("data-a")
                if check is not None:
                    answer.append(check)
            if len(answer) > 4:
                answer = answer[:int(len(answer) / 2)]
            tmp.append(answer)
    req_end = 0
    flag = {"location": 0, "result": True}
    for i, v in enumerate(tmp):
        if len(v) == 0:
            req_end = i + 1
        elif flag["result"]:
            flag["result"] = False
            flag["location"] = i
    for i, v in enumerate(tmp):
        if flag["location"] < req_end and req_end - 1 > i >= flag["location"]:
            field = "required"
            answer_attrs[field].append(v)
        elif flag["location"] == req_end and i >= req_end:
            field = "optional"
            answer_attrs[field].append(v)
        elif flag["location"] < req_end <= i:
            field = "optional"
            answer_attrs[field].append(v)
    output = []
    if len(answer_attrs["required"]) > 0:
        output.append("本期答案\n")
        for i, v in enumerate(answer_attrs["required"]):
            checks = ""
            for j, v2 in enumerate(v):
                try:
                    if v2 == "1":
                        checks += option[j]
                except:
                    pass
            output.append(template.format(num=i + 1, check=checks) + "\n")
    if len(answer_attrs["optional"]) != 0:
        output.append("课外习题\n")
        for i, v in enumerate(answer_attrs["optional"]):
            checks = ""
            for j, v2 in enumerate(v):
                if v2 == "1":
                    checks += option[j]
            output.append(template.format(num=i + 1, check=checks) + "\n")
    result = [output[0]]
    for i, v in enumerate(output):
        if i % 13 != 0 and i != 0:
            result[int(i / 13)] += v
        elif i % 13 == 0 and i != 0:
            result.append(v)
    try:
        end_url = url.replace('m.html', 'images/end.jpg')
    except:
        end_url = url[:-6] + 'images/end.jpg'
    return {
        "end_url": end_url,
        "catalogue": title,
        "answer": result[0]
    }


async def update_answer():
    logger.opt(colors=True).info("<u><y>[大学习数据库]</y></u><g>➤➤➤➤➤检查答案数据✔✔✔✔✔</g>")
    resp_url = 'https://h5.cyol.com/special/weixin/sign.json'
    async with AsyncClient(headers=headers) as client:
        response = await client.get(url=resp_url, timeout=10)
    response.encoding = response.charset_encoding
    result = json.loads(response.text)
    code_result = list(result)[-10:]
    for code in code_result:
        if await Answer.filter(code=code).count():
            continue
        else:
            try:
                url = result[code]["url"]
                data = await crawl_answer(url=url)
                end_url = data["end_url"]
                answer = data["answer"]
                catalogue = data["catalogue"]
                async with AsyncClient(headers=headers) as client:
                    end_jpg = await client.get(end_url, timeout=10)
                cover = end_jpg.content
                await Answer.create(
                    time=time.time(),
                    code=code,
                    catalogue=catalogue,
                    url=url,
                    end_url=end_url,
                    answer=answer,
                    cover=cover
                )
                logger.opt(colors=True).success(f"<u><y>青年大学习</y></u> <m>{catalogue}</m> <g>更新成功!</g>")
            except Exception as e:
                logger.error(e)
    logger.opt(colors=True).success("<u><y>[大学习数据库]</y></u><g>➤➤➤➤➤答案数据更新完成✔✔✔✔✔</g>")


@scheduler.scheduled_job('cron', day_of_week='6', hour="21-23", minute="*/15", id='update_data',
                         timezone="Asia/Shanghai")
async def update_data():
    try:
        bot: Bot = get_bot()
    except ValueError as e:
        return
    resp_url = 'https://h5.cyol.com/special/weixin/sign.json'
    async with AsyncClient(headers=headers) as client:
        response = await client.get(url=resp_url, timeout=10)
    response.encoding = response.charset_encoding
    result = json.loads(response.text)
    code_result = list(result)[-10:]
    for code in code_result:
        if await Answer.filter(code=code).count():
            continue
        else:
            try:
                url = result[code]["url"]
                data = await crawl_answer(url=url)
                end_url = data["end_url"]
                answer = data["answer"]
                catalogue = data["catalogue"]
                async with AsyncClient(headers=headers) as client:
                    end_jpg = await client.get(end_url, timeout=10)
                cover = end_jpg.content
                await Answer.create(
                    time=time.time(),
                    code=code,
                    catalogue=catalogue,
                    url=url,
                    end_url=end_url,
                    answer=answer,
                    cover=cover
                )
                logger.opt(colors=True).success(f"<u><y>青年大学习</y></u> <m>{catalogue}</m> <g>更新成功!</g>")
                admin = await Admin.all().values()
                await bot.send_private_msg(user_id=admin[0]["user_id"],
                                           message=f"检测到青年大学习有更新，下周一为{catalogue},详细信息请登录后台：http://{admin[0]['ip']}:{get_driver().config.port}/TeenStudy/login 查看d(´ω｀*)")
            except Exception as e:
                logger.error(e)


@scheduler.scheduled_job('cron', second='*/15', misfire_grace_time=10)
async def check_apply():
    try:
        bot: Bot = get_bot()
    except ValueError as e:
        return
    apply_list = await AddUser.filter(status="未通过").values()

    for item in apply_list:
        result = await User.filter(user_id=item["user_id"], group_id=item["group_id"]).count()
        if result:
            await AddUser.filter(id=item["id"]).update(status="已通过")
            await bot.send_group_msg(group_id=item["group_id"],
                                     message=MessageSegment.at(user_id=item["user_id"]) + MessageSegment.text(
                                         "信息绑定成功( • ̀ω•́ )✧"))
            await asyncio.sleep(2)
            continue
        now_time = int(time.time())
        if (now_time - item["time"]) > 180:
            await AddUser.filter(id=item["id"]).update(status="已过期")
            await bot.send_group_msg(group_id=item["group_id"],
                                     message=MessageSegment.at(user_id=item["user_id"]) + MessageSegment.text(
                                         "添加申请已过期，请重新发 添加大学习 指令进行申请( • ̀ω•́ )✧"))
            await asyncio.sleep(2)
        else:
            continue


@scheduler.scheduled_job('cron', day_of_week='0', hour='0', minute='0', id='clear', timezone="Asia/Shanghai")
async def clear():
    try:
        result = await Area.all().values()
        for item in result:
            await Area.filter(id=item["id"]).update(status=False)
        logger.opt(colors=True).success(
            f"<u><y>[大学习数据库]</y></u> <m>地区最新一期状态</m> <g>重置成功!</g>")
    except Exception as e:
        logger.opt(colors=True).error(
            f"<u><y>[大学习数据库]</y></u> <m>地区最新一期状态</m> <r重置失败：{e}</r>")
