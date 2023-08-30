from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from . import models, utils, web

__plugin_meta__ = PluginMetadata(
    name='TeenStudy',
    description='一个可以自动提交青年大学习的插件',
    usage='添加大学习',
    homepage="https://github.com/YouthLearning/TeenStudy",
    type="application",
    supported_adapters={"~onebot.v11"},
    extra={
        'author': 'ZM25XC TeenStudyFlow',
        'version': '0.2.2',
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
