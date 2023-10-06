<div align="center">
    <img src="https://img1.imgtp.com/2023/10/06/NChUNeiA.png" alt="TeenStudy.png" border="0" width="500px" height="500px"/>
    <h1>TeenStudy</h1>
    <b>基于nonebot2和go-cqhttp的青年大学习自动提交插件，用于自动完成大学习，在后台留下记录，返回完成截图</b>
    <br/>
    <a href="https://github.com/YouthLearning/TeenStudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/YouthLearning/TeenStudy?style=flat-square"></a>
    <a href="https://github.com/YouthLearning/TeenStudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/YouthLearning/TeenStudy?style=flat-square"></a>
    <a href="https://github.com/YouthLearning/TeenStudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YouthLearning/TeenStudy?style=flat-square"></a>
    <a href="https://pypi.python.org/pypi/TeenStudy"><img src="https://img.shields.io/pypi/v/TeenStudy?color=yellow" alt="pypi"></a>
  	<a href="https://pypi.python.org/pypi/TeenStudy">
    <img src="https://img.shields.io/pypi/dm/TeenStudy" alt="pypi download"></a>
    <a href="https://github.com/YouthLearning/TeenStudy">
    <img src="https://views.whatilearened.today/views/github/YouthLearning/TeenStudy.svg" alt="Views"></a>
	<a href="https://github.com/YouthLearning/TeenStudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/YouthLearning/TeenStudy?style=flat-square"></a>
    <a href="https://onebot.dev/">
    <img src="https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="onebot"></a>
    <a href="https://jq.qq.com/?_wv=1027&k=NGFEwXyS">
    <img src="https://img.shields.io/badge/QQ反馈群-511173803-orange?style=flat-square" alt="QQ Chat Group"></a>
	<a href="http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=2PQucjirnkHyPjoS1Pkr-ai2aPGToBKm">
    <img src="https://img.shields.io/badge/QQ体验群-821280615-orange?style=flat-square" alt="QQ Chat Group">
  </a>
  </div>

## 说明

- 本项目基于[nonebot2](https://github.com/nonebot/nonebot2)和[OneBot V11](https://onebot.dev/)协议，使用本插件前请先阅读以上两个项目的使用文档
-  **启动插件之后，一定要登录后台在推送列表中添加需要开启大学习功能的群聊**
-  **本项目无法在中国大陆地区（除港、澳、台）IP环境下使用，如有开启代理，请关闭或添加代理规则**
- 需要抓包的地区，绑定后尽量别进官方公众号，避免token或cookie刷新导致无法提交
- 本项目需要部署在公网可访问的容器中，并开放端口（nonebot2配置的port），否则大部分功能将出现异常
- 欢迎加入[QQ反馈群](https://jq.qq.com/?_wv=1027&k=NGFEwXyS)，交流讨论，如您不会搭建又想每周自动提交，可加入[QQ体验群](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=2PQucjirnkHyPjoS1Pkr-ai2aPGToBKm)。
- 时间精力有限，目前只维护湖北和江西两个地区，其他地区出问题请提交Issues,我找个时间修，需要增加地区请进群帮忙测试，个别地区没账号无法测试
- 觉得项目不错，不妨点个stars.

## 地区状态

<details>

|  共青团名称  | 开发状态 |             备注             |
| :----------: | :------: | :--------------------------: |
|   青春湖北   |   支持   |           无需抓包           |
|  江西共青团  |   支持   |           无需抓包           |
|  安徽共青团  |   支持   |           无需抓包           |
|  广东共青团  |   支持   |           无需抓包           |
|   青春北京   |   支持   |           无需抓包           |
|   青春上海   |   支持   |         微信扫码绑定         |
|   青春浙江   |   支持   |         微信扫码绑定         |
|   津彩青春   |   支持   |         需要自行抓包         |
|   青春山东   |   支持   |         需要自行抓包         |
|  重庆共青团  |   支持   |         需要自行抓包         |
|   吉青飞扬   |   支持   |         需要自行抓包         |
|  天府新青年  |   支持   | 绑定好信息后不进入天府新青年云token时效为**100**Years |
|  河南共青团  |  不支持  |      cookie时效小于1周       |
|  江苏共青团  |  不支持  |      cookie时效小于1周       |
| 黑龙江共青团 |  不支持  |      cookie时效小于1周       |
|  广西青年圈  |  待开发  |                              |
|   青春湖南   |  待开发  |                              |
|   甘肃青年   |  待开发  |                              |
|   山西青年   |  待开发  |                              |
|  河北共青团  |  待开发  |                              |
|  福建共青团  |  待开发  |                              |
|  内蒙古青年  |  待开发  |                              |
|  云南共青团  |  待开发  |                              |
|   三秦青年   |  待开发  |                              |
|  海南共青团  |  待开发  |                              |
|   青春黔言   |  待开发  |                              |
|   青春柳州   |  待开发  |                              |
|  辽宁共青团  |  待开发  |                              |
|  宁夏共青团  |  待开发  |                              |
|  新疆共青团  |  待开发  |                              |
|  西藏共青团  |  待开发  |                              |
</details>


##  安装及更新

<details>
<summary>第一种方式(不推荐)</summary>

- 使用`git clone https://github.com/YouthLearning/TeenStudy.git`指令克隆本仓库或下载压缩包文件

</details>

<details>
<summary>第二种方式(二选一)</summary>

- 使用`pip install TeenStudy`来进行安装,使用`pip install TeenStudy -U`进行更新
- 使用`nb plugin install TeenStudy`来进行安装,使用`nb plugin install TeenStudy -U`进行更新

</details>


## 导入插件

<details>
<summary>使用第一种方式安装看此方法</summary>

- 将`TeenStudy`放在nb的`plugins`目录下，运行nb机器人即可

- 文件结构如下

    ```py
    📦 AweSome-Bot
    ├── 📂 awesome_bot
    │   └── 📂 plugins
    |       └── 📂 TeenStudy
    |           └── 📜 __init__.py
    ├── 📜 .env.prod
    ├── 📜 .gitignore
    ├── 📜 pyproject.toml
    └── 📜 README.md
    ```

    

</details>

<details>
<summary>使用第二种方式安装看此方法</summary>

- 在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["TeenStudy"]`

</details>

## 机器人配置

- 在nonebot的`.env` 或 `.env.prod`配置文件中修改nonebot2的`HOST`为`0.0.0.0`、设置好超管账号和公网IP

  ```py
  HOST = "0.0.0.0"  #nonebot2监听的IP
  SUPERUSERS = [""] # 超级用户
  COMMAND_START=[""] # 命令前缀,根据需要自行修改
  DXX_IP = ""
  ```

## 使用方式

- 启动nb,等待插件加载数据，加载完毕后登录后台，账号默认为`nonebot配置文件中的超管账号`，密码默认为：`admin`,开放端口（默认为.env中配置的port）
- 在管理后台的推送列表中添加需要开启大学习使用的群聊

## 功能列表
|     指令     |               指令格式               |                               说明                               |
| :----------: | :----------------------------------: | :--------------------------------------------------------------: |
|  添加大学习  |           添加大学习`地区`           |                    添加大学习湖北 添加大学习                     |
|  我的大学习  |              我的大学习              |                           查询个人信息                           |
|  提交大学习  |         提交大学习`x期` 戳一戳Bot         |                        提交一期（默认最新一期）大学习                        |
|    大学习    |     大学习答案、大学习、答案截图     |                    获取最新一期青年大学习答案                    |
|   完成截图   | 完成截图`x期`、大学习截图`x期`、大学习完成截图`x期` |            获取青年大学习一期（默认最新一期）完成截图（带状态栏）            |
|  完成大学习  |        完成大学习、全员大学习        | 团支书可用，需要成员填写团支书ID，填写后团支书可发指令提交大学习 |
|   重置配置   |          重置配置、刷新配置          |                   超管可用，刷新Web UI默认配置                   |
|   重置密码   |               重置密码               |                   重置登录Web UI的密码为用户ID                   |
|  删除大学习  |              删除大学习              |                     用户申请清除数据库的信息                     |
| 导出用户数据 |        导出用户数据、导出数据        |                   将数据导出至TeenStudy目录下                    |
| 更新用户数据 |      更新用户数据、刷新用户数据      |                      将用户数据导入到数据库                      |
| 更新资源数据 |      更新资源数据、刷新资源数据      |          更新数据库中的资源数据（江西共青团团支部数据）          |


## ToDo


- [ ] 增加更多地区支持
- [ ] 优化 Bot


## 更新日志


### 2023/09/11

- 修复江西地区组织获取失败BUG
- 完成截图状态栏随机时间范围调整为2~5分钟
- 开放获取往期完成截图功能,指令为`完成截图 x期` 示例：完成截图2023年第18期 
- 湖北地区(其余地区等待适配)开放提交往期大学习功能，指令为`提交大学习 x期` 示例：提交大学习2023年第18期
- 项目进入重构状态，计划使用`node.js` `vue.js` `typescript` `express` `vite` `element-plus`  `mongoDB` 搭建API服务端(带Web UI)适配多平台

<details>
<summary>2023/08/31</summary>

- 因项目特殊性，将项目移交至组织
- 因[ZM25XC](https://github.com/ZM25XC)个人原因，维护人员变更为[TeenStudyFlow](https://github.com/TeenStudyFlow)
- 优化更新获取最新一期答案的算法
- 因使用QQNT无法查看回复中的图片，项目将所有涉及回复改成单独发送

</details>

<details>
<summary>2023/06/12</summary>

- 适配北京地区，无需抓包
- 增加天津地区，需要自行抓包
- 因江苏和黑龙江地区Cookie时效小于1周，移除江苏和黑龙江地区
- Web UI添加日志和主动退出功能
- 更新江西地区拉取团支部数据方式，移除缓存团支部数据，包体积减小50%
- 修复大学习公网检测失败问题
- 更新Nonebot2强制meta字段
- 同步UI依赖AMIS版本到最新版本
- 开放体验群，不会搭建又想使用的可加[QQ体验群](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=2PQucjirnkHyPjoS1Pkr-ai2aPGToBKm)
  
</details>

<details>

<summary>2023/05/21</summary>

- 增加黑龙江地区，需要自行抓包，该地区上线测试中，请积极提issue反馈
- 下版本为大版本更新，将添加新功能，优化功能，请积极提issue反馈或加交流群反馈


</details>


<details>
<summary>2023/05/11</summary> 

- 增加广东地区，无需抓包[#13](https://github.com/YouthLearning/TeenStudy/issues/13)，感谢[@neal240](https://github.com/neal240)提供账号测试

</details>

<details>
<summary>2023/05/06</summary> 

- 增加吉林地区，需要自行抓包
- 修复超管更改登录密码后用原密码能继续登录问题
- 添加二维码转链接开关，需要自行在后台配置页面打开
- 调整部分依赖

</details>

<details>
<summary> 2023/04/12</summary> 

- 因河南地区cookie时效小于1周，移除河南地区
- 添加`删除大学习`功能，用户可自行删除数据
- 添加`导出用户数据`功能
- 添加`更新用户数据`功能
- 添加`更新资源数据`功能，江西地区更新后请使用下此功能刷新团支部数据
- 添加戳一戳提交大学习开关，默认开启，请在Web UI后台配置页面进行修改
- 添加大学习提醒开关，默认开启，支持修改时间，请在Web UI后台配置页面进行修改
- 添加自动提交大学习开关，默认开启，支持修改时间，请在Web UI后台进行修改
- 调整安徽地区添加方式[#9](https://github.com/YouthLearning/TeenStudy/issues/9)，无需抓包，感谢[@yhzcake](https://github.com/yhzcake)测试提供方法
- 修复Web UI 首页公网IP显示异常
- 修复浙江地区用户重复显示
- 更新江西共青团团支部数据
  
</details>


<details>
<summary>2023/03/18</summary>

- 适配河南地区，需要自行抓包
- 适配四川地区，需要自行抓包
- 适配山东地区，需要自行抓包
- 适配重庆地区，需要自行抓包
- 添加自动获取公网IP功能，别再问如何配置公网IP啦
- 添加重置密码功能，指令`重置密码`
- 添加重置配置功能，指令`重置配置`，`刷新配置`
- 添加完成大学习功能，团支书可一次性提交全班的大学习，指令`完成大学习`，`全员大学习`
- 管理后台开放添加用户权限（浙江，上海地区无法添加）
- 优化用户信息页
- 优化登录界面提示
- 将添加链接，登录链接转化成二维码，减少公网IP暴露，没啥用，样式好看一些
- 修复Ubuntu系统导入资源失败BUG
  
</details>

<details>

<summary>2023/03/05</summary>

- 适配浙江地区，使用微信扫码进行绑定
- 适配上海地区，使用微信扫码进行绑定
- 适配江苏地区，需要自行抓包
- 适配安徽地区，需要自行抓包

</details>

<details>
<summary>2023/03/01</summary>

- 将代码上传至pypi，可使用`pip install TeenStudy`指令安装本插件
- 上传基础代码
- 适配湖北地区，无需抓包，安装即用
- 适配江西地区，无需抓包，安装即用

</details>
