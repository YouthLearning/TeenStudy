from amis import App, PageSchema, TableColumn, CRUD, ActionType, LevelEnum
from amis import Html, Page, Form, InputText, Switch, InputTime, InputNumber
from amis import Tpl, Dialog, DisplayModeEnum, Select, Flex, Service, Property

from .addArea import areaPage
from .log import page_log

logo = Html(html=f'''
<p align="center">
    <a href="https://github.com/YouthLearning/TeenStudy/">
        <img src="https://img1.imgtp.com/2023/10/06/NChUNeiA.png"
         width="256" height="256" alt="TeenStudy">
    </a>
</p>
<h2 align="center">大学习自动提交</h2>
<div align="center">
    <a href="https://github.com/YouthLearning/TeenStudy/" target="_blank">
    Github仓库</a>
    <a href="https://jq.qq.com/?_wv=1027&k=NGFEwXyS" target="_blank">QQ反馈群</a>
    <a href="http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=2PQucjirnkHyPjoS1Pkr-ai2aPGToBKm" target="_blank">QQ体验群</a>
</div>
<br>
''')
github_logo = Tpl(className='w-full',
                  tpl='<div class="flex justify-between"><div></div><div><a href="https://github.com/YouthLearning/TeenStudy" target="_blank" title="Github 仓库"><i class="fa fa-github fa-2x"></i></a></div></div>')
header = Flex(className='w-full', justify='flex-end', alignItems='flex-end', items=[github_logo,
                                                                                    {
                                                                                        "type": "button",
                                                                                        "label": "退出",
                                                                                        "onEvent": {
                                                                                            "click": {
                                                                                                "actions": [
                                                                                                    {
                                                                                                        "actionType": "confirmDialog",
                                                                                                        "args": {
                                                                                                            "title": "操作确认",
                                                                                                            "msg": "是否退出系统？"
                                                                                                        }},

                                                                                                    {
                                                                                                        "actionType": "custom",
                                                                                                        "script": "window.location.href = '/TeenStudy/login';window.localStorage.clear();window.sessionStorage.clear();\n //event.stopPropagation();"
                                                                                                    }

                                                                                                ]
                                                                                            },
                                                                                        }}
                                                                                    ])
"""机器人状态面板"""
status = Service(
    api='/TeenStudy/api/status',
    interval=60000,
    body=[Property(
        title='机器人信息',
        column=2,
        items=[
            Property.Item(
                label='Bot昵称',
                content='${nickname}'
            ),
            Property.Item(
                label='Bot qq号',
                content='${bot_id}'
            ),
            Property.Item(
                label='Bot好友数量',
                content='${friend_count}'
            ),
            Property.Item(
                label='Bot群聊数量',
                content='${group_count}'
            ),
            Property.Item(
                label='Bot启动时间',
                content='${start_time}'
            ),
            Property.Item(
                label='系统启动时间',
                content='${system_start_time}'
            ),
            Property.Item(
                label='通知群数量',
                content='${notice_count}'
            ),
            Property.Item(
                label='用户数量',
                content='${user_count}'
            ),
            Property.Item(
                label='支持地区数量',
                content='${area_count}'
            ), Property.Item(
                label='最新一期大学习',
                content='${catalogue}'
            ), Property.Item(
                label='公网访问IP',
                content='${ip}'
            ),
            Property.Item(
                label='CPU占用率',
                content='${cpu_percent}'
            ),
            Property.Item(
                label='RAM占用率',
                content='${ram_percent}'
            ),
            Property.Item(
                label='SWAP占用率',
                content='${swap_percent}',
            ),
        ]
    )]
)
"""提交记录模板"""
record_table = CRUD(mode='table',
                    title='',
                    syncLocation=False,
                    api='/TeenStudy/api/get_records',
                    interval=60000,
                    type='crud',
                    headerToolbar=[ActionType.Ajax(label='删除所有提交记录',
                                                   level=LevelEnum.warning,
                                                   confirmText='确定要删除所有提交记录吗？',
                                                   api='delete:/TeenStudy/api/delete_all?type=records'),
                                   "bulkActions", "reload"],
                    itemActions=[
                        ActionType.Ajax(tooltip='删除',
                                        icon='fa fa-times text-danger',
                                        confirmText='删除该条提交记录',
                                        api='delete:/TeenStudy/api/delete_record?id=${id}')
                    ],
                    footable=True,
                    columns=[
                        TableColumn(label='用户ID', name='user_id', searchable=True),
                        TableColumn(label='姓名', name='name', searchable=True),
                        TableColumn(label='提交地区', name='area', searchable=True),
                        TableColumn(label='学校名称', name='university', searchable=True),
                        TableColumn(label='学院名称', name='college', searchable=True),
                        TableColumn(label='团支部', name='organization', searchable=True),
                        TableColumn(label='提交期数', name='catalogue', searchable=True),
                        TableColumn(tppe="tpl", label='提交状态', tpl='${status===true?"成功":"失败"}', name="status",
                                    searchable=True),
                        TableColumn(type='tpl', tpl='${time|date:YYYY-MM-DD HH\\:mm\\:ss}',
                                    label='提交时间',
                                    name='time', sortable=True)
                    ],
                    bulkActions=[
                        ActionType.Ajax(label='批量删除',
                                        level=LevelEnum.warning,
                                        confirmText="确定要批量删除？",
                                        api="delete:/TeenStudy/api/delete_records?ids=${ids|raw}")])
answer_table = CRUD(mode='table',
                    title='',
                    syncLocation=False,
                    api='/TeenStudy/api/get_answers',
                    interval=60000,
                    type='crud',
                    headerToolbar=[ActionType.Ajax(label='删除青年大学习期数',
                                                   level=LevelEnum.warning,
                                                   confirmText='确定要删除青年大学习期数吗？',
                                                   api='delete:/TeenStudy/api/delete_all?type=answers'),
                                   "bulkActions", "reload"],
                    itemActions=[
                        ActionType.Ajax(tooltip='删除',
                                        icon='fa fa-times text-danger',
                                        confirmText='删除该期青年大学习',
                                        api='delete:/TeenStudy/api/delete_answer?id=${id}')
                    ],
                    footable=True,
                    columns=[
                        TableColumn(label='数据库ID', name='id'),
                        TableColumn(label='大学习ID', name='code'),
                        TableColumn(label='大学习期数', name='catalogue', searchable=True),
                        TableColumn(type='tpl', tpl='${url|truncate:20}', label='官方网址',
                                    name='url',
                                    popOver={'mode': 'dialog', 'title': '完整网址',
                                             'className': 'break-all',
                                             'body': {'type': 'tpl',
                                                      'tpl': '${url}'}}, copyable=True),
                        TableColumn(type='tpl', tpl='${end_url|truncate:20}', label='完成截图网址',
                                    name='end_url',
                                    popOver={'mode': 'dialog', 'title': '完整网址',
                                             'className': 'break-all',
                                             'body': {'type': 'tpl',
                                                      'tpl': '${end_url}'}}, copyable=True),
                        TableColumn(type='tpl', tpl='${answer|truncate:20}', label='答案',
                                    name='answer',
                                    popOver={'mode': 'dialog', 'title': '完整答案',
                                             'className': 'break-all',
                                             'body': {'type': 'tpl',
                                                      'tpl': '${answer}'}}),
                        TableColumn(type='tpl', tpl='${time|date:YYYY-MM-DD HH\\:mm\\:ss}',
                                    label='更新时间',
                                    name='time', sortable=True)
                    ],
                    bulkActions=[
                        ActionType.Ajax(label='批量删除',
                                        level=LevelEnum.warning,
                                        confirmText="确定要批量删除？",
                                        api="delete:/TeenStudy/api/delete_answers?ids=${ids|raw}")])

"""Web端配置表"""
setting_table = Form(
    title="Web端配置",
    submitText="保存",
    api="put:/TeenStudy/api/change_settings",
    initApi="get:/TeenStudy/api/get_settings",
    body=[
        InputText(
            name="SUPERUSER",
            label="超管登录账号",
            description="超管登录账号",
            showCounter=True,
            value="${SUPERUSER}",
            trimContents=True,
            maxLength=10,
            required=True,
            clearable=True
        ),
        InputText(
            name="password",
            label="超管登录密码",
            description="超管登录密码，可不填，默认是admin",
            showCounter=True,
            maxLength=16,
            value="",
            trimContents=True,
            required=False, clearable=True

        ),
        InputText(
            name="TOKEN_TIME",
            label="token失效时间",
            description="Web访问token失效时间，单位为分钟",
            showCounter=True,
            maxLength=3,
            value="${TOKEN_TIME}",
            trimContents=True,
            resetValue=30,
            required=True,
            clearable=True
        ),
        InputText(
            name="KEY",
            label="加密秘钥",
            description="加密秘钥，为64位哈希散列值，用于生成token",
            showCounter=True,
            maxLength=64,
            value="${KEY}",
            resetValue="d82ffad91168fb324ab6ebc2bed8dacd43f5af8e34ad0d1b75d83a0aff966a06",
            trimContents=True,
            required=True, clearable=True
        ),
        InputText(
            name="ALGORITHM",
            label="加密算法",
            description="生成token的算法",
            value="${ALGORITHM}",
            trimContents=True,
            showCounter=True,
            required=True,
            resetValue="HS256",
            clearable=True
        ),
        InputText(
            name="DXX_IP",
            label="公网访问IP",
            value="${DXX_IP}",
            description="公网访问IP，用于外网访问",
            showCounter=True,
            trimContents=True,
            resetValue="0.0.0.0",
            required=True,
            clearable=True
        ),
        InputNumber(
            name="DXX_PORT",
            displayMode="enhance",
            label="公网访问端口",
            value="${DXX_PORT}",
            min=0,
            max=65535,
            description="公网访问端口，用于外网访问，不配置域名和反向代理请勿修改",
            showCounter=True,
            trimContents=True,
            resetValue=8080,
            required=True,
            clearable=True
        ),
        Switch(
            name="URL_STATUS",
            label="二维码转链接开关",
            value="${URL_STATUS}",
            onText='开启',
            offText='关闭',
            required=True,
        ),
        Switch(
            name="POKE_SUBMIT",
            label="戳一戳提交大学习开关",
            value="${POKE_SUBMIT}",
            onText='开启',
            offText='关闭',
            required=True,
        ),
        Switch(
            name="DXX_REMIND",
            label="大学习提醒开关",
            value="${DXX_REMIND}",
            onText='开启',
            offText='关闭',
            required=True,
        ),
        InputTime(
            name="remind",
            label="提醒时间",
            type="input-time",
            required=True,
            value="${remind}",
        ),
        Switch(
            name="AUTO_SUBMIT",
            label="大学习自动提交开关",
            value="${AUTO_SUBMIT}",
            onText='开启',
            offText='关闭',
            required=True,
        ),
        InputTime(
            name="auto",
            label="自动提交时间",
            type="input-time",
            required=True,
            value="${auto}",
        ),
    ]
)
"""申请记录模板"""
request_table = CRUD(mode='table',
                     title='',
                     syncLocation=False,
                     api='/TeenStudy/api/get_requests',
                     interval=60000,
                     type='crud',
                     headerToolbar=[ActionType.Ajax(label='删除所有申请记录',
                                                    level=LevelEnum.warning,
                                                    confirmText='确定要删除所有申请记录吗？',
                                                    api='delete:/TeenStudy/api/delete_all?type=requests'),
                                    "bulkActions", "reload"],
                     itemActions=[
                         ActionType.Ajax(tooltip='删除',
                                         icon='fa fa-times text-danger',
                                         confirmText='删除该条申请记录',
                                         api='delete:/TeenStudy/api/delete_request?id=${id}')
                     ],
                     footable=True,
                     columns=[
                         TableColumn(label='申请ID', name='user_id', searchable=True),
                         TableColumn(label='申请群号', name='group_id', searchable=True),
                         TableColumn(label='申请地区', name='area', searchable=True),
                         TableColumn(label='申请状态', name='status', searchable=True),
                         TableColumn(type='tpl', tpl='${time|date:YYYY-MM-DD HH\\:mm\\:ss}',
                                     label='申请时间',
                                     name='time', sortable=True)
                     ],
                     bulkActions=[
                         ActionType.Ajax(label='批量删除',
                                         level=LevelEnum.warning,
                                         confirmText="确定要批量删除？",
                                         api="delete:/TeenStudy/api/delete_requests?ids=${ids|raw}")])

"""推送群聊模板"""
push_table = CRUD(mode='table',
                  title='',
                  syncLocation=False,
                  api='/TeenStudy/api/get_push_list',
                  type='crud',
                  headerToolbar=[ActionType.Ajax(label='删除所有推送群聊',
                                                 level=LevelEnum.warning,
                                                 confirmText='确定要删除所有推送群聊吗？',
                                                 api='delete:/TeenStudy/api/delete_all?type=push_list'),
                                 "bulkActions", "reload", ActionType.Dialog(
                          label='添加推送群聊',
                          level=LevelEnum.info,
                          icon='fa fa-plus',
                          dialog=Dialog(title='添加推送群聊',
                                        size='lg',
                                        body=[
                                            Form(title='',
                                                 api='post:/TeenStudy/api/add_push',
                                                 submitText='添加',
                                                 mode=DisplayModeEnum.horizontal,
                                                 labelAlign='right',
                                                 body=[Select(
                                                     label="群聊",
                                                     name="groups",
                                                     description="需要推送的群组",
                                                     checkAll=True,
                                                     source="get:/TeenStudy/api/get_group_list",
                                                     value='',
                                                     multiple=True,
                                                     required=True,
                                                     searchable=True,
                                                     joinValues=False,
                                                     extractValue=True,
                                                     statistics=True,
                                                 )
                                                 ])])
                      )],
                  itemActions=[
                      ActionType.Ajax(tooltip='删除',
                                      icon='fa fa-times text-danger',
                                      confirmText='删除该推送群聊吗',
                                      api='delete:/TeenStudy/api/delete_push?id=${id}')
                  ],
                  footable=True,
                  columns=[
                      TableColumn(label='数据库ID', name='id'),
                      TableColumn(label='机器人ID', name='self_id', searchable=True, ),
                      TableColumn(label='通知群号', name='group_id'),
                      TableColumn(label='添加人员', name='user_id', searchable=True, ),
                      TableColumn(type="tpl", label='提交状态', tpl='${status==true?"开启":"关闭"}', name="status",
                                  searchable=True, ),
                      TableColumn(type='tpl', tpl='${time|date:YYYY-MM-DD HH\\:mm\\:ss}',
                                  label='添加时间',
                                  name='time', sortable=True)
                  ],
                  bulkActions=[
                      ActionType.Ajax(label='批量删除',
                                      level=LevelEnum.warning,
                                      confirmText="确定要批量删除？",
                                      api="delete:/TeenStudy/api/delete_push?ids=${ids|raw}")])
page_detail = Page(title='', body=[logo, status])
admin_page = PageSchema(url='/TeenStudy/admin', label='首页', icon='fa fa-home', isDefaultPage=True, schema=page_detail)
"""成员列表页"""

admin_app = App(brandName='TeenStudy',
                logo='https://img1.imgtp.com/2023/10/06/NChUNeiA.png',
                header=header,
                pages=[{
                    'children': [
                        admin_page,
                        PageSchema(icon='fa fa-circle-user', label='成员管理',
                                   children=areaPage),
                        PageSchema(url="/TeenStudy/notice", label='推送列表', icon='fa fa-bell',
                                   schema=Page(title='', body=[push_table])),
                        PageSchema(url="/TeenStudy/request", label='申请记录', icon='fa fa-circle-info',
                                   schema=Page(title='', body=[request_table])),
                        PageSchema(url="/TeenStudy/answer", label='大学习列表', icon='fa fa-book-open',
                                   schema=Page(title='', body=[answer_table])),
                        PageSchema(url="/TeenStudy/records", label='提交记录', icon='fa fa-code-commit',
                                   schema=Page(title='', body=[record_table])),
                        PageSchema(url="/TeenStudy/setting", label='配置', icon='fa fa-gear',
                                   schema=Page(title='', body=[setting_table])),
                        page_log
                    ]}],
                footer=Html(
                    html=f'<div class="p-2 text-center bg-blue-100">Copyright © 2022 - 2023 <a href="https://github.com/YouthLearning/TeenStudy" target="_blank" class="link-secondary">TeenStudy v0.2.4</a> X<a target="_blank" href="https://github.com/baidu/amis" class="link-secondary" rel="noopener"> amis v3.4.2</a></div>'))
