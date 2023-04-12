import asyncio
import datetime
import random
import socket
import time

from nonebot import get_driver, on_notice, require, get_bot
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot, GROUP, Message, MessageEvent, \
    PokeNotifyEvent
from nonebot.params import ArgStr, T_State, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import Rule

from .path import getConfig, saveConfig
from .rule import must_command, check_poke, check_time, must_group, must_leader
from .utils import get_end_pic, distribute_area, distribute_area_url, get_answer_pic, get_qrcode, get_login_qrcode, \
    to_hash
from ..models.accuont import User, AddUser
from ..models.dxx import Area, Answer, PushList

scheduler = require('nonebot_plugin_apscheduler').scheduler
SUPERS = get_driver().config.superusers
CONFIG = getConfig()

end_pic = on_command("end_pic", aliases={"完成截图", "大学习截图"}, permission=SUPERUSER | GROUP, rule=Rule(must_command,must_group),
                     priority=50)

submit = on_command("submit", aliases={"提交大学习"}, permission=SUPERUSER | GROUP, rule=Rule(must_command, must_group),
                    priority=50)
add = on_command("add_dxx", aliases={"添加大学习"}, permission=GROUP, rule=must_group, priority=50)
my_info = on_command("my_info", aliases={"我的大学习"}, permission=SUPERUSER | GROUP, rule=Rule(must_command,must_group), priority=50)
poke_notify = on_notice(priority=60, rule=check_poke)
answer_pic = on_command("answer_pic", aliases={"答案截图", "大学习"}, rule=Rule(must_command,must_group), permission=SUPERUSER | GROUP,
                        priority=50)
finish_dxx = on_command("finish_dxx", aliases={"完成大学习", "全员大学习"},
                        rule=Rule(must_command, must_group, must_leader), permission=GROUP | SUPERUSER, priority=50)
reset_config = on_command("reset_config", aliases={"重置配置", "刷新配置"}, permission=SUPERUSER, rule=must_command,
                          priority=50)
reset_password = on_command("reset_password", aliases={"重置密码"}, permission=GROUP,
                            rule=Rule(must_command, must_group), priority=50)
delete_dxx = on_command("delete_dxx", aliases={"删除大学习"}, priority=50, rule=Rule(must_command, must_group))


@end_pic.handle()
async def test_() -> None:
    await end_pic.finish(
        message=MessageSegment.text("青年大学习最新一期完成截图") + MessageSegment.image(await get_end_pic()),
        at_sender=True, reply_message=True)


@submit.handle()
async def submit_(event: GroupMessageEvent) -> None:
    user_id = event.user_id
    result = await User.filter(user_id=user_id).values()
    if result:
        if not await check_time():
            await submit.finish(
                message=MessageSegment.text("当前时间段禁止提交青年大学习，请在周一11:00之后再提交哦(｡･ω･｡)"),
                at_sender=True, reply_message=True)
        area = result[0]['area']
        data = await distribute_area(user_id=user_id, area=area)
        if data['status'] == 0:
            message = f'青年大学习{data["catalogue"]}提交成功( ･´ω`･ )\n个人详细信息可扫码登录查看(｡･ω･｡)'
            await submit.send(message=MessageSegment.text(message) + MessageSegment.image(await get_login_qrcode()),
                              at_sender=True, reply_message=True)
            await asyncio.sleep(1)
            await submit.finish(
                message=MessageSegment.text("青年大学习最新一期完成截图") + MessageSegment.image(await get_end_pic()),
                at_sender=True, reply_message=True)
        await submit.finish(message=MessageSegment.text(data['msg']), at_sender=True, reply_message=True)
    else:
        await submit.finish(message=MessageSegment.text("用户数据不存在！请使用 添加大学习 指令添加(｡･ω･｡)"),
                            at_sender=True, reply_message=True)


@add.handle()
async def add_(state: T_State, event: GroupMessageEvent, msg: Message = CommandArg()) -> None:
    user_id = event.user_id
    if await User.filter(user_id=user_id).count():
        await add.finish(message=MessageSegment.text("你已经添加过了，不要重复添加哦( • ̀ω•́ )✧"), at_sender=True,
                         reply_message=True)
    if str(msg):
        state['province'] = str(msg)


@add.got(key="province", prompt="请输入需要添加的省份或回复 取消 停止操作！")
async def add_(event: GroupMessageEvent, province: str = ArgStr("province")) -> None:
    group_id = event.group_id
    user_id = event.user_id
    if province in ["取消", "No", "停止", "NO"]:
        await add.finish(message=MessageSegment.text("操作取消！φ(>ω<*) "), at_sender=True, reply_message=True)
    if await Area.filter(area=province).count():
        url = await distribute_area_url(province=province, user_id=user_id, group_id=group_id)
        if province in ["上海", "浙江"]:
            result = await add.send(
                message=MessageSegment.text("请使用微信扫码进行绑定( ･´ω`･ )") + MessageSegment.image(
                    await get_qrcode(user_id=user_id, group_id=group_id, area=province)), at_sender=True,
                reply_message=True)
        else:
            result = await add.send(
                message=MessageSegment.text(f"请扫码进入网页添加绑定( ･´ω`･ )") + MessageSegment.image(url),
                at_sender=True,
                reply_message=True)
        await AddUser.create(
            time=time.time(),
            user_id=user_id,
            group_id=group_id,
            area=province,
            message_id=result["message_id"],
            status="未通过"
        )
    else:
        await add.reject(
            prompt=MessageSegment.text(
                "该省份暂不支持或输入省份名称（名称不要带省字）错误，请重新输入或回复 取消 停止操作( ･´ω`･ )"),
            at_sender=True,
            reply_message=True)


@my_info.handle()
async def my_info_(event: MessageEvent) -> None:
    user_id = event.user_id
    if await User.filter(user_id=user_id).count():
        await my_info.finish(
            message=MessageSegment.text('请扫码登录查看哦(｡･ω･｡)') + MessageSegment.image(await get_login_qrcode()),
            at_sender=True, reply_message=True)
    else:
        await my_info.finish(
            message=MessageSegment.text("你还没有绑定大学习哦ヾ(ｏ･ω･)ﾉ，使用 添加大学习 指令进行绑定信息吧( • ̀ω•́ )✧"),
            at_sender=True, reply_message=True)


@poke_notify.handle()
async def poke_notify_(bot: Bot, event: PokeNotifyEvent):
    config = getConfig()
    if not config["POKE_SUBMIT"]:
        return
    try:
        group_id = event.group_id
    except AttributeError:
        group_id = None
    user_id = event.user_id
    target_id = event.target_id
    if target_id != int(bot.self_id):
        return
    if group_id:
        result = await User.filter(user_id=user_id).values()
        if result:
            if not await check_time():
                await submit.finish(
                    message=MessageSegment.text("当前时间段禁止提交青年大学习，请在周一11:00之后再提交哦(｡･ω･｡)"),
                    at_sender=True)
            area = result[0]['area']
            data = await distribute_area(user_id=user_id, area=area)
            if data['status'] == 0:
                message = f'青年大学习{data["catalogue"]}提交成功( ･´ω`･ )\n个人详细信息请扫码登录查看(｡･ω･｡)'
                await poke_notify.send(
                    message=MessageSegment.text(message) + MessageSegment.image(await get_login_qrcode()),
                    at_sender=True)
                await asyncio.sleep(1)
                await poke_notify.finish(
                    message=MessageSegment.text("青年大学习最新一期完成截图") + MessageSegment.image(
                        await get_end_pic()), at_sender=True,
                    reply_message=True)
            await poke_notify.finish(message=MessageSegment.text(data['msg']), at_sender=True, reply_message=True)
        else:
            await poke_notify.finish(
                message=MessageSegment.text("用户数据不存在！请使用 添加大学习 指令进行绑定(*^▽^*)"), at_sender=True,
                reply_message=True)
    else:
        await bot.send_private_msg(user_id=user_id,
                                   message=MessageSegment.at(user_id) + MessageSegment.text("别戳啦(~￣△￣)~"))


@answer_pic.handle()
async def answer_pic_() -> None:
    await answer_pic.finish(message=MessageSegment.image(await get_answer_pic()), at_sender=True, reply_message=True)


@finish_dxx.handle()
async def finish() -> None:
    if not await check_time():
        await submit.finish(
            message=MessageSegment.text("当前时间段禁止提交青年大学习，请在周一11:00之后再发指令哦(｡･ω･｡)"),
            at_sender=True, reply_message=True)


@finish_dxx.got(key="msg", prompt="是否提交团支部全体成员最新一期青年大学习？（是|否）")
async def finish(event: GroupMessageEvent, msg: str = ArgStr("msg")) -> None:
    if msg not in ["是", "yes", "Y", "y", "YES", "true"]:
        await finish_dxx.finish(message=MessageSegment.text("操作取消(*^▽^*)"), at_sender=True, reply_message=True)
    else:
        await finish_dxx.send(message=MessageSegment.text("开始提交(*￣︶￣)"), at_sender=True, reply_message=True)
    self_id = event.self_id
    group_id = event.group_id
    user_id = event.user_id
    result = await User.filter(leader=user_id, group_id=group_id).values()
    if result:
        answer_result = await Answer.all().order_by('time').values()
        catalogue = answer_result[-1]["catalogue"]
        for item in result:
            if item["catalogue"] == catalogue:
                continue
            else:
                await distribute_area(user_id=item["user_id"], area=item["area"])
                await asyncio.sleep(random.randint(10, 15))
    await finish_dxx.finish(message=MessageSegment.text("提交完成！"), at_sender=True, reply_message=True)


@reset_config.got(key="msg", prompt="是否重置大学习配置为默认配置？（是|否）")
async def reset_config_(event: MessageEvent, msg: str = ArgStr("msg")) -> None:
    user_id = event.user_id
    if msg not in ["是", "yes", "Y", "y", "YES", "true"]:
        await reset_config.finish(message=MessageSegment.text("操作取消(*^▽^*)"), at_sender=True, reply_message=True)
    else:
        try:
            ip = get_driver().config.dxx_ip
        except AttributeError:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('114.114.114.114', 12345))
            ip = s.getsockname()[0]
        data = {
            "TOKEN_TIME": 30,
            "SUPERUSER": user_id,
            "KEY": "d82ffad91168fb324ab6ebc2bed8dacd43f5af8e34ad0d1b75d83a0aff966a06",
            "ALGORITHM": "HS256",
            "PASSWORD": await to_hash("admin"),
            "DXX_IP": ip
        }
        status = saveConfig(data=data)
        if status:
            await reset_config.finish(message=MessageSegment.text("重置成功(oﾟ▽ﾟ)o  "), at_sender=True,
                                      reply_message=True)
        else:
            await reset_config.finish(message=MessageSegment.text("重置失败╮(╯﹏╰）╭ "), at_sender=True,
                                      reply_message=True)


@reset_password.handle()
async def reset_password_(event: MessageEvent) -> None:
    user_id = event.user_id
    result = await User.filter(user_id=user_id).count()
    if not result:
        await reset_password.finish(message=MessageSegment.text("重置失败，用户数据不存在！( ･´ω`･ )"), at_sender=True,
                                    reply_message=True)


@reset_password.got(key="msg", prompt="是否重置大学习登录密码？（是|否）")
async def reset_password_(event: MessageEvent, msg: str = ArgStr("msg")) -> None:
    user_id = event.user_id
    if msg not in ["是", "yes", "Y", "y", "YES", "true"]:
        await reset_password.finish(message=MessageSegment.text("操作取消(*^▽^*)"), at_sender=True, reply_message=True)
    else:
        await User.filter(user_id=user_id).update(
            password=await to_hash(str(user_id))
        )
        await reset_password.finish(message=MessageSegment.text("登录密码重置成功，默认为用户QQ(๑*◡*๑)"),
                                    at_sender=True, reply_message=True)


@delete_dxx.handle()
async def delete_dxx_(event: GroupMessageEvent, state: T_State) -> None:
    user_id = event.user_id
    result = await User.filter(user_id=user_id).values("id")
    if result:
        state["id"] = result[0]["id"]
    else:
        await delete_dxx.finish(message=MessageSegment.text("操作失败，用户数据不存在(*^▽^*)"), at_sender=True,
                                reply_message=True)


@delete_dxx.got(key="msg", prompt="是否删除大学习数据？（是|否）")
async def delete_dxx_(state: T_State, msg: str = ArgStr("msg")) -> None:
    if msg not in ["是", "yes", "Y", "y", "YES", "true"]:
        await delete_dxx.finish(message=MessageSegment.text("操作取消(*^▽^*)"), at_sender=True, reply_message=True)
    else:
        await User.filter(id=state["id"]).delete()
        await delete_dxx.finish(message=MessageSegment.text("删除成功(*^▽^*)"), at_sender=True, reply_message=True)


@scheduler.scheduled_job('cron', day_of_week='0', hour=CONFIG["DXX_REMIND_HOUR"], minute=CONFIG["DXX_REMIND_MINUTE"],
                         id='push_dxx', timezone="Asia/Shanghai")
async def push_dxx() -> None:
    config = getConfig()
    if not config["DXX_REMIND"]:
        return
    try:
        bot: Bot = get_bot()
    except ValueError as e:
        return None
    answer_result = await Answer.all().order_by('time').values()
    if (int(time.time()) - answer_result[-1]["time"]) > 259200:
        return None
    else:
        catalogue = answer_result[-1]["catalogue"]
        now_time = datetime.datetime.fromtimestamp(answer_result[-1]["time"]).strftime("%Y年%m月%d日 %H:%M:%S")
        message = f'\n本周的大学习开始喽!\n{catalogue}\n更新时间：{now_time}\n答案见图一\n完成截图见图二\nPs:当11:00:00以后，可使用 提交大学习 指令或戳一戳Bot完成大学习!'
        push_list = await PushList.filter(status=True).values()
        for item in push_list:
            try:
                await bot.send_group_msg(group_id=item["group_id"],
                                         message=MessageSegment.at("all") + MessageSegment.text(
                                             message) + MessageSegment.image(
                                             await get_answer_pic()) + MessageSegment.image(await get_end_pic()))
                await asyncio.sleep(random.randint(15, 30))
            except Exception as e:
                logger.error(e)
                continue


@scheduler.scheduled_job('cron', day_of_week='0', hour=CONFIG["AUTO_SUBMIT_HOUR"], minute=CONFIG["AUTO_SUBMIT_MINUTE"],
                         id='auto_dxx', timezone="Asia/Shanghai")
async def auto_dxx() -> None:
    config = getConfig()
    if not config["AUTO_SUBMIT"]:
        return
    answer_result = await Answer.all().order_by('time').values()
    if (int(time.time()) - answer_result[-1]["time"]) > 259200:
        return None
    else:
        user_list = await User.all().values("id", "area", "catalogue", "user_id")
        catalogue = answer_result[-1]["catalogue"]
        for item in user_list:
            result = await User.filter(id=item["id"]).values("id", "area", "catalogue", "user_id", "auto_submit")
            if result[0]["catalogue"] == catalogue or not result[0]["auto_submit"]:
                continue
            else:
                await distribute_area(user_id=item["user_id"], area=item["area"])
                await asyncio.sleep(random.randint(15, 45))
