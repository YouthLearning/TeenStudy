from amis import App, PageSchema, TableColumn, \
    CRUD, ActionType, LevelEnum, Card, Tpl, CardsCRUD, Dialog, DisplayModeEnum, Select, Flex
from amis import Html, Page, Form, InputText

logo = Html(html=f'''
<p align="center">
    <a href="https://github.com/ZM25XC/TeenStudy/">
        <img src="https://i.328888.xyz/2023/02/23/xIh5k.png"
         width="256" height="256" alt="TeenStudy">
    </a>
</p>
<h2 align="center">大学习自动提交</h2>
<div align="center">
    <a href="https://github.com/ZM25XC/TeenStudy/" target="_blank">
    Github仓库</a>
    <a href="https://jq.qq.com/?_wv=1027&k=NGFEwXyS" target="_blank">交流群</a>
</div>
<br>
''')
github_logo = Tpl(className='w-full',
                  tpl='<div class="flex justify-between"><div></div><div><a href="https://github.com/ZM25XC/TeenStudy" target="_blank" title="Github 仓库"><i class="fa fa-github fa-2x"></i></a></div></div>')
header = Flex(className='w-full', justify='flex-end', alignItems='flex-end', items=[github_logo])
"""提交记录模板"""
record_table = CRUD(mode='table',
                    title='',
                    syncLocation=False,
                    api='/TeenStudy/api/get_records',
                    interval=12000,
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
                        TableColumn(label='提交状态', name='${status==true?"成功":"失败"}', searchable=True),
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
                    interval=12000,
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
            name="user_id",
            label="超管登录账号",
            description="超管登录账号",
            showCounter=True,
            value="${user_id}",
            trimContents=True,
            maxLength=10,
            required=True,
            clearable=True
        ),
        InputText(
            name="Password",
            label="超管登录密码",
            description="超管登录密码，可不填，默认是admin",
            showCounter=True,
            maxLength=16,
            value="",
            trimContents=True,
            required=False, clearable=True

        ),
        InputText(
            name="time",
            label="token失效时间",
            description="Web访问token失效时间，单位为分钟",
            showCounter=True,
            maxLength=3,
            value="${time}",
            trimContents=True,
            resetValue=30,
            required=True,
            clearable=True
        ),
        InputText(
            name="key",
            label="加密秘钥",
            description="加密秘钥，为64位哈希散列值，用于生成token",
            showCounter=True,
            maxLength=64,
            value="${key}",
            resetValue="d82ffad91168fb324ab6ebc2bed8dacd43f5af8e34ad0d1b75d83a0aff966a06",
            trimContents=True,
            required=True, clearable=True
        ),
        InputText(
            name="algorithm",
            label="加密算法",
            description="生成token的算法",
            value="${algorithm}",
            trimContents=True,
            showCounter=True,
            required=True,
            resetValue="HS256",
            clearable=True
        ),
        InputText(
            name="ip",
            label="公网访问IP",
            value="${ip}",
            description="公网访问IP，用于外网访问",
            showCounter=True,
            trimContents=True,
            resetValue="0.0.0.0",
            required=True,
            clearable=True
        )
    ]
)
"""申请记录模板"""
request_table = CRUD(mode='table',
                     title='',
                     syncLocation=False,
                     api='/TeenStudy/api/get_requests',
                     interval=12000,
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
detail_form = Form(
    title='',
    api='put:/TeenStudy/api/change?user_id=${user_id}',
    submitText='保存修改',
    mode=DisplayModeEnum.horizontal,
    labelAlign='right',
    body=[
        InputText(label='性别', name='gender', value='${gender}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=3, visibleOn="${gender==null?false:true}",
                  description='性别'),
        InputText(label='uid|nid', name='dxx_id', value='${dxx_id}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=24, visibleOn="${dxx_id==null?false:true}",
                  description='大学习认证ID，不清楚请勿改动'),
        InputText(label='手机号', name='mobile', value='${mobile}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=24, visibleOn="${mobile==null?false:true}",
                  description='手机号'),
        InputText(label='团支书ID', name='leader', value='${leader}',
                  showCounter=True, maxLength=10, hiddenOn=True, trimContents=True,
                  clearable=True,
                  description='团支书ID，填写后团支书可操作提交功能，不清楚请勿改动'),
        InputText(label='openid', name='openid', value='${openid}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=64, visibleOn="${openid==null?false:true}",
                  description='微信认证ID，不清楚请勿改动'),
        InputText(label='登录密码', name='Password', value='', type="input-password",
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=16, visibleOn="${password==null?false:true}",
                  description='登录Web UI的密码'),
        InputText(label='学校类型', name='university_type', value='${university_type}',
                  showCounter=True, maxLength=16, required=True, trimContents=True,
                  clearable=True,
                  visibleOn="${university_type==null?false:true}",
                  description='四川地区学校类型，不清楚清无改动'),
        InputText(label='学校ID', name='university_id', value='${university_id}',
                  required=True, trimContents=True, clearable=True,
                  showCounter=True, maxLength=24,
                  visibleOn="${university_id==null?false:true}",
                  description='学校ID，不清楚请勿改动'),
        InputText(label='学校名称', name='university', value='${university}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=20, visibleOn="${university==null?false:true}",
                  description='学校名称'),
        InputText(label='学院ID', name='college_id', value='${college_id}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=24, visibleOn="${college_id==null?false:true}",
                  description='学院ID'),
        InputText(label='学院名称', name='college', value='${college}',
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=24, visibleOn="${college==null?false:true}",
                  description='学院名称'),
        InputText(label='团支部ID', name='organization_id', value='${organization_id}',
                  required=True, trimContents=True, clearable=True,
                  showCounter=True, maxLength=24,
                  visibleOn="${organization_id==null?false:true}",
                  description='团支部ID'),
        InputText(label='团支部名称', name='organization', value='${organization}',
                  required=True, trimContents=True, clearable=True,
                  showCounter=True, maxLength=24,
                  visibleOn="${organization==null?false:true}",
                  description='团支部名称'),
        InputText(label='token', name='token', value='${token}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, visibleOn="${token==null?false:true}",
                  description='提交大学习需要的token'),
        InputText(label='cookie', name='cookie', value='${cookie}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, visibleOn="${cookie==null?false:true}",
                  description='提交大学习需要的cookie')
    ])
detail_button = ActionType.Dialog(label='信息',
                                  size='lg',
                                  icon='fa fa-user-tag',
                                  dialog=Dialog(title='${name}的详细信息', size='lg', body=[detail_form]))
card = Card(
    header=Card.Header(title='$name',
                       subTitle='$user_id',
                       description='$catalogue',
                       avatarText='${area}',
                       avatarTextClassName='overflow-hidden'),
    actions=[detail_button, ActionType.Ajax(
        tooltip='删除',
        label="删除",
        icon='fa fa-trash-can text-danger',
        confirmText='删除该用户',
        api='delete:/TeenStudy/api/delete_member?user_id=${user_id}'
    )],
    toolbar=[
        Tpl(tpl='$name', className='label label-warning', hiddenOn=True),
        Tpl(tpl='$area', className='label label-primary', hiddenOn=True),
    ])
"""成员卡片面板"""
cards_curd = CardsCRUD(mode='cards',
                       title='',
                       syncLocation=False,
                       name="member",
                       fetchFailed="数据初始化！",
                       api='get:/TeenStudy/api/get_members',
                       loadDataOnce=True,
                       source='${rows | filter:user_id:keywords_user_id | filter:name:keywords_name|filter:area:keywords_area|filter:university:keywords_university|filter:college:keywords_college|filter:organization:keywords_organization}',
                       filter={
                           'body': [
                               InputText(name='keywords_user_id', label='用户ID',
                                         trimContents=True, clearable=True,
                                         submitOnChange=True),
                               InputText(name='keywords_name', label='用户姓名',
                                         trimContents=True, clearable=True,
                                         submitOnChange=True),
                               InputText(name='keywords_area', label='地区',
                                         trimContents=True, clearable=True,
                                         submitOnChange=True),
                               InputText(name='keywords_university', label='学校',
                                         trimContents=True, clearable=True,
                                         submitOnChange=True),
                               InputText(name='keywords_college', label='学院',
                                         trimContents=True, clearable=True,
                                         submitOnChange=True),
                               InputText(name='keywords_organization', label='团支部',
                                         trimContents=True, clearable=True,
                                         submitOnChange=True),
                           ]
                       },
                       perPage=16,
                       autoJumpToTopOnPagerChange=True,
                       placeholder='暂无大学习用户',
                       footerToolbar=['switch-per-page', 'pagination'],
                       columnsCount=4,
                       card=card)
"""推送群聊模板"""
push_table = CRUD(mode='table',
                  title='',
                  syncLocation=False,
                  api='/TeenStudy/api/get_push_list',
                  interval=12000,
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
                      TableColumn(label='提交状态', name='${status==true?"开启":"关闭"}', searchable=True, ),
                      TableColumn(type='tpl', tpl='${time|date:YYYY-MM-DD HH\\:mm\\:ss}',
                                  label='添加时间',
                                  name='time', sortable=True)
                  ],
                  bulkActions=[
                      ActionType.Ajax(label='批量删除',
                                      level=LevelEnum.warning,
                                      confirmText="确定要批量删除？",
                                      api="delete:/TeenStudy/api/delete_push?ids=${ids|raw}")])
page_detail = Page(title='', body=[logo, cards_curd])
admin_page = PageSchema(url='/admin', label='首页', icon='fa fa-home', isDefaultPage=True, schema=page_detail)
admin_app = App(brandName='TeenStudy',
                logo='https://i.328888.xyz/2023/02/23/xIh5k.png',
                header=header,
                pages=[{
                    'children': [
                        admin_page,
                        PageSchema(url="/notice", label='推送列表', icon='fa fa-bell',
                                   schema=Page(title='', body=[push_table])),
                        PageSchema(url="/request", label='申请记录', icon='fa fa-circle-info',
                                   schema=Page(title='', body=[request_table])),
                        PageSchema(url="/answer", label='大学习列表', icon='fa fa-book-open',
                                   schema=Page(title='', body=[answer_table])),
                        PageSchema(url="/records", label='提交记录', icon='fa fa-code-commit',
                                   schema=Page(title='', body=[record_table])),
                        PageSchema(url="/setting", label='配置', icon='fa fa-gear',
                                   schema=Page(title='', body=[setting_table])),
                    ]}],
                footer=Html(
                    html=f'<div class="p-2 text-center bg-blue-100">Copyright © 2022 - 2023 <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy" target="_blank" class="link-secondary">TeenStudy</a> X<a target="_blank" href="https://github.com/baidu/amis" class="link-secondary" rel="noopener"> amis v2.2.0</a></div>'))
