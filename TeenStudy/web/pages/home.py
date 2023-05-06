from amis import App, PageSchema, Flex, ActionType, LevelEnum, Dialog, Form, DisplayModeEnum, InputText, TableColumn, \
    CRUD, Tpl, Switch
from amis import Html, Page, Property, Service, Divider

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
operation_button = Flex(justify='center', items=[
    ActionType.Dialog(
        label='修改信息',
        className='m-l',
        level=LevelEnum.primary,
        dialog=Dialog(title='修改信息',
                      size='lg',
                      body=[
                          Form(
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
                                            description='学校类型，不清楚清无改动'),
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
                      ])
    ),
    ActionType.Ajax(
        label="提交大学习",
        className='m-l',
        level=LevelEnum.primary,
        confirmText='是否提交最新一期青年大学习？',
        api='get:/TeenStudy/api/commit?user_id=${user_id}&area=${area}'
    ),
    Switch(name='auto_submit',
           value='${auto_submit}',
           tooltip='自动提交大学习开关',
           onText='自动提交大学习开',
           offText='自动提交大学习关',
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

from_table = Service(
    title="",
    api="/TeenStudy/api/get_user?user_id=${user_id}",
    interval=12000,
    body=[
        Property(
            title='用户详细信息',
            column=2,
            items=[
                Property.Item(
                    label='用户ID',
                    content='${user_id}'
                ),
                Property.Item(
                    label='姓名',
                    content='${name}'
                ),
                Property.Item(
                    label='地区',
                    content='${area}'
                ),
                Property.Item(
                    label='学校',
                    content='${university}'
                ),
                Property.Item(
                    label='学院',
                    content='${college}'
                ),
                Property.Item(
                    label='团支部',
                    content='${organization}'
                ),
                Property.Item(
                    label='最新提交期数',
                    content='${catalogue}'
                ),
                Property.Item(
                    label='最新提交时间',
                    content='${commit_time}'
                ),
                Property.Item(
                    label='性别',
                    content='${gender}',
                    visibleOn="${gender==null?false:true}"
                ),
                Property.Item(
                    label='手机号|学号',
                    content='${mobile}',
                    visibleOn="${mobile==null?false:true}"
                ),
                Property.Item(
                    label='团支书ID',
                    content='${leader}',
                    visibleOn="${leader==null?false:true}"
                ),
                Property.Item(
                    label='Uid|Nid',
                    content='${dxx_id}',
                    visibleOn="${dxx_id==null?false:true}"
                ),
                Property.Item(
                    label='学校类型',
                    content='${university_type}',
                    visibleOn="${university_type==null?false:true}"
                ),
                Property.Item(
                    label='学校ID',
                    content='${university_id}',
                    visibleOn="${university_id==null?false:true}"
                ),
                Property.Item(
                    label='学院ID',
                    content='${college_id}',
                    visibleOn="${college_id==null?false:true}"
                ),
                Property.Item(
                    label='团支部ID',
                    content='${organization_id}',
                    visibleOn="${organization_id==null?false:true}"
                ), Property.Item(
                    label='openid',
                    content='${openid}',
                    visibleOn="${openid==null?false:true}"
                ), Property.Item(
                    label='token',
                    content='${token}',
                    visibleOn="${token==null?false:true}",
                    span=2
                ), Property.Item(
                    label='cookie',
                    content='${cookie}',
                    visibleOn="${cookie==null?false:true}",
                    span=2
                )
            ]
        )
    ]
)
"""提交记录模板"""
record_table = CRUD(mode='table',
                    title='',
                    syncLocation=False,
                    api='/TeenStudy/api/get_records?user_id=${user_id}',
                    type='crud',
                    headerToolbar=[],
                    itemActions=[],
                    footable=True,
                    columns=[
                        TableColumn(label='用户ID', name='user_id'),
                        TableColumn(label='姓名', name='name'),
                        TableColumn(label='提交地区', name='area'),
                        TableColumn(label='学校名称', name='university'),
                        TableColumn(label='学院名称', name='college'),
                        TableColumn(label='团支部', name='organization'),
                        TableColumn(label='提交期数', name='catalogue', searchable=True),
                        TableColumn(label='提交状态', name='${status==true?"成功":"失败"}'),
                        TableColumn(type='tpl', tpl='${time|date:YYYY-MM-DD HH\\:mm\\:ss}',
                                    label='提交时间',
                                    name='time', sortable=True)
                    ])
answer_table = CRUD(mode='table',
                    title='',
                    syncLocation=False,
                    api='/TeenStudy/api/get_answers',
                    type='crud',
                    headerToolbar=[],
                    itemActions=[],
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
                    ])
page_detail = Page(title='', body=[logo, operation_button, Divider(), from_table])
home_page = PageSchema(url='/home', label='首页', icon='fa fa-home', isDefaultPage=True, schema=page_detail)
home_app = App(brandName='TeenStudy',
               logo='https://i.328888.xyz/2023/02/23/xIh5k.png',
               header=header,
               pages=[{
                   'children': [
                       home_page,
                       PageSchema(url="answer", label='大学习列表', icon='fa fa-book-open',
                                  schema=Page(title='', body=[answer_table])),
                       PageSchema(url="/records", label='提交记录', icon='fa fa-code-commit',
                                  schema=Page(title='', body=[record_table]))
                   ]}],
               footer=Html(
                   html=f'<div class="p-2 text-center bg-blue-100">Copyright © 2022 - 2023 <a href="https://github.com/ZM25XC/TeenStudy" target="_blank" class="link-secondary">TeenStudy</a> X<a target="_blank" href="https://github.com/baidu/amis" class="link-secondary" rel="noopener"> amis v2.2.0</a></div>'))
