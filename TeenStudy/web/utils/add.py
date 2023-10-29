import random
import string
import time

from nonebot import logger

from ...models.accuont import User
from ...utils.utils import to_hash


async def get_openid() -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, 28))


async def write_to_database(data: dict) -> bool:
    try:
        if data["password"]:
            data["password"] = await to_hash(str(data["password"]))
        else:
            data["password"] = await to_hash(str(data["user_id"]))
        if await User.filter(user_id=int(data["user_id"])).count():
            return False
        if data["area"] in ["湖北"]:
            data["openid"] = await get_openid()
        start = {
            "time": time.time(),
            "user_id": None,
            "area": None,
            "name": None,
            "password": None,
            "group_id": None,
            "gender": None,
            "mobile": None,
            "leader": None,
            "openid": None,
            "dxx_id": None,
            "university_type": None,
            "university_id": None,
            "university": None,
            "college_id": None,
            "college": None,
            "organization_id": None,
            "organization": None,
            "token": None,
            "cookie": None,
            "catalogue": None,
            "auto_submit": True,
            "commit_time": None
        }
        start.update(data)
        await User.create(**start)
        return True
    except Exception as e:
        logger.error(e)
        return False
