from amis import Form, InputText, InputPassword, DisplayModeEnum, Horizontal, Remark, Html, Page, AmisAPI, Wrapper, \
    Switch

logo = Html(html=f'''
<p align="center">
    <a href="https://github.com/YouthLearning/TeenStudy/">
        <img src="https://img1.imgtp.com/2023/06/11/sG4KdlpL.png"
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
<br>
''')
login_api = AmisAPI(
    url='/TeenStudy/api/login',
    method='post',
    adaptor='''
        if (payload.status == 0) {
            localStorage.setItem("token", payload.data.token);
            localStorage.setItem("user_id", payload.data.user_id);
            localStorage.setItem("role", payload.data.role);
            if(payload.data.role){
            window.location.href = '/TeenStudy/admin'
            }
            else{
            window.location.href = '/TeenStudy/home?user_id='+payload.data.user_id;}
        }
        return payload;
    '''
)

login_form = Form(api=login_api, title='', body=[
    InputText(name='user_id', label='用户ID', description='默认为用户QQ号'),
    InputPassword(name='password', label='密码',
                  description='管理员默认为admin，普通用户默认为QQ号'),
    Switch(name='role', label='身份组', onText='管理员', offText='用户', value=False,
           labelRemark=Remark(shape='circle', content='是否以管理员身份登录'))
], mode=DisplayModeEnum.horizontal, horizontal=Horizontal(left=3, right=9, offset=5), submitText="登录")
body = Wrapper(className='w-2/5 mx-auto my-0 m:w-full', body=login_form)
login_page = Page(title='', body=[logo, body])
