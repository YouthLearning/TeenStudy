import random
import string
import time

from nonebot import logger

from ...models.accuont import User
from ...models.dxx import JiangXi
from ...utils.utils import to_hash


async def get_openid() -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, 28))


async def write_to_database(data: dict) -> bool:
    try:
        if data["password"]:
            data["password"] = await to_hash(str(data["password"]))
        else:
            data["password"] = await to_hash(str(data["user_id"]))
        if data["area"] in ["湖北", "江西"]:
            data["openid"] = await get_openid()
            if data["area"] == "江西":
                result = await JiangXi.filter(organization_id=data["dxx_id"]).values()
                data["organization"] = result[0]["organization"]
                data["university_id"] = result[0]["university_id"]
                data["college_id"] = result[0]["college_id"]
                data["organization_id"]=data["dxx_id"]
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
            "commit_time": None
        }
        start.update(data)
        await User.create(**start)
        return True
    except Exception as e:
        logger.error(e)
        return False
