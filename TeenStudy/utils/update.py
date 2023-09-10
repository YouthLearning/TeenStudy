import asyncio
import json
import time

from bs4 import BeautifulSoup
from httpx import AsyncClient
from nonebot import logger, require, get_bot, get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageSegment

from .path import getConfig
from .utils import get_login_qrcode
from ..models.accuont import AddUser, User
from ..models.dxx import Answer, Area

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
    :param url: 青年大学习的地址
    :return:
    """
    async with AsyncClient(headers=headers, max_redirects=5) as client:
        response = await client.get(url=url, timeout=10)
    response.encoding = response.charset_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    title: str = soup.find('title').text[7:].strip()
    start_div: int = response.text.find('<div class="section0 topindex">')
    end_div: int = response.text.find('<script type="text/javascript" src="js/index.js')
    soup = BeautifulSoup(response.text[start_div:end_div], 'lxml')
    answer: dict = {"knowledgeCard": [], "exercise": []}
    option: str = "ABCDEF"
    template: str = "{num}. {options}"
    for item in soup.select('body [class^="section"]'):
        topicId: int = int(item.get("class")[0][7:])
        temp: list = []
        for item2 in item.select("div"):
            if item2.get("data-a"):
                temp.append(item2.get("data-a"))
        if len(temp) == 0:
            continue
        if len(temp) > 4:
            temp = temp[:int(len(temp) / 2)]
        options: str = ""
        for i, v in enumerate(temp):
            if v == "1":
                options += option[i]
        if topicId < 4:
            answer["knowledgeCard"].append(
                template.format(num=len(answer["knowledgeCard"]) + 1, options=options) + "\n")
        else:
            answer["exercise"].append(template.format(num=len(answer["exercise"]) + 1, options=options) + "\n")
    try:
        end_url: str = url.replace('m.html', 'images/end.jpg')
    except IndexError:
        end_url: str = url[:-6] + 'images/end.jpg'
    return {
        "end_url": end_url,
        "catalogue": title,
        "answer": f'知识卡片：{"".join(answer["knowledgeCard"])}课后习题：{"".join(answer["exercise"])}'
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


@scheduler.scheduled_job('cron', day_of_week='0-6', hour="0-23", minute="*/15", id='update_data',
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
                admin = getConfig()
                content = await get_login_qrcode()
                if admin["URL_STATUS"]:
                    await bot.send_private_msg(user_id=admin["SUPERUSER"], message=MessageSegment.text(
                        f"检测到青年大学习有更新，下周一为{catalogue},详细信息请点击链接登录后台查看，如打不开链接，请复制链接到浏览器d(´ω｀*)\n") + MessageSegment.text(
                        content["url"]))
                await bot.send_private_msg(user_id=admin["SUPERUSER"], message=MessageSegment.text(
                    f"检测到青年大学习有更新，下周一为{catalogue},详细信息请扫码登录后台查看d(´ω｀*)") + MessageSegment.image(
                    content["content"]))
            except Exception as e:
                logger.error(e)


@scheduler.scheduled_job('cron', second='*/10', misfire_grace_time=10)
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
                                         "信息绑定成功，可发指令：提交大学习 提交最新一期青年大学习哦( • ̀ω•́ )✧"))
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
