import asyncio
import datetime
import random
import time

from nonebot import get_driver, on_notice, require, get_bot
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot, GROUP, Message, MessageEvent, \
    PokeNotifyEvent
from nonebot.params import ArgStr, T_State, CommandArg
from nonebot.permission import SUPERUSER

from .rule import must_command, check_poke, check_time
from .utils import get_end_pic, distribute_area, distribute_area_url, get_answer_pic
from ..models.accuont import User, Admin, AddUser
from ..models.dxx import Area, Answer, PushList

scheduler = require('nonebot_plugin_apscheduler').scheduler
SUPERS = get_driver().config.superusers

end_pic = on_command("end_pic", aliases={"完成截图", "大学习截图"}, permission=SUPERUSER | GROUP, rule=must_command,
                     priority=50)

submit = on_command("submit", aliases={"提交大学习"}, permission=SUPERUSER | GROUP, rule=must_command, priority=50)
add = on_command("add_dxx", aliases={"添加大学习"}, permission=GROUP, priority=50)
my_info = on_command("my_info", aliases={"我的大学习"}, permission=SUPERUSER | GROUP, rule=must_command, priority=50)
poke_notify = on_notice(priority=60, rule=check_poke)
answer_pic = on_command("answer_pic", aliases={"答案截图", "大学习"}, rule=must_command, permission=SUPERUSER | GROUP,
                        priority=50)


@end_pic.handle()
async def test_() -> None:
    await end_pic.finish(message=MessageSegment.image(await get_end_pic()))


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
            setting = await Admin.filter(user_id=int(list(SUPERS)[0])).values()
            message = f'青年大学习{data["catalogue"]}提交成功( ･´ω`･ )\n个人详细信息请前往：http://{setting[0]["ip"]}:{get_driver().config.port}/TeenStudy/login 查看(｡･ω･｡)'
            await submit.send(message=MessageSegment.text(message), at_sender=True, reply_message=True)
            await asyncio.sleep(1)
            await submit.finish(message=MessageSegment.image(await get_end_pic()), at_sender=True, reply_message=True)
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


@add.got(key="province", prompt="请输入需要添加的省份或回复取消停止操作！")
async def add_(event: GroupMessageEvent, province: str = ArgStr("province")) -> None:
    group_id = event.group_id
    user_id = event.user_id
    if province in ["取消", "No", "停止", "NO"]:
        await add.finish(message=MessageSegment.text("操作取消！φ(>ω<*) "), at_sender=True, reply_message=True)
    if await Area.filter(area=province).count():
        url = await distribute_area_url(province=province, user_id=user_id, group_id=group_id)
        result = await add.send(message=MessageSegment.text(f"请前往{url}网页添加绑定( ･´ω`･ )"), at_sender=True,
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
                "该省份暂不支持或输入省份名称（名称不要带省字）错误，请重新输入或回复取消停止操作( ･´ω`･ )"),
            at_sender=True,
            reply_message=True)


@my_info.handle()
async def my_info_(event: MessageEvent) -> None:
    user_id = event.user_id
    if await User.filter(user_id=user_id).count():
        setting = await Admin.filter(user_id=int(list(SUPERS)[0])).values()
        await my_info.finish(message=MessageSegment.text(
            f'请前往：http://{setting[0]["ip"]}:{get_driver().config.port}/TeenStudy/login 查看哦(｡･ω･｡)'),
            at_sender=True, reply_message=True)
    else:
        await my_info.finish(
            message=MessageSegment.text("你还没有绑定大学习哦ヾ(ｏ･ω･)ﾉ，使用 添加大学习 指令进行绑定信息吧( • ̀ω•́ )✧"),
            at_sender=True, reply_message=True)


@poke_notify.handle()
async def poke_notify_(bot: Bot, event: PokeNotifyEvent):
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
                setting = await Admin.filter(user_id=int(list(SUPERS)[0])).values()
                message = f'青年大学习{data["catalogue"]}提交成功( ･´ω`･ )\n个人详细信息请前往：http://{setting[0]["ip"]}:{get_driver().config.port}/TeenStudy/login 查看(｡･ω･｡)'
                await poke_notify.send(message=MessageSegment.text(message), at_sender=True)
                await asyncio.sleep(1)
                await poke_notify.finish(message=MessageSegment.image(await get_end_pic()), at_sender=True,
                                         reply_message=True)
            await poke_notify.finish(message=MessageSegment.text(data['msg']), at_sender=True, reply_message=True)
        else:
            await poke_notify.finish(message=MessageSegment.text("用户数据不存在！"), at_sender=True, reply_message=True)
    else:
        await bot.send_private_msg(user_id=user_id,
                                   message=MessageSegment.at(user_id) + MessageSegment.text("别戳啦(~￣△￣)~"))


@answer_pic.handle()
async def answer_pic_() -> None:
    await answer_pic.finish(message=MessageSegment.image(await get_answer_pic()), at_sender=True, reply_message=True)


@scheduler.scheduled_job('cron', day_of_week='0', hour=9, minute=0, id='push_dxx', timezone="Asia/Shanghai")
async def push_dxx() -> None:
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


@scheduler.scheduled_job('cron', day_of_week='0', hour=11, minute=30, id='auto_dxx', timezone="Asia/Shanghai")
async def auto_dxx() -> None:
    try:
        bot: Bot = get_bot()
    except ValueError as e:
        return None
    answer_result = await Answer.all().order_by('time').values()
    if (int(time.time()) - answer_result[-1]["time"]) > 259200:
        return None
    else:
        user_list = await User.all().values()
        catalogue = answer_result[-1]["catalogue"]
        for item in user_list:
            if item["catalogue"] == catalogue:
                continue
            else:
                await distribute_area(user_id=item["user_id"], area=item["area"])
                await asyncio.sleep(random.randint(15, 45))
        admin = await Admin.all().values()
        message = f"\n本群所有已绑定成员已全部提交最新一期青年大学习，详细信息请登录后台：http://{admin[0]['ip']}:{get_driver().config.port}/TeenStudy/login 查看d(´ω｀*)"
        push_list = await PushList.filter(status=True).values()
        for item in push_list:
            try:
                await bot.send_group_msg(group_id=item["group_id"],
                                         message=MessageSegment.at("all") + MessageSegment.text(
                                             message) + MessageSegment.image(await get_end_pic()))
                await asyncio.sleep(random.randint(15, 30))
            except Exception as e:
                logger.error(e)
                continue
