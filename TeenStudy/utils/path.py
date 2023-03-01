from pathlib import Path
from typing import Optional, Union

from nonebot import logger
from tortoise import Tortoise

from ..models import accuont, dxx

# 插件基础数据
DATABASE_PATH = Path().cwd() / 'data' / 'TeenStudy'

DATABASE_PATH.mkdir(parents=True, exist_ok=True)
PATH = DATABASE_PATH / "database.db"

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
