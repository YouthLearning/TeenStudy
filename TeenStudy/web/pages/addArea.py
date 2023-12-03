from amis import InputText, Form, DisplayModeEnum, Alert, LevelEnum, Select, PageSchema
from amis import Page, ActionType, Dialog, Card, Tpl, Switch, CardsCRUD

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
                  description='学校类型，不清楚请勿改动'),
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
                                  icon='fas fa-user-tag text-primary',
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
        icon='fas fa-check text-success',
        confirmText='是否提交最新一期青年大学习？',
        api='get:/TeenStudy/api/commit?user_id=${user_id}&area=${area}'
    ), ActionType.Ajax(
        tooltip='删除',
        label="删除",
        icon='fas fa-trash-can text-danger',
        confirmText='删除该用户',
        api='delete:/TeenStudy/api/delete_member?user_id=${user_id}'
    ), ],
    toolbar=[
        Tpl(tpl='$area', className='label label-warning', hiddenOn=True),
        Switch(name='auto_submit',
               value='${auto_submit}',
               tooltip='自动提交大学习开关',
               onText='开启',
               offText='关闭',
               onEvent={
                   'change': {
                       'actions': {
                           'actionType': 'ajax',
                           'args': {
                               'api': {
                                   'url': '/TeenStudy/api/set_auto_submit',
                                   'method': 'put'
                               },
                               'messages': {
                                   'success': '自动提交已设置为${event.data.value==true?"开启":"关闭"}',
                                   'failed': '修改失败！'
                               },
                               'status': '${event.data.value}',
                               'id': '${id}'
                           }
                       }
                   }
               })
    ])
"""成员卡片面板"""
cards_curd = CardsCRUD(mode='cards',
                       title='',
                       syncLocation=False,
                       name="member",
                       fetchFailed="数据初始化！",
                       api='get:/TeenStudy/api/get_members',
                       loadDataOnce=True,
                       interval=180000,
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

list_page = PageSchema(url='/TeenStudy/list', icon='fas fa-list-ul', label='成员列表',
                       schema=Page(title='成员列表', body=[cards_curd]))

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
            hiddenOn="this.group_id==''?true:false"
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
            value="${IF(ISEMPTY(organization),SPLIT(college,'-')[1],SPLIT(organization,'-')[1])}",
            disabled=True
        ),
        Select(
            type="select",
            label="学校类型",
            name="university_type",
            searchable=True,
            required=True,
            clearable=True,
            options=[
                {'label': "团省委机关", "value": "团省委机关-N0017"},
                {'label': "省直属单位团委", "value": "省直属单位团委-N0016"},
                {'label': "省属本科院校团委", "value": "省属本科院校团委-N0013"},
                {'label': "非省属本科院校团委", "value": "非省属本科院校团委-N0014"},
                {'label': "高职专科院校团委", "value": "高职专科院校团委-N0015"},
                {'label': "南昌市", "value": "南昌市-N0002"},
                {'label': "九江市", "value": "九江市-N0003"},
                {'label': "景德镇市", "value": "景德镇市-N0004"},
                {'label': "萍乡市", "value": "萍乡市-N0005"},
                {'label': "新余市", "value": "新余市-N0006"},
                {'label': "鹰潭市", "value": "鹰潭市-N0007"},
                {'label': "赣州市", "value": "赣州市-N0008"},
                {'label': "宜春市", "value": "宜春市-N0009"},
                {'label': "上饶市", "value": "上饶市-N0010"},
                {'label': "吉安市", "value": "吉安市-N0011"},
                {'label': "抚州市", "value": "抚州市-N0012"}
            ]
        ),
        Select(
            type="select",
            label="学校名称",
            name="university",
            value="${IF(ISEMPTY(university_type),university,'')}",
            searchable=True,
            required=True,
            clearable=True,
            source={
                "method": "get",
                "url": "/TeenStudy/api/organization?pid=${SPLIT(university_type,'-')[1]}",
                "sendOn": "this.university_type!==''"
            }, hiddenOn="this.university_type===''|| this.university_type===undefined"
        ),
        Select(
            type="select",
            label="学院名称",
            name="college",
            value="${IF(ISEMPTY(university),college,'')}",
            searchable=True,
            required=True,
            clearable=True,
            source={
                "method": "get",
                "url": "/TeenStudy/api/organization?pid=${SPLIT(university,'-')[1]}",
                "sendOn": "this.university!==''"
            },
            hiddenOn="this.university_type==='' || this.university===''||this.university_type===undefined || this.university===undefined"
        ),
        Select(
            type="select",
            label="团支部",
            description="团支部名称，对应江西共青团个人修改信息页 班级/团支部",
            name="organization",
            value="${IF(ISEMPTY(college),organization,'')}",
            searchable=True,
            required=False,
            clearable=True,
            source={
                "method": "get",
                "url": "/TeenStudy/api/organization?pid=${SPLIT(college,'-')[1]}",
                "sendOn": "this.college!==''"
            },
            hiddenOn="this.university_type===''||this.university===''||this.college===''||this.university_type===undefined||this.university===undefined||this.college===undefined"
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
            label="url",
            description="个人信息修改页，点右上角分享，复制链接填入即可 链接格式：http://dxx.ahyouth.org.cn/modify/?tk=您的token值",
            name="url",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=128
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
"""吉林添加成员面板"""
jilin_table = Form(
    title="添加吉青飞扬用户",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/jilin/add",
    redirect="/TeenStudy/login",
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
            value="吉林",
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
            description="您的姓名",
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
        ),
        InputText(
            label="学校",
            description="你就读的高校",
            name="university",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学院",
            description="学院名称",
            name="college",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部",
            description="团支部|班级，没有可不填",
            name="organization",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
        )

    ]
)
"""广东地区添加用户"""
guangdong_table = Form(
    title="添加广东共青团用户",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/guangdong/add",
    redirect="/TeenStudy/login",
    body=[
        Alert(level=LevelEnum.info,
              className='white-space-pre-wrap',
              body=(
                  "链接获取方式:\n12355青春之声公众号\n智慧团建-认证资料-生成电子团员证，点击最下方生成按钮。\n在团员证页面复制链接 应为：https://tuan.12355.net/wechat/view/information/member_certification_generated.html?memberId=xxxxxx&showMemberAdditionNames=&showMemberRewardIds=&isShowAllFee=true \n其中xxxxxx即为mid")),
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
            value="广东",
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
            description="您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="url",
            description="链接格式：https://tuan.12355.net/wechat/view/information/member_certification_generated.html?memberId=xxxxxx&showMemberAdditionNames=&showMemberRewardIds=&isShowAllFee=true",
            name="url",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=512
        ),
        InputText(
            label="学校",
            description="你就读的高校",
            name="university",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学院",
            description="学院名称",
            name="college",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部",
            description="团支部|班级，没有可不填",
            name="organization",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
        )]
)
"""北京地区添加用户面板"""
beijing_table = Form(
    title="添加北京共青团用户",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/beijing/add",
    redirect="/TeenStudy/login",
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
            value="北京",
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
            description="您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ), InputText(
            label="大学习ID",
            description="名字后面括号内的数字",
            name="dxx_id",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="学校",
            description="你就读的高校",
            name="university",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学院",
            description="学院名称",
            name="college",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部",
            description="团支部|班级，没有可不填",
            name="organization",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部ID",
            description="支部后面括号内的数字",
            name="organization_id",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="账号",
            description="登录北京共青团的账号",
            name="cookie",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ), InputText(
            label="密码",
            description="登陆北京共青团的密码",
            name="token",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        )
    ]
)
"""天津地区添加用户"""
tianjin_table = Form(
    title="添加津彩青春用户",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/tianjin/add",
    redirect="/TeenStudy/login",
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
            value="天津",
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
            description="您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="学校",
            description="你就读的高校",
            name="university",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学院",
            description="学院名称",
            name="college",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部",
            description="团支部|班级，没有可不填",
            name="organization",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
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
    ]
)
"""三秦青年青年添加用户"""
shanxi_table = Form(
    title="添加三秦青年用户",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/ShanXi/add",
    redirect="/TeenStudy/login",
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
            value="陕西",
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
            description="您的姓名",
            name="name",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=8
        ),
        InputText(
            label="学校",
            description="你就读的高校",
            name="university",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=24
        ),
        InputText(
            label="学院",
            description="学院名称",
            name="college",
            inline=False,
            required=True,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="团支部",
            description="团支部|班级，没有可不填",
            name="organization",
            inline=False,
            required=False,
            value="",
            clearable=True,
            maxLength=32
        ),
        InputText(
            label="token",
            description="自行抓包获取",
            name="token",
            inline=False,
            required=True,
            value="",
            clearable=True,
        ),
    ]
)
hubei_page = PageSchema(url='/TeenStudy/add/hubei', icon='far fa-edit', vendor="", label='青春湖北',
                        schema=Page(title='青春湖北', body=[hubei_table]))
jiangxi_page = PageSchema(url='/TeenStudy/add/jiangxi', icon='far fa-edit', vendor="", label='江西共青团',
                          schema=Page(title='江西共青团', body=[jiangxi_table]))
anhui_page = PageSchema(url='/TeenStudy/add/anhui', icon='far fa-edit', vendor="", label='安徽共青团',
                        schema=Page(title='安徽共青团', body=[anhui_table]))
sichuan_page = PageSchema(url='/TeenStudy/add/sichuan', icon='far fa-edit', vendor="", label='天府新青年',
                          schema=Page(title='天府新青年', body=[sichuan_table]))
shandong_page = PageSchema(url='/TeenStudy/add/shandong', icon='far fa-edit', vendor="", label='青春山东',
                           schema=Page(title='青春山东', body=[shandong_table]))
chongqing_page = PageSchema(url='/TeenStudy/add/chongqing', icon='far fa-edit', vendor="", label='重庆共青团',
                            schema=Page(title='重庆共青团', body=[chongqing_table]))
jilin_page = PageSchema(url='/TeenStudy/add/jilin', icon='far fa-edit', vendor="", label='吉青飞扬',
                        schema=Page(title='吉青飞扬', body=[jilin_table]))
guangdong_page = PageSchema(url='/TeenStudy/add/guangdong', icon='far fa-edit', vendor="", label='广东共青团',
                            schema=Page(title='广东共青团', body=[guangdong_table]))
beijing_page = PageSchema(url='/TeenStudy/add/beijing', icon='far fa-edit', vendor="", label='北京共青团',
                          schema=Page(title='北京共青团', body=[beijing_table]))
tianjin_page = PageSchema(url='/TeenStudy/add/tianjin', icon='far fa-edit', vendor="", label='津彩青春',
                          schema=Page(title='津彩青春', body=[tianjin_table]))
shanxi_page = PageSchema(url='/TeenStudy/add/shanxi', icon='far fa-edit', vendor="", label='三秦青年',
                         schema=Page(title='三秦青年', body=[shanxi_table]))
areaPage = [list_page,
            hubei_page, jiangxi_page, anhui_page,
            sichuan_page, shandong_page, chongqing_page, jilin_page, guangdong_page, beijing_page,
            tianjin_page, shanxi_page
            ]
