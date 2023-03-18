import asyncio
import datetime

import psutil
from nonebot import get_bot, get_driver

from ...models.accuont import User, Admin
from ...models.dxx import PushList, Answer, Area

DRIVER = get_driver()
start_time: str = ""


async def get_status():
    status_result = {
    }
    try:
        status_result['start_time'] = start_time
    except Exception:
        status_result['start_time'] = '未知'
    try:
        bot = get_bot()
        bot_info = await bot.get_login_info()
        status_result['bot_id'] = bot_info['user_id']
        status_result['nickname'] = bot_info['nickname']
        bot_friends = await bot.get_friend_list()
        bot_groups = await bot.get_group_list()
        status_result['friend_count'] = len(bot_friends)
        status_result['group_count'] = len(bot_groups)
        status_result['user_count'] = await User.all().count()
        status_result['area_count'] = await Area.all().count()
        answer = await Answer.all().order_by("time").values()
        title = answer[-1]["catalogue"]
        setting = await Admin.all().order_by("time").values()
        status_result["ip"]= setting[-1]["ip"]
        status_result['catalogue'] = title
        status_result['notice_count'] = await PushList.all().count()
    except Exception:
        status_result['bot_id'] = '未知'
        status_result['msg_received'] = '未知'
        status_result['msg_sent'] = '未知'

    status_result['system_start_time'] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
        "%Y-%m-%d %H:%M:%S")

    psutil.cpu_percent()
    await asyncio.sleep(0.1)
    cpu_percent = psutil.cpu_percent()
    # cpu_count = psutil.cpu_count(logical=False)
    # cpu_count_logical = psutil.cpu_count()
    # cpu_freq = psutil.cpu_freq()
    ram_stat = psutil.virtual_memory()
    swap_stat = psutil.swap_memory()
    status_result['cpu_percent'] = f'{cpu_percent}%'
    status_result['ram_percent'] = f'{ram_stat.percent}%'
    status_result['swap_percent'] = f'{swap_stat.percent}%'

    return status_result


@DRIVER.on_startup
async def start_up():
    global start_time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
