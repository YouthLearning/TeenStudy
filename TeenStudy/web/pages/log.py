from amis import LevelEnum, ButtonGroupSelect, \
    Log, Alert, Form, Select, Group, PageSchema, Page

from ...utils.path import getConfig

CONFIG = getConfig()
SECRET_KEY = CONFIG["KEY"]
select_log_num = Select(
    label='日志数量',
    name='log_num',
    value=100,
    options=[
        {
            'label': 100,
            'value': 100
        },
        {
            'label': 200,
            'value': 200
        },
        {
            'label': 300,
            'value': 300
        },
        {
            'label': 400,
            'value': 400
        },
        {
            'label': 500,
            'value': 500
        }
    ]
)

select_log_level = ButtonGroupSelect(
    label='日志等级',
    name='log_level',
    btnLevel=LevelEnum.light,
    btnActiveLevel=LevelEnum.warning,
    value='info',
    options=[
        {
            'label': 'INFO',
            'value': 'info',
            "level": "primary"
        },
        {
            'label': 'DEBUG',
            'value': 'debug',
            "level": "primary"
        }
    ]
)

log_page = Log(
    autoScroll=True,
    disableColor=False,
    placeholder='暂无日志数据...',
    operation=['stop', 'showLineNumber', 'filter'],
    source={
        'method': 'get',
        'url': '/TeenStudy/api/log?level=${log_level | raw}&num=${log_num | raw}',
        'headers': {
            'token': SECRET_KEY[:16]
        }
    }
)
page_detail = Page(title='', body=[Alert(level=LevelEnum.info,
                                         body='查看最近最多500条日志，不会自动刷新，需要手动点击两次"暂停键"来进行刷新，DEBUG日志需要Nonebot日志模式为DEBUG才能查看。'),
                                   Form(title="", interval=180000,
                                        body=[Group(body=[select_log_num, select_log_level]), log_page], submitText=''
                                        )])
page_log = PageSchema(url='/TeenStudy/log', label='运行日志', icon='fa fa-bug', schema=page_detail)
