from amis import Page, Divider, Html, Form, InputText, DisplayModeEnum, Select, Alert, LevelEnum

logo = Html(html=f'''
<p align="center">
    <a href="https://github.com/ZM25XC/TeenStudy/">
        <img src="https://i.imgloc.com/2023/05/20/VyRjTV.png"
         width="256" height="256" alt="TeenStudy">
    </a>
</p>
<h2 align="center">大学习自动提交</h2>
<div align="center">
    <a href="https://github.com/ZM25XC/TeenStudy" target="_blank">
    Github仓库</a>
    <a href="https://jq.qq.com/?_wv=1027&k=NGFEwXyS" target="_blank">QQ反馈群</a>
    <a href="http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=2PQucjirnkHyPjoS1Pkr-ai2aPGToBKm" target="_blank">QQ体验群</a>
</div>

<br>
''')
footer = Html(
    html=f'<div class="p-2 text-center bg-blue-100">Copyright © 2022 - 2023 <a href="https://github.com/ZM25XC/TeenStudy" target="_blank" class="link-secondary">TeenStudy v0.2.0</a> X<a target="_blank" href="https://github.com/baidu/amis" class="link-secondary" rel="noopener"> amis v3.1.1</a></div>')
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

jiangxi_page = Page(title='添加大学习', body=[logo, Divider(), jiangxi_table, footer])

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

anhui_page = Page(title='添加大学习', body=[logo, Divider(), anhui_table, footer])

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

jilin_table = Form(
    title="吉青飞扬",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/jilin/add",
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

jilin_page = Page(title='添加大学习', body=[logo, Divider(), jilin_table, footer])

guangdong_table = Form(
    title="广东共青团",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/guangdong/add",
    redirect="/TeenStudy/login",
    body=[
        Alert(level=LevelEnum.info,
              className='white-space-pre-wrap',
              body=(
                  "链接获取方式:\n12355青春之声公众号\n智慧团建-认证资料-生成电子团员证，点击最下方生成按钮。\n在团员证页面复制链接 应为：https://tuan.12355.net/wechat/view/information/member_certification_generated.html?memberId=xxxxxx&showMemberAdditionNames=&showMemberRewardIds=&isShowAllFee=true \n其中xxxxxx即为mid")),
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

guangdong_page = Page(title='添加大学习', body=[logo, Divider(), guangdong_table, footer])

beijing_table = Form(
    title="北京共青团",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/beijing/add",
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

beijing_page = Page(title='添加大学习', body=[logo, Divider(), beijing_table, footer])

tianjin_table = Form(
    title="津彩青春",
    mode=DisplayModeEnum.horizontal,
    api="post:/TeenStudy/api/tianjin/add",
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

tianjin_page = Page(title='添加大学习', body=[logo, Divider(), tianjin_table, footer])
