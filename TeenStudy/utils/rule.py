import datetime
from typing import Union

from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, NotifyEvent
from nonebot.params import CommandArg

from ..models.accuont import User
from ..models.dxx import PushList


async def must_group(bot: Bot, event: Union[MessageEvent, NotifyEvent]) -> bool:
    """
    必须是群消息才响应
    :param bot: 机器人
    :param event: 事件
    :return: 返回True或False
    """
    if isinstance(event, MessageEvent):
        if event.message_type == "group":
            self_id = int(bot.self_id)
            group_id = event.group_id
            if await PushList.filter(group_id=group_id, status=True, self_id=self_id).count():
                return True

        else:
            return False
    else:
        try:
            group_id = event.group_id
        except AttributeError:
            return False
        self_id = int(bot.self_id)
        if await PushList.filter(group_id=group_id, status=True, self_id=self_id).count():
            return True
        return False


async def must_command(order: Message = CommandArg()) -> bool:
    """
    限制指令后面不能加内容才生效
    :param order: 指令后面的内容
    :return: 返回True或False
    """
    if order:
        return False
    else:
        return True


async def must_leader(bot: Bot, event: MessageEvent) -> bool:
    """
    只有团支书发送才生效
    :param bot: 机器人id
    :param event: 消息事件
    :return:
    """
    if event.message_type == "group":
        self_id = int(bot.self_id)
        group_id = event.group_id
        user_id = event.user_id
        if await User.filter(leader=user_id, group_id=group_id).count():
            return True
    else:
        return False


async def check_poke(event: NotifyEvent) -> bool:
    """
    判断是否为戳一戳消息通知
    :param event: 通知事件
    :return: 返回True或False
    """
    if event.sub_type in ["poke"]:
        return True
    else:
        return False


async def check_time():
    now_day = datetime.datetime.now().weekday()
    now_hour = datetime.datetime.now().hour
    if now_day in [0, 5, 6]:
        if now_day in [5, 6]:
            return False
        else:
            if now_hour in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                return False
    return True
