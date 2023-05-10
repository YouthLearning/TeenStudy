import base64
import datetime
import hashlib
import json
import os
import random
import socket
import time
from io import BytesIO
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont
from httpx import AsyncClient
from nonebot import logger, get_driver, on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import ArgStr
from nonebot.permission import SUPERUSER
from pydantic import BaseModel

from . import dxx, path, rule
from ..models.accuont import User
from ..models.dxx import Area, Answer, Resource, JiangXi

USERDATA = path.DATABASE_PATH / "users.json"


class UserModel(BaseModel):
    id: int = None
    """用户ID"""
    time: int = None
    """添加时间戳"""
    self_id: int = None
    """BOT ID"""
    user_id: int = None
    """用户ID"""
    password: str = None
    """登录密码，用于登录web端"""
    group_id: int = None
    """通知群号"""
    name: str = None
    """姓名"""
    gender: str = None
    """性别"""
    mobile: str = None
    """手机号"""
    area: str = None
    """地区"""
    leader: int = None
    """团支书ID"""
    openid: str = None
    """微信认证ID"""
    dxx_id: str = None
    """大学习用户id,nid或uid"""
    university_type: str = None
    """学校类型"""
    university_id: str = None
    """学校id"""
    university: str = None
    """学校名称"""
    college_id: str = None
    """学院id"""
    college: str = None
    """学院名称"""
    organization_id: str = None
    """团支部id"""
    organization: str = None
    """团支部名称"""
    token: str = None
    """提交需要的token"""
    cookie: str = None
    """提交要用的cookie"""
    catalogue: str = None
    """提交期数"""
    auto_submit: bool = True
    """自动提交状态"""
    commit_time: int = None
    """提交时间"""


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
    },
    {
        "area": "安徽",
        "host": "dxx.ahyouth.org.cn",
        "referer": "http://dxx.ahyouth.org.cn/",
        "origin": "http://dxx.ahyouth.org.cn",
        "url": "http://dxx.ahyouth.org.cn/api/hidtoryList",
        "status": True,
        "catalogue": None
    },
    {
        "area": "四川",
        "host": "dxx.scyol.com",
        "referer": "http://scyol.com/v_prod6.02/",
        "origin": "http://scyol.com",
        "url": "https://dxx.scyol.com/api/student/commit",
        "status": True,
        "catalogue": None
    },
    {
        "area": "山东",
        "host": "qndxx.youth54.cn",
        "referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=pageSdtwdt",
        "origin": "http://qndxx.youth54.cn",
        "url": "http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getNewestVersionInfo&openid=",
        "status": True,
        "catalogue": None
    },
    {
        "area": "重庆",
        "host": "qndxx.cqyouths.com",
        "referer": None,
        "origin": "http://qndxx.cqyouths.com",
        "url": "http://qndxx.cqyouths.com/new_course.json?time=",
        "status": True,
        "catalogue": None
    },
    {
        "area": "吉林",
        "host": "jqfy.jl54.org",
        "referer": None,
        "origin": "http://jqfy.jl54.org/jltw/wechat",
        "url": "http://jqfy.jl54.org/jltw/wechat",
        "status": True,
        "catalogue": None
    },
    {
        "area": "广东",
        "host": "tuanapi.12355.net",
        "referer": None,
        "origin": "https://tuan.12355.net",
        "url": "https://youthstudy.12355.net/saomah5/api/young/chapter/new",
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

export_data = on_command("export_data", aliases={"导出用户数据", "导出数据"}, priority=50, permission=SUPERUSER,
                         rule=rule.must_command)
update_users = on_command("update_user", aliases={"更新用户数据", "刷新用户数据"}, priority=50, permission=SUPERUSER,
                          rule=rule.must_command)
update_resource = on_command("update_resource", aliases={"更新资源数据", "刷新资源数据"}, priority=50,
                             permission=SUPERUSER, rule=rule.must_command)


@update_resource.got(key="msg", prompt="是否刷新资源数据库信息？（是|否）")
async def update_resource_(msg: str = ArgStr("msg")) -> None:
    if msg not in ["是", "yes", "Y", "y", "YES", "true"]:
        await update_resource.finish(message="操作取消(*^▽^*)", at_sender=True, reply_message=True)
    else:
        await update_resource.send("资源重新载入中（请等待1分钟左右）······", at_sender=True, reply_message=True)
        await JiangXi.all().delete()
        await Resource.all().delete()
        await resource_init()
        await update_resource.finish(message="资源数据载入成功(^_−)☆", at_sender=True, reply_message=True)


@export_data.got(key="msg", prompt="是否导出用户数据至TeenStudy目录？（是|否）")
async def export_user(event: MessageEvent, msg: str = ArgStr("msg")) -> None:
    self_id = event.self_id
    if msg not in ["是", "yes", "Y", "y", "YES", "true"]:
        await export_data.finish(message="操作取消(*^▽^*)", at_sender=True, reply_message=True)
    else:
        result = await User.all().values()
        user_list = []
        for item in result:
            data = UserModel().dict()
            item["self_id"] = self_id
            data.update(**item)
            user_list.append(data)
        with open(USERDATA, "w", encoding="utf-8") as w:
            json.dump(user_list, w, indent=4, ensure_ascii=False)
        await export_data.finish(message="用户数据成功导出至TeenStudy目录(*^▽^*)", at_sender=True,
                                 reply_message=True)


@update_users.handle()
async def update_user() -> None:
    if not Path(USERDATA).exists():
        await update_users.finish(
            message="更新失败，没有找到可导入用户数据文件，请确保TeeStudy数据目录下存有用户数据文件╮(╯﹏╰）╭",
            at_sender=True, reply_message=True)


@update_users.got(key="msg", prompt="是否覆盖更新用户数据?（是|否）")
async def update_user() -> None:
    with open(USERDATA, "r", encoding="utf-8") as f:
        data_obj = json.load(f)
    await User.all().delete()
    for item in data_obj:
        data = UserModel().dict()
        data.update(**item)
        await User.create(**data)
    await update_users.finish(message="用户数据更新完成(*^▽^*)", at_sender=True, reply_message=True)


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
    try:
        superuser = int(list(get_driver().config.superusers)[0])
    except AttributeError:
        superuser = -1
        logger.error("请配置好超管账号，之后重启nonebot2")
    try:
        ip = get_driver().config.dxx_ip
    except AttributeError:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 12345))
        ip = s.getsockname()[0]
    result = path.getConfig()
    if result["DXX_IP"] == ip and result["SUPERUSER"] == superuser:
        return
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41"
        }
        try:
            logger.opt(colors=True).info(
                f'<u><y>[大学习数据库]</y></u><g>加载配置公网IP</g>')
            ip = get_driver().config.dxx_ip
            logger.opt(colors=True).info(
                f'<u><y>[大学习数据库]</y></u><g>加载配置公网IP成功，启动检测公网IP访问状态</g>ip:<m>{ip}</m>')
            url = f"http://{ip}:{get_driver().config.port}/TeenStudy/login"
            logger.info(url)
            try:
                async with AsyncClient(headers=headers) as client:
                    response = await client.get(url=url)
                logger.debug(f"公网请求状态：{response.status_code}")
                if response.status_code != 200:
                    ip = ""
                    logger.opt(colors=True).info(
                        f'<u><y>[大学习数据库]</y></u><g>检测到配置公网ip地址无法通过外网访问，将自动获取公网IP</g>')
                logger.opt(colors=True).success(
                    f'<u><y>[大学习提交 Web UI]</y></u><g>配置外网IP设置成功</g>，外网访问地址为:<m>http://{ip}:{get_driver().config.port}/TeenStudy/login</m>')
            except Exception as e:
                logger.error(e)
                ip = ""
                logger.opt(colors=True).info(
                    f'<u><y>[大学习数据库]</y></u><g>检测到配置公网ip地址无法通过外网访问，将自动配置局域网IP</g>')
        except AttributeError:
            ip = ''
            logger.opt(colors=True).info(
                f'<u><y>[大学习数据库]</y></u><g>加载配置IP失败，未检测到配置ip，启动自动获取公网IP</g>')
        if not ip:
            async with AsyncClient(headers=headers) as client:
                response = await client.get("http://ip.42.pl/raw")
            if response.status_code == 200:
                ip = response.text.strip()
                logger.opt(colors=True).info(
                    f'<u><y>[大学习数据库]</y></u><g>自动获取公网IP成功，启动检测公网IP访问状态</g>ip:<m>{ip}</m>')
                url = f"http://{ip}:{get_driver().config.port}/TeenStudy/login"
                logger.info(url)
                try:
                    async with AsyncClient(headers=headers, timeout=5) as client:
                        response = await client.get(url=url)
                    logger.debug(f"公网请求状态:{response.status_code}")
                    if response.status_code != 200:
                        ip = ""
                        logger.opt(colors=True).warning(
                            f'<u><y>[大学习数据库]</y></u><g>检测到ip地址无法通过外网访问，将自动配置局域网IP，请手动在.env.prod文件中配置公网IP，配置格式：DXX_IP="您的公网IP"</g>')
                    else:
                        logger.opt(colors=True).success(
                            f'<u><y>[大学习提交 Web UI]</y></u><g>自动获取外网IP成功</g>，外网访问地址为:<m>http://{ip}:{get_driver().config.port}/TeenStudy/login</m>')
                except Exception as e:
                    ip = ""
                    logger.debug(e)
                    logger.opt(colors=True).warning(
                        f'<u><y>[大学习数据库]</y></u><g>检测到ip地址无法通过外网访问，将自动配置局域网IP，请手动在.env.prod文件中配置公网IP，配置格式：DXX_IP="您的公网IP"</g>')
            else:
                ip = ""
                logger.opt(colors=True).warning(
                    f'<u><y>[大学习数据库]</y></u><g>自动获取公网IP失败，将自动配置局域网IP，请手动在.env.prod文件中配置公网IP，配置格式：DXX_IP="您的公网IP"</g>')
        if not ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('114.114.114.114', 12345))
            ip = s.getsockname()[0]
            logger.opt(colors=True).success(
                f'<u><y>[大学习提交 Web UI]</y></u><g>配置局域网IP成功</g>，局域网访问地址为:<m>http://{ip}:{get_driver().config.port}/TeenStudy/login</m>')
        data = {
            "TOKEN_TIME": 30,
            "SUPERUSER": int(list(SUPERS)[0]),
            "KEY": "d82ffad91168fb324ab6ebc2bed8dacd43f5af8e34ad0d1b75d83a0aff966a06",
            "ALGORITHM": "HS256",
            "PASSWORD": await to_hash("admin"),
            "DXX_IP": ip,
            "DXX_PORT": get_driver().config.port
        }
        path.saveConfig(data=data)


async def resource_init():
    base_file_path = os.path.dirname(__file__)[:-5] + "resource/"
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
    elif area == "四川":
        return await dxx.sichuan(user_id=user_id)
    elif area == "山东":
        return await dxx.shandong(user_id=user_id)
    elif area == "重庆":
        return await dxx.chongqing(user_id=user_id)
    elif area == "吉林":
        return await dxx.jilin(user_id=user_id)
    elif area == "广东":
        return await dxx.guangdong(user_id=user_id)
    else:
        return {
            "status": 404,
            "msg": "该地区暂未支持！"
        }


async def distribute_area_url(province: str, user_id: int, group_id: int) -> dict:
    config = path.getConfig()
    if province == "湖北":
        province = "hubei"
    elif province == "江西":
        province = "jiangxi"
    elif province == "江苏":
        province = "jiangsu"
    elif province == "安徽":
        province = "anhui"
    elif province == "四川":
        province = "sichuan"
    elif province == "山东":
        province = "shandong"
    elif province == "重庆":
        province = "chongqing"
    elif province == "吉林":
        province = "jilin"
    elif province == "广东":
        province="guangdong"
    data = f"http://{config['DXX_IP']}:{config['DXX_PORT']}/TeenStudy/api/{province}?user_id={user_id}&group_id={group_id}"
    img = qrcode.make(data=data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return {
        "url": data,
        "content": content
    }


async def get_login_qrcode() -> dict:
    config = path.getConfig()
    data = f'http://{config["DXX_IP"]}:{config["DXX_PORT"]}/TeenStudy/login'
    img = qrcode.make(data=data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return {
        "url": data,
        "content": content
    }


async def get_qrcode(user_id: int, group_id: int, area: str) -> dict:
    config = path.getConfig()
    if area == "浙江":
        data = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx56b888a1409a2920&redirect_uri=https://wx.yunban.cn/wx/oauthInfoCallback?r_uri=http://{config['DXX_IP']}:{config['DXX_PORT']}/TeenStudy/api/zhejiang/{user_id}/{group_id}&source=common&response_type=code&scope=snsapi_userinfo&state=STATE&component_appid=wx0f0063354bfd3d19&connect_redirect=1"
    else:
        data = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa693f4127cc93fad&redirect_uri=https://wx.yunban.cn/wx/oauthInfoCallback?r_uri=http://{config['DXX_IP']}:{config['DXX_PORT']}/TeenStudy/api/shanghai/{user_id}/{group_id}&source=common&response_type=code&scope=snsapi_userinfo&state=STATE&component_appid=wx0f0063354bfd3d19&connect_redirect=1"
    img = qrcode.make(data=data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    content = "base64://" + base64_str
    return {
        "url": data,
        "content": content
    }
