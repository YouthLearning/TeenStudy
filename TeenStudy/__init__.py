from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from . import models, utils, web

__plugin_meta__ = PluginMetadata(
    name='TeenStudy',
    description='一个可以自动提交青年大学习的插件',
    usage='...',
    extra={
        'author': 'ZM25XC',
        'version': '0.1.7',
        'priority': 50,
    }
)

DRIVER = get_driver()


@DRIVER.on_startup
async def startup():
    await utils.path.connect()
    await utils.utils.admin_init()
    await utils.utils.plugin_init()
    await utils.utils.resource_init()
    await utils.update.update_answer()


DRIVER.on_shutdown(utils.path.disconnect)
