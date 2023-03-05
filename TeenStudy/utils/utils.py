import base64
import datetime
import hashlib
import json
import os
import random
import time
from io import BytesIO

import qrcode
from PIL import Image, ImageDraw, ImageFont
from nonebot import logger, get_driver

from . import dxx
from ..models.accuont import Admin
from ..models.dxx import Area, Answer, Resource, JiangXi

SUPERS = get_driver().config.superusers
AREA = [
    {
        "area": "湖北",
        "host": "cp.fjg360.cn",
        "referer": None,
        "origin": None,
        "url": "https://h5.cyol.com/special/weixin/sign.json",
        "status": True,
        "catalogue": None
    },
    {
        "area": "江西",
        "host": "www.jxqingtuan.cn",
        "referer": "http://www.jxqingtuan.cn/html/h5_index.html?&accessToken=",
        "origin": "http://www.jxqingtuan.cn",
        "url": "http://www.jxqingtuan.cn/pub/vol/volClass/index?userId=4363431",
        "status": True,
        "catalogue": None
    },
    {
        "area": "浙江",
        "host": "qczj.h5yunban.com",
        "referer": None,
        "origin": None,
        "url": "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current?accessToken=",
        "status": True,
        "catalogue": None
    },
    {
        "area": "上海",
        "host": "qcsh.h5yunban.com",
        "referer": None,
        "origin": None,
        "url": "https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/join?accessToken=",
        "status": True,
        "catalogue": None
    },
    {
        "area": "江苏",
        "host": "service.jiangsugqt.org",
        "referer": None,
        "origin": None,
        "url": "https://service.jiangsugqt.org/youth/lesson/confirm",
        "status": True,
        "catalogue": None
    }, {
        "area": "安徽",
        "host": "dxx.ahyouth.org.cn",
        "referer": "http://dxx.ahyouth.org.cn/",
        "origin": "http://dxx.ahyouth.org.cn",
        "url": "http://dxx.ahyouth.org.cn/api/hidtoryList",
        "status": True,
        "catalogue": None
    },
]
RESOURCE = [
    {
        "name": "MiSans-Light.ttf",
        "url": "",
        "type": "字体",
        "size": "7.6 M"
    }, {
        "name": "answer.png",
        "url": "",
        "type": "答案背景",
        "size": "860.5 K"
    },
    {
        "name": "backgroud1.jpg",
        "url": "",
        "type": "完成截图背景",
        "size": "51.0 K"
    }, {
        "name": "backgroud2.jpg",
        "url": "",
        "type": "完成截图背景",
        "size": "50.9 K"
    }, {
        "name": "backgroud3.jpg",
        "url": "",
        "type": "完成截图背景",
        "size": "50.9 K"
    }, {
        "name": "backgroud4.jpg",
        "url": "",
        "type": "完成截图背景",
        "size": "50.7 K"
    }, {
        "name": "backgroud5.jpg",
        "url": "",
        "type": "完成截图背景",
        "size": "50.4 K"
    }
]


async def plugin_init():
    for item in AREA:
        if await Area.filter(area=item['area']).count():
            continue
        else:
            await Area.create(
                time=time.time(),
                area=item['area'],
                host=item['host'],
                referer=item['referer'],
                origin=item['origin'],
                url=item['url'],
                status=item['status'],
                catalogue=item['catalogue']
            )


async def admin_init():
    result = await Admin.filter(user_id=int(list(SUPERS)[0])).count()
    if result:
        return
    else:
        await Admin.create(
            time=30,
            user_id=int(list(SUPERS)[0]),
            key="d82ffad91168fb324ab6ebc2bed8dacd43f5af8e34ad0d1b75d83a0aff966a06",
            algorithm="HS256",
            password=await to_hash("admin"),
            ip="127.0.0.1"
        )


async def resource_init():
    base_file_path = os.path.dirname(__file__)[:-5] + "resource\\"
    logger.opt(colors=True).info("<u><y>[大学习数据库]</y></u><g>➤➤➤➤➤检查资源数据✔✔✔✔✔</g>")
    for item in RESOURCE:
        if not await Resource.filter(name=item['name']).count():
            try:
                with open(base_file_path + item['name'], 'rb') as r:
                    content = r.read()
                await Resource.create(
                    time=time.time(),
                    name=item['name'],
                    type=item['type'],
                    url=item['url'],
                    size=item['size'],
                    file=content
                )
                logger.opt(colors=True).success(
                    f"<u><y>[大学习数据库]</y></u> <m>{item['type']}-{item['name']}</m> <g>更新成功!</g>")
            except Exception as e:
                logger.success(e)
                continue
    try:
        if not await JiangXi.all().count():
            with open(base_file_path + "dxx_jx.json", 'r', encoding='utf-8') as r:
                obj = json.load(r)
            for item in obj:
                await JiangXi.create(
                    time=time.time(),
                    university_id=item['university_id'],
                    university=item['university'],
                    college_id=item['college_id'],
                    college=item['college'],
                    organization=item['organization'],
                    organization_id=item['organization_id']
                )
            logger.opt(colors=True).success(
                f"<u><y>[大学习数据库]</y></u> <m>江西共青团团支部数据</m> <g>更新成功!</g>")
    except Exception as e:
        logger.error(e)
    logger.opt(colors=True).success("<u><y>[大学习数据库]</y></u><g>➤➤➤➤➤资源数据更新完成✔✔✔✔✔</g>")


async def get_end_pic():
    font_data = await Resource.filter(type="字体").values()
    answer = await Answer.all().order_by('time').values()
    title = '"青年大学习"' + answer[-1]["catalogue"]
    backgrouds = await Resource.filter(type="完成截图背景").values()
    bg_img = Image.open(BytesIO(backgrouds[random.randint(0, 4)]['file']))
    end_img = Image.open(BytesIO(answer[-1]['cover']))
    end_img = end_img.resize((1080, 2200), Image.BILINEAR)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 45)
    img = Image.new('RGB', (end_img.width, bg_img.height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    img.paste(bg_img)
    time = (datetime.datetime.now() + datetime.timedelta(minutes=random.randint(5, 10))).strftime('%H:%M')
    draw.text((120, 30), text=time, font=font, fill='black')
    draw.text((1080 / 2 - (len(title) / 2) * 30, 130), text=title, font=font, fill='black')
    img.paste(end_img, (0, 200))
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return content


async def get_answer_pic():
    font_data = await Resource.filter(type="字体").values()
    answer_result = await Answer.all().order_by('time').values()
    backgrouds = await Resource.filter(type="答案背景").values()
    title = answer_result[-1]["catalogue"]
    answer = answer_result[-1]["answer"]
    start_time = datetime.datetime.fromtimestamp(answer_result[-1]['time']).strftime(
        "%Y年%m月%d日 %H:%M:%S")
    end_day = (datetime.datetime.fromtimestamp(answer_result[-1]["time"]) + datetime.timedelta(
        days=7)).strftime("%Y年%m月%d日")
    end_time = f'{end_day} 22:00:00'
    answer_bg = Image.open(BytesIO(backgrouds[0]['file']))
    img = Image.new('RGB', (902, 987), (255, 255, 255))
    img.paste(answer_bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 55)
    draw.text((20, 20), text='青年大学习主题团课', fill='gold', font=font)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 48)
    draw.text((20, 100), text=title, fill='gold', font=font)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 40)
    draw.text((20, 180), fill='gold', font=font, text=answer)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 40)
    draw.text((410, 550), fill='gold', font=font, text=start_time)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 40)
    draw.text((410, 650), fill='gold', font=font, text=end_time)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 40)
    draw.text((550, 500), text='开始时间', fill='gold', font=font)
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), 40)
    draw.text((550, 600), text='结束时间', fill='gold', font=font)
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return content


async def pic(text: str) -> str:
    """
    文字转图片
    :param text: 文字
    :return:
    """
    font_size = 30  # 字体大小
    lines = text.split('\n')
    # 画布颜色
    img = Image.new('RGB', (1080, len(lines) * (font_size + 7)), (255, 255, 255))  # (fontSize * (len(lines) + 10)
    dr = ImageDraw.Draw(img)
    # 字体样式
    font_data = await Resource.filter(type="字体").values()
    font = ImageFont.truetype(BytesIO(font_data[0]['file']), font_size)
    # 文字颜色
    dr.text((0, 0), text, font=font, fill="#000000")
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


async def to_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


async def distribute_area(user_id: int, area: str) -> dict:
    if area == "湖北":
        return await dxx.hubei(user_id=user_id)
    elif area == "江西":
        return await dxx.jiangxi(user_id=user_id)
    elif area == "浙江":
        return await dxx.zhejiang(user_id=user_id)
    elif area == "上海":
        return await dxx.shanghai(user_id=user_id)
    elif area == "江苏":
        return await dxx.jiangsu(user_id=user_id)
    elif area == "安徽":
        return await dxx.anhui(user_id=user_id)

async def distribute_area_url(province: str, user_id: int, group_id: int) -> str:
    setting = await Admin.filter(user_id=int(list(SUPERS)[0])).values()
    if province == "湖北":
        province = "hubei"
    elif province == "江西":
        province = "jiangxi"
    elif province == "江苏":
        province = "jiangsu"
    elif province == "安徽":
        province = "anhui"
    return f"http://{setting[0]['ip']}:{get_driver().config.port}/TeenStudy/api/{province}?user_id={user_id}&group_id={group_id}"


async def get_qrcode(user_id: int, group_id: int, area: str) -> str:
    setting = await Admin.filter(user_id=int(list(SUPERS)[0])).values()
    if area == "浙江":
        data = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx56b888a1409a2920&redirect_uri=https://wx.yunban.cn/wx/oauthInfoCallback?r_uri=http://{setting[0]['ip']}:{get_driver().config.port}/TeenStudy/api/zhejiang/{user_id}/{group_id}&source=common&response_type=code&scope=snsapi_userinfo&state=STATE&component_appid=wx0f0063354bfd3d19&connect_redirect=1"
    else:
        data = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa693f4127cc93fad&redirect_uri=https://wx.yunban.cn/wx/oauthInfoCallback?r_uri=http://{setting[0]['ip']}:{get_driver().config.port}/TeenStudy/api/shanghai/{user_id}/{group_id}&source=common&response_type=code&scope=snsapi_userinfo&state=STATE&component_appid=wx0f0063354bfd3d19&connect_redirect=1"
    img = qrcode.make(data=data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return content
