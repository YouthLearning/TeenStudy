import datetime

from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent, MessageEvent, NotifyEvent
from nonebot.params import CommandArg


async def must_owner(bot: Bot, event: GroupMessageEvent) -> bool:
    """
    机器人必须为群主才能响应
    :param bot :机器人
    :param event: 事件
    :return: 返回True或者False
    """
    self_id = int(bot.self_id)
    group_id = event.group_id
    result = await bot.get_group_member_info(group_id=group_id, user_id=self_id)
    if result:
        role = result['role']
        if role == "owner":
            return True
        return False
    return False


async def must_admin(bot: Bot, event: GroupMessageEvent) -> bool:
    """
        机器人必须为群管理才能响应
        :param bot :机器人
        :param event: 事件
        :return: 返回True或者False
        """
    self_id = int(bot.self_id)
    group_id = event.group_id
    result = await bot.get_group_member_info(group_id=group_id, user_id=self_id)
    if result:
        role = result['role']
        if role in ["owner", "admin"]:
            return True
        return False
    return False


async def must_group(bot: Bot, event: MessageEvent) -> bool:
    """
    必须是群消息才响应
    :param bot: 机器人
    :param event: 事件
    :return: 返回True或False
    """
    if event.message_type == "group":
        self_id = int(bot.self_id)
        group_id = event.group_id
        result = await bot.get_group_member_info(group_id=group_id, user_id=self_id)
        if result:
            role = result['role']
            if role in ["owner", "admin"]:
                return True
    else:
        return False


async def must_private(event: MessageEvent) -> bool:
    """
    必须是私聊消息才响应
    :param event:
    :return:
    """
    if event.message_type == "group":
        return False
    else:
        return True


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
