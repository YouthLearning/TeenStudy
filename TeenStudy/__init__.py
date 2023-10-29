from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from . import models, utils, web

__plugin_meta__ = PluginMetadata(
    name='青年大学习提交',
    description='一个可以自动提交多地区青年大学习的插件',
    usage='添加大学习',
    homepage="https://github.com/YouthLearning/TeenStudy",
    type="application",
    supported_adapters={"~onebot.v11"},
    extra={
        'author': 'TeenStudyFlow',
        'version': '0.2.4',
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
    await utils.update.update_shanxi()
    await utils.update.update_shandong()
    await utils.update.update_jiangxi()


DRIVER.on_shutdown(utils.path.disconnect)
