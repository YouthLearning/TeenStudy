from amis import App, PageSchema, TableColumn, \
    CRUD, ActionType, LevelEnum, Card, Tpl, CardsCRUD, Dialog, DisplayModeEnum, Select, Flex, Service, Alert, Property
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
        Select(
            label="通知群聊",
            name="group_id",
            description="大学习提醒群号",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='${group_id}',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        InputText(label='性别', name='gender', value='${gender}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=3, visibleOn="${gender==null?false:true}",
                  description='性别'),
        InputText(label='uid|nid', name='dxx_id', value='${dxx_id}', required=True,
                  trimContents=True, clearable=True,
                  showCounter=True, maxLength=24, visibleOn="${dxx_id==null?false:true}",
                  description='大学习认证ID，不清楚请勿改动'),
        InputText(label='手机号|学号', name='mobile', value='${mobile}', required=False,
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
        InputText(label='学院ID', name='college_id', value='${college_id}', required=False,
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
                  required=False, trimContents=True, clearable=True,
                  showCounter=True, maxLength=36,
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
                                  tooltip='查看|修改信息',
                                  size='lg',
                                  icon='fa fa-user-tag text-primary',
                                  dialog=Dialog(title='${name}的详细信息', size='lg', body=[detail_form]))
card = Card(
    header=Card.Header(title='$name',
                       subTitle='$user_id',
                       description='$catalogue',
                       avatarText='${area}',
                       avatarTextClassName='overflow-hidden'),
    actions=[detail_button, ActionType.Ajax(
        label="提交",
        tooltip='提交大学习',
        icon='fa fa-check text-success',
        confirmText='是否提交最新一期青年大学习？',
        api='get:/TeenStudy/api/commit?user_id=${user_id}&area=${area}'
    ), ActionType.Ajax(
        tooltip='删除',
        label="删除",
        icon='fa fa-trash-can text-danger',
        confirmText='删除该用户',
        api='delete:/TeenStudy/api/delete_member?user_id=${user_id}'
    ), ],
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

"""湖北添加成员面板"""
hubei_table = Form(
    title="添加青春湖北用户",
    submitText="添加",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/add",
    resetAfterSubmit=True,
    body=[
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="湖北",
            disabled=True
        ),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="姓名",
            description="对应青春湖北个人信息页 您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="用户编号",
            description="对应青春湖北个人信息页 用户编号",
            name="dxx_id",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=9
        ),
        InputText(
            label="学校",
            description="对应青春湖北填写信息页 高校",
            name="university",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学院",
            description="对应青春湖北填写信息页 院系",
            name="college",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部",
            description="对应青春湖北填写信息页 选择组织",
            name="organization",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
        )

    ]
)
"""江西添加成员面板"""
jiangxi_table = Form(
    title="添加江西共青团用户",
    submitText="添加",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/add",
    resetAfterSubmit=True,
    body=[
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="江西",
            disabled=True
        ),
        InputText(
            label="用户编号",
            description="团组织ID，无需填写",
            name="dxx_id",
            inline=False,
            required=True,
            value="${organization}",
            disabled=True
        ),
        Service(
            interval=3000,
            size="lg",
            body=[
                Select(
                    type="select",
                    label="学校名称",
                    name="university",
                    searchable=True,
                    required=True,
                    options=[{'label': '南昌大学', 'value': '南昌大学'},
                             {'label': '江西师范大学', 'value': '江西师范大学'},
                             {'label': '江西农业大学', 'value': '江西农业大学'},
                             {'label': '江西财经大学', 'value': '江西财经大学'},
                             {'label': '华东交通大学', 'value': '华东交通大学'},
                             {'label': '东华理工大学', 'value': '东华理工大学'},
                             {'label': '江西理工大学', 'value': '江西理工大学'},
                             {'label': '南昌航空大学', 'value': '南昌航空大学'},
                             {'label': '井冈山大学', 'value': '井冈山大学'},
                             {'label': '江西科技师范大学', 'value': '江西科技师范大学'},
                             {'label': '江西中医药大学', 'value': '江西中医药大学'},
                             {'label': '景德镇陶瓷大学', 'value': '景德镇陶瓷大学'},
                             {'label': '赣南师范大学', 'value': '赣南师范大学'},
                             {'label': '赣南医学院', 'value': '赣南医学院'},
                             {'label': '南昌工程学院', 'value': '南昌工程学院'},
                             {'label': '江西科技学院', 'value': '江西科技学院'},
                             {'label': '南昌理工学院', 'value': '南昌理工学院'},
                             {'label': '江西应用科技学院', 'value': '江西应用科技学院'},
                             {'label': '南昌师范学院', 'value': '南昌师范学院'},
                             {'label': '宜春学院', 'value': '宜春学院'},
                             {'label': '上饶师范学院', 'value': '上饶师范学院'},
                             {'label': '九江学院', 'value': '九江学院'},
                             {'label': '南昌大学科学技术学院', 'value': '南昌大学科学技术学院'},
                             {'label': '江西开放大学人民武装学院', 'value': '江西开放大学人民武装学院'},
                             {'label': '南昌大学共青学院', 'value': '南昌大学共青学院'},
                             {'label': '江西师范大学科学技术学院', 'value': '江西师范大学科学技术学院'},
                             {'label': '江西农业大学南昌商学院', 'value': '江西农业大学南昌商学院'},
                             {'label': '江西财经大学现代经济管理学院', 'value': '江西财经大学现代经济管理学院'},
                             {'label': '南昌交通学院', 'value': '南昌交通学院'},
                             {'label': '赣南科技', 'value': '赣南科技'},
                             {'label': '赣东学院', 'value': '赣东学院'},
                             {'label': '南昌航空大学科技学院', 'value': '南昌航空大学科技学院'},
                             {'label': '景德镇陶瓷大学科技艺术学院', 'value': '景德镇陶瓷大学科技艺术学院'},
                             {'label': '江西中医药大学科技学院', 'value': '江西中医药大学科技学院'},
                             {'label': '赣南师范大学科技学院', 'value': '赣南师范大学科技学院'},
                             {'label': '江西警察学院', 'value': '江西警察学院'},
                             {'label': '新余学院', 'value': '新余学院'},
                             {'label': '南昌工学院', 'value': '南昌工学院'},
                             {'label': '江西服装学院', 'value': '江西服装学院'},
                             {'label': '景德镇学院', 'value': '景德镇学院'},
                             {'label': '萍乡学院', 'value': '萍乡学院'},
                             {'label': '江西工程学院', 'value': '江西工程学院'},
                             {'label': '豫章师范学院', 'value': '豫章师范学院'},
                             {'label': '南昌职业大学', 'value': '南昌职业大学'},
                             {'label': '江西软件职业技术大学', 'value': '江西软件职业技术大学'},
                             {'label': '景德镇艺术职业大学', 'value': '景德镇艺术职业大学'},
                             {'label': '南昌医', 'value': '南昌医'},
                             {'label': '南昌应用技术师范学院', 'value': '南昌应用技术师范学院'},
                             {'label': '江西中医药高等专科学校', 'value': '江西中医药高等专科学校'},
                             {'label': '九江职业大学', 'value': '九江职业大学'},
                             {'label': '九江职业技术学院', 'value': '九江职业技术学院'},
                             {'label': '江西工业职业技术学院', 'value': '江西工业职业技术学院'},
                             {'label': '江西电力职业技术学院', 'value': '江西电力职业技术学院'},
                             {'label': '江西旅游商贸职业学院', 'value': '江西旅游商贸职业学院'},
                             {'label': '江西机电职业技术学院', 'value': '江西机电职业技术学院'},
                             {'label': '江西陶瓷工艺美术职业技术学院', 'value': '江西陶瓷工艺美术职业技术学院'},
                             {'label': '江西环境工程职业学院', 'value': '江西环境工程职业学院'},
                             {'label': '江西信息应用职业技术学院', 'value': '江西信息应用职业技术学院'},
                             {'label': '江西工业工程职业技术学院', 'value': '江西工业工程职业技术学院'},
                             {'label': '江西交通职业技术学院', 'value': '江西交通职业技术学院'},
                             {'label': '江西艺术职业学院', 'value': '江西艺术职业学院'},
                             {'label': '江西财经职业学院', 'value': '江西财经职业学院'},
                             {'label': '江西司法警官职业学院', 'value': '江西司法警官职业学院'},
                             {'label': '江西应用技术职业学院', 'value': '江西应用技术职业学院'},
                             {'label': '江西师范高等专科学校', 'value': '江西师范高等专科学校'},
                             {'label': '江西现代职业技术学院', 'value': '江西现代职业技术学院'},
                             {'label': '江西外语外贸职业学院', 'value': '江西外语外贸职业学院'},
                             {'label': '江西工业贸易职业技术学院', 'value': '江西工业贸易职业技术学院'},
                             {'label': '江西应用工程职业学院', 'value': '江西应用工程职业学院'},
                             {'label': '江西建设职业技术学院', 'value': '江西建设职业技术学院'},
                             {'label': '宜春职业技术学院', 'value': '宜春职业技术学院'},
                             {'label': '抚州职业技术学院', 'value': '抚州职业技术学院'},
                             {'label': '江西生物科技职业学院', 'value': '江西生物科技职业学院'},
                             {'label': '江西卫生职业学院', 'value': '江西卫生职业学院'},
                             {'label': '江西青年职业学院', 'value': '江西青年职业学院'},
                             {'label': '上饶职业技术学院', 'value': '上饶职业技术学院'},
                             {'label': '江西农业工程职业学院', 'value': '江西农业工程职业学院'},
                             {'label': '江西科技职业学院', 'value': '江西科技职业学院'},
                             {'label': '江西航空职业技术学院', 'value': '江西航空职业技术学院'},
                             {'label': '赣西科技职业学院', 'value': '赣西科技职业学院'},
                             {'label': '江西制造职业技术学院', 'value': '江西制造职业技术学院'},
                             {'label': '江西工程职业学院', 'value': '江西工程职业学院'},
                             {'label': '江西经济管理干部学院', 'value': '江西经济管理干部学院'},
                             {'label': '江西泰豪动漫职业学院', 'value': '江西泰豪动漫职业学院'},
                             {'label': '江西枫林涉外经贸职业学院', 'value': '江西枫林涉外经贸职业学院'},
                             {'label': '江西新能源科技职业学院', 'value': '江西新能源科技职业学院'},
                             {'label': '江西传媒职业学院', 'value': '江西传媒职业学院'},
                             {'label': '江西冶金职业技术学院', 'value': '江西冶金职业技术学院'},
                             {'label': '江西工商职业技术学院', 'value': '江西工商职业技术学院'},
                             {'label': '共青科技职业学院', 'value': '共青科技职业学院'},
                             {'label': '景德镇陶瓷职业技术学院', 'value': '景德镇陶瓷职业技术学院'},
                             {'label': '江西医学高等专科学校', 'value': '江西医学高等专科学校'},
                             {'label': '赣州师范高等专科学校', 'value': '赣州师范高等专科学校'},
                             {'label': '江西水利职业学院', 'value': '江西水利职业学院'},
                             {'label': '吉安职业技术学院', 'value': '吉安职业技术学院'},
                             {'label': '江西洪州职业学院', 'value': '江西洪州职业学院'},
                             {'label': '南昌影视传播职业学院', 'value': '南昌影视传播职业学院'},
                             {'label': '赣南卫生健康职业学院', 'value': '赣南卫生健康职业学院'},
                             {'label': '抚州幼儿师范高等专科学校', 'value': '抚州幼儿师范高等专科学校'},
                             {'label': '上饶幼儿师范高等专科学校', 'value': '上饶幼儿师范高等专科学校'},
                             {'label': '宜春幼儿师范高等专科学校', 'value': '宜春幼儿师范高等专科学校'},
                             {'label': '萍乡卫生职业学院', 'value': '萍乡卫生职业学院'},
                             {'label': '江西婺源茶业职业学院', 'value': '江西婺源茶业职业学院'},
                             {'label': '赣州职业技术学院', 'value': '赣州职业技术学院'},
                             {'label': '九江理工职业学院', 'value': '九江理工职业学院'},
                             {'label': '和君职业学院', 'value': '和君职业学院'}]

                ), Select(
                    type="select",
                    label="学院名称",
                    name="college",
                    searchable=True,
                    required=True,
                    source="get:/TeenStudy/api/organization?type=jx&university=${university}&college="
                ),
                Select(
                    type="select",
                    label="团支部",
                    description="团支部名称，对应江西共青团个人修改信息页 班级/团支部",
                    name="organization",
                    searchable=True,
                    required=True,
                    source="get:/TeenStudy/api/organization?type=jx&university=${university}&college=${college}"
                )]),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="手机号/学号",
            description="对应江西共青团个人修改信息页 手机号/学号，空着不用填",
            name="mobile",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=11
        ),
        InputText(
            label="姓名",
            description="对应江西共青团个人修改信息页 真实姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        )

    ]
)
"""江苏添加成员面板"""
jiangsu_table = Form(
    title="添加江苏共青团用户",
    submitText="添加",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/jiangsu/add",
    resetAfterSubmit=True,
    body=[
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="江苏",
            disabled=True
        ),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="姓名",
            description="对应江苏共青团个人信息页 您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="用户编号",
            description="对应江苏共青团个人信息页 用户编号",
            name="dxx_id",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=9
        ),
        InputText(
            label="cookie",
            description="自行抓包获取，结构为：laravel_session=NsldMlIPeBXV5*********6lYDCOpeNANnlvf",
            name="cookie",
            inline=False,
            required=True,
            value="",
            clearable=True,
        )

    ]
)
"""安徽添加成员面板"""
anhui_table = Form(
    title="添加安徽共青团用户",
    submitText="添加",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/anhui/add",
    resetAfterSubmit=True,
    body=[
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="安徽",
            disabled=True
        ),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="token",
            description="对应抓包内容中的token",
            name="token",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=64
        ),
        InputText(
            label="姓名",
            description="对应抓包内容中的username",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="性别",
            description="对应抓包内容中的gender",
            name="gender",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=9
        ),
        InputText(
            label="手机号",
            description="对应抓包内容中的mobile",
            name="mobile",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学校类型",
            description="对应抓包内容中的level1",
            name="university_type",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学校",
            description="对应抓包内容中的level2",
            name="university",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学院",
            description="对应抓包内容中的level3",
            name="college",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部",
            description="对应抓包内容中的level4",
            name="organization",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
        ), InputText(
            label="团支部ID",
            description="对应抓包内容中的level5",
            name="organization_id",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
        )

    ]
)
"""河南添加成员面板"""
henan_table = Form(
    title="添加河南共青团用户",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/henan/add",
    submitText="添加",
    resetAfterSubmit=True,
    body=[
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="河南",
            disabled=True
        ),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="姓名",
            description="对应河南共青团个人信息页 您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="cookie",
            description="自行抓包获取，结构为：stw=xxxxxx-xxxx-xxxxx-xxxx-e52xxxx2c3b45",
            name="cookie",
            inline=False,
            required=True,
            value="",
            clearable=True,
        )

    ]
)
"""四川添加成员面板"""
sichuan_table = Form(
    title="添加天府新青年用户",
    submitText="添加",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/sichuan/add",
    resetAfterSubmit=True,
    body=[
        Alert(level=LevelEnum.info,
              className='white-space-pre-wrap',
              body=(
                  "该地区需要自行抓包填入\ntoken值在https://dxx.scyol.com/api/wechat/login 响应里\n其余信息在 https://dxx.scyol.com/api/student/showStudyStageOrg?id=xxxxxx&stageId=xx 响应里")),
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="四川",
            disabled=True
        ),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="姓名",
            description="对应抓包内容 name",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="token",
            description="自行抓包获取，在：https://dxx.scyol.com/api/wechat/login 链接的响应内容里",
            name="token",
            inline=False,
            required=True,
            value="",
            clearable=True,
        ),
        InputText(
            label="手机号",
            description="自行抓包获取，对应tel",
            name="mobile",
            inline=False,
            required=True,
            value="",
            clearable=True,
        ),
        InputText(
            label="整体组织ID",
            description="自行抓包获取，对应org",
            name="org",
            inline=False,
            required=True,
            value="",
            clearable=True,
        ),
        InputText(
            label="组织ID",
            description="自行抓包获取，对应lastOrg",
            name="lastOrg",
            inline=False,
            required=True,
            value="",
            clearable=True,
        ),
        InputText(
            label="团支部名称",
            description="自行抓包获取，对应 orgName",
            name="orgName",
            inline=False,
            required=True,
            value="",
            clearable=True,
        ), InputText(
            label="组织全称",
            description="自行抓包获取，对应allOrgName",
            name="allOrgName",
            inline=False,
            required=True,
            value="",
            clearable=True,
        )

    ]
)
"""山东添加成员面板"""
shandong_table = Form(
    title="添加青春山东用户",
    sunmitText="添加",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/shandong/add",
    resetAfterSubmit=True,
    body=[
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="山东",
            disabled=True
        ),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="姓名",
            description="对应青春山东个人信息页 您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="cookie",
            description="自行抓包获取，结构为：JSESSIONID=1873FXXXXXXXX5DFCBF1CC13703",
            name="cookie",
            inline=False,
            required=True,
            value="",
            clearable=True,
        ),
        InputText(
            label="openid",
            description="自行抓包获取，结构为：ohz9xxxxxxxxxxxxlF0Io0uCnM",
            name="openid",
            inline=False,
            required=True,
            value="",
            clearable=True,
        )

    ]
)
"""重庆添加成员面板"""
chongqing_table = Form(
    title="添加重庆共青团用户",
    sunmitText="添加",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/chongqing/add",
    resetAfterSubmit=True,
    body=[
        Select(
            label="群聊",
            name="group_id",
            description="需要添加的群组",
            checkAll=False,
            source="get:/TeenStudy/api/get_group_list",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
        ),
        Select(
            label="用户ID",
            name="user_id",
            description="需要添加的用户ID",
            checkAll=False,
            source="get:/TeenStudy/api/get_member_list?group_id=${group_id}",
            value='',
            multiple=False,
            required=True,
            searchable=True,
            joinValues=False,
            extractValue=True,
            statistics=True,
            hiddenOn="${group_id==''?true:false}"
        ),
        InputText(
            label="地区",
            description="所处省份",
            name="area",
            value="重庆",
            disabled=True
        ),
        InputText(
            label="登录密码",
            type='input-password',
            description="可不填，默认为用户ID",
            name="password",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=16
        ),
        InputText(
            label="姓名",
            description="对应重庆共青团个人信息页 您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="openid",
            description="自行抓包获取，结构为: ohz9xxxxxxxxxxxxlF0Io0uCnM",
            name="openid",
            inline=False,
            required=True,
            value="",
            clearable=True,
        )

    ]
)
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
page_detail = Page(title='', body=[logo, status])
admin_page = PageSchema(url='/admin', label='首页', icon='fa fa-home', isDefaultPage=True, schema=page_detail)
"""成员列表页"""
list_page = PageSchema(url='/list', icon='fa fa-list-ul', label='成员列表',
                       schema=Page(title='成员列表', body=[cards_curd]))
hubei_page = PageSchema(url='/add/hubei', icon='fa fa-pen-to-square', label='青春湖北',
                        schema=Page(title='青春湖北', body=[hubei_table]))
jiangxi_page = PageSchema(url='/add/jiangxi', icon='fa fa-pen-to-square', label='江西共青团',
                          schema=Page(title='江西共青团', body=[jiangxi_table]))
jiangsu_page = PageSchema(url='/add/jiangsu', icon='fa fa-pen-to-square', label='江苏共青团',
                          schema=Page(title='江苏共青团', body=[jiangsu_table]))
anhui_page = PageSchema(url='/add/anhui', icon='fa fa-pen-to-square', label='安徽共青团',
                        schema=Page(title='安徽共青团', body=[anhui_table]))
henan_page = PageSchema(url='/add/henan', icon='fa fa-pen-to-square', label='河南共青团',
                        schema=Page(title='河南共青团', body=[henan_table]))
sichuan_page = PageSchema(url='/add/sichuan', icon='fa fa-pen-to-square', label='天府新青年',
                          schema=Page(title='天府新青年', body=[sichuan_table]))
shandong_page = PageSchema(url='/add/shandong', icon='fa fa-pen-to-square', label='青春山东',
                           schema=Page(title='青春山东', body=[shandong_table]))
chongqing_page = PageSchema(url='/add/chongqing', icon='fa fa-pen-to-square', label='重庆共青团',
                            schema=Page(title='重庆共青团', body=[chongqing_table]))
admin_app = App(brandName='TeenStudy',
                logo='https://i.328888.xyz/2023/02/23/xIh5k.png',
                header=header,
                pages=[{
                    'children': [
                        admin_page,
                        PageSchema(icon='fa fa-circle-user', label='成员管理',
                                   children=[list_page, hubei_page, jiangxi_page, jiangsu_page, anhui_page, henan_page,
                                             sichuan_page, shandong_page, chongqing_page]),
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
                    html=f'<div class="p-2 text-center bg-blue-100">Copyright © 2022 - 2023 <a href="https://github.com/ZM25XC/TeenStudy" target="_blank" class="link-secondary">TeenStudy</a> X<a target="_blank" href="https://github.com/baidu/amis" class="link-secondary" rel="noopener"> amis v2.2.0</a></div>'))
