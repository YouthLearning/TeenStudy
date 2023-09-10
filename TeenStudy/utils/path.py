import json
from pathlib import Path
from typing import Optional, Union

from nonebot import logger
from pydantic import BaseModel
from tortoise import Tortoise

from ..models import accuont, dxx

# 插件基础数据
DATABASE_PATH = Path().cwd() / 'data' / 'TeenStudy'

DATABASE_PATH.mkdir(parents=True, exist_ok=True)
PATH = DATABASE_PATH / "database.db"
CONFIG_PATH = DATABASE_PATH / "config.json"
DATABASE = {
    'connections': {
        'TeenStudy_database': {
            'engine': 'tortoise.backends.sqlite',
            'credentials': {'file_path': PATH},
        }
    },
    "apps": {
        'TeenStudy_database': {
            'models': [accuont.__name__,
                       dxx.__name__],
            'default_connection': 'TeenStudy_database',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


class Config(BaseModel):
    DXX_IP: str = "127.0.0.1"
    """大学习访问IP"""
    DXX_PORT: int = None
    """大学习访问端口"""
    SUPERUSER: int = None
    """超管账号"""
    KEY: str = "d82ffad91168fb324ab6ebc2bed8dacd43f5af8e34ad0d1b75d83a0aff966a06"
    """大学习秘钥，为64位哈希散列值，用于生成token"""
    ALGORITHM: str = "HS256"
    """加密算法"""
    TOKEN_TIME: int = 30
    """token时效"""
    PASSWORD: str = None
    """后台登录算法"""
    DXX_REMIND: bool = True
    """周一检测更新提醒"""
    DXX_REMIND_HOUR: int = 9
    """大学习更新提醒时间-小时，可填范围：0-23"""
    DXX_REMIND_MINUTE: int = 0
    """大学习更新提醒时间-分钟，可选范围：0-59"""
    POKE_SUBMIT: bool = True
    """戳一戳提交大学习状态"""
    AUTO_SUBMIT: bool = True
    """周一11:30自动提交状态"""
    AUTO_SUBMIT_HOUR: int = 11
    """大学习自动提交时间-小时，可选范围：0-23"""
    AUTO_SUBMIT_MINUTE: int = 30
    """大学习自动提交时间-分钟，可选范围：0-59"""
    URL_STATUS: bool = False
    """是否将二维码转链接发送，默认为False"""


def saveConfig(data: dict) -> bool:
    try:
        config = Config().dict()
        config.update(**data)
        with open(CONFIG_PATH, "w", encoding="utf-8") as w:
            json.dump(config, w, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(e)
        return False


def getConfig() -> dict:
    if not Path(CONFIG_PATH).exists():
        status = saveConfig({
        })
        if status:
            return Config().dict()
    else:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            obj = json.load(f)
        if "URL_STATUS" not in obj.keys():
            obj["URL_STATUS"] = False
            with open(CONFIG_PATH, "w", encoding="utf-8") as w:
                json.dump(obj, w, indent=4, ensure_ascii=False)
        return obj


def register_database(db_name: str, models: str, db_path: Optional[Union[str, Path]]):
    """
    注册数据库
    :param db_name: 数据库名称
    :param models: 数据存储模型
    :param db_path: 数据存储路径
    :return:
    """
    if db_name in DATABASE['connections'] and db_name in DATABASE['apps']:
        DATABASE['apps'][db_name]['models'].append(models)
    else:
        DATABASE['connections'][db_name] = {
            'engine': 'tortoise.backends.sqlite',
            'credentials': {'file_path': db_path},
        }
        DATABASE['apps'][db_name] = {
            'models': [models],
            'default_connection': db_name,
        }


async def connect():
    """
    建立数据库连接
    """
    try:
        await Tortoise.init(DATABASE)
        await Tortoise.generate_schemas()
        logger.opt(colors=True).success('<u><y>[大学习数据库]</y></u><g>➤➤➤➤➤连接成功✔✔✔✔✔</g>')
    except Exception as e:
        logger.opt(colors=True).warning(f'<u><y>[大学习数据库]</y></u><r>➤➤➤➤➤连接失败✘✘✘✘✘:{e}</r>')
        raise e


async def disconnect():
    """
    断开数据库连接
    """
    await Tortoise.close_connections()
    logger.opt(colors=True).success('<u><y>[大学习数据库]</y></u><r>◄◄◄◄◄连接已断开✘✘✘✘✘</r>')
