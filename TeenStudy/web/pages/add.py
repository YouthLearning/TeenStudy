from amis import Page, Divider, Html, Form, InputText, DisplayModeEnum, Select, Service, Alert, LevelEnum

logo = Html(html=f'''
<p align="center">
    <a href="https://github.com/ZM25XC/TeenStudy/">
        <img src="https://i.328888.xyz/2023/02/23/xIh5k.png"
         width="256" height="256" alt="TeenStudy">
    </a>
</p>
<h2 align="center">大学习自动提交</h2>
<div align="center">
    <a href="https://github.com/ZM25XC/TeenStudy" target="_blank">
    Github仓库</a>
</div>
<br>
''')
footer = Html(
    html=f'<div class="p-2 text-center bg-blue-100">Copyright © 2022 - 2023 <a href="https://github.com/ZM25XC/TeenStudy" target="_blank" class="link-secondary">TeenStudy</a> X<a target="_blank" href="https://github.com/baidu/amis" class="link-secondary" rel="noopener"> amis v2.2.0</a></div>')
hubei_table = Form(
    title="青春湖北",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/add",
    redirect="/TeenStudy/login",
    body=[
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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

hubei_page = Page(title='添加大学习', body=[logo, Divider(), hubei_table, footer])
jiangxi_table = Form(
    title="江西共青团",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/add",
    redirect="/TeenStudy/login",
    body=[
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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
                             {'label': '景德镇学院', 'value': '景德镇学院'}, {'label': '萍乡学院', 'value': '萍乡学院'},
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

jiangxi_page = Page(title='添加大学习', body=[logo, Divider(), jiangxi_table, footer])

jiangsu_table = Form(
    title="江苏共青团",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/jiangsu/add",
    redirect="/TeenStudy/login",
    body=[
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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

jiangsu_page = Page(title='添加大学习', body=[logo, Divider(), jiangsu_table, footer])

anhui_table = Form(
    title="安徽共青团",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/anhui/add",
    redirect="/TeenStudy/login",
    body=[
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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

anhui_page = Page(title='添加大学习', body=[logo, Divider(), anhui_table, footer])

henan_table = Form(
    title="河南共青团",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/henan/add",
    redirect="/TeenStudy/login",
    body=[
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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

henan_page = Page(title='添加大学习', body=[logo, Divider(), henan_table, footer])

sichuan_table = Form(
    title="天府新青年",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/sichuan/add",
    redirect="/TeenStudy/login",
    body=[
        Alert(level=LevelEnum.info,
              className='white-space-pre-wrap',
              body=(
                  "该地区需要自行抓包填入\ntoken值在https://dxx.scyol.com/api/wechat/login 响应里\n其余信息在 https://dxx.scyol.com/api/student/showStudyStageOrg?id=xxxxxx&stageId=xx 响应里")),
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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

sichuan_page = Page(title='添加大学习', body=[logo, Divider(), sichuan_table, footer])

shandong_table = Form(
    title="青春山东",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/shandong/add",
    redirect="/TeenStudy/login",
    body=[
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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
            description="自行抓包获取，结构为: ohz9xxxxxxxxxxxxlF0Io0uCnM",
            name="openid",
            inline=False,
            required=True,
            value="",
            clearable=True,
        )

    ]
)

shandong_page = Page(title='添加大学习', body=[logo, Divider(), shandong_table, footer])

chongqing_table = Form(
    title="重庆共青团",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/chongqing/add",
    redirect="/TeenStudy/login",
    body=[
        InputText(
            label="用户ID",
            description="用户ID，为用户QQ号，无需填写",
            name="user_id",
            value="${user_id}",
            disabled=True
        ),
        InputText(
            label="通知群ID",
            description="通知群号，无需填写",
            name="group_id",
            value="${group_id}",
            disabled=True
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

chongqing_page = Page(title='添加大学习', body=[logo, Divider(), chongqing_table, footer])
