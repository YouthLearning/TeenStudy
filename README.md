<div align="center">
    <img src="https://i.328888.xyz/2023/02/28/z23ho.png" alt="TeenStudy.png" border="0" width="500px" height="500px"/>
    <h1>TeenStudy</h1>
    <b>基于nonebot2的青年大学习自动提交插件，用于自动完成大学习，在后台留下记录，返回完成截图</b>
    <br/>
    <a href="https://github.com/ZM25XC/TeenStudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ZM25XC/TeenStudy?style=flat-square"></a>
    <a href="https://github.com/ZM25XC/TeenStudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ZM25XC/TeenStudy?style=flat-square"></a>
    <a href="https://github.com/ZM25XC/TeenStudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ZM25XC/TeenStudy?style=flat-square"></a>
    <a href="https://pypi.python.org/pypi/TeenStudy"><img src="https://img.shields.io/pypi/v/TeenStudy?color=yellow" alt="pypi"></a>
  	<a href="https://pypi.python.org/pypi/TeenStudy">
    <img src="https://img.shields.io/pypi/dm/TeenStudy" alt="pypi download"></a>
     <a href="https://github.com/ZM25XC/TeenStudy">
    <img src="https://visitor-badge.glitch.me/badge?page_id=https://github.com/ZM25XC/TeenStudy" alt="Teenstudy"></a>
	<a href="https://github.com/ZM25XC/TeenStudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ZM25XC/TeenStudy?style=flat-square"></a>
    <a href="https://jq.qq.com/?_wv=1027&k=NGFEwXyS">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-511173803-orange?style=flat-square" alt="QQ Chat Group">
  </a>
  </div>

## 说明

- 本项目为[青年大学习提交](https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy) `Web UI`版
- 本项目基于[nonebot2](https://github.com/nonebot/nonebot2)和[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，使用本插件前请先阅读以上两个项目的使用文档
-  **启动插件之后，一定要登录后台在推送列表中添加需要开启大学习功能的群聊**
- 需要抓包的地区，绑定后尽量别进官方公众号，避免token或cookie刷新导致无法提交
- 本项目需要部署在公网可访问的容器中，并开放端口（nonebot2配置的port），否则大部分功能将出现异常
- 欢迎加入[QQ群](https://jq.qq.com/?_wv=1027&k=NGFEwXyS)，交流讨论。
- 时间精力有限，目前只维护湖北和江西两个地区，其他地区出问题请提交Issues,我找个时间修，需要增加地区请进群帮忙测试，个别地区没账号无法测试

- 觉得项目不错，不妨点个stars.

## 地区状态

<details>

| 共青团名称 | 开发状态 | 备注 |
|:-----:|:----:|:----:|
|青春湖北|支持|无需抓包|
|江西共青团|支持|无需抓包|
|青春上海|支持|微信扫码绑定|
|青春浙江|支持|微信扫码绑定|
|安徽共青团|支持|无需抓包|
|江苏共青团|支持|需要自行抓包|
|青春山东|支持|需要自行抓包|
|重庆共青团|支持|需要自行抓包|
|河南共青团|不支持|cookie时效小于1周|
|天府新青年|支持|不进入公众号token时效大于1周|
|黑龙江共青团|待开发||
|广西青年圈|待开发||
|青春湖南|待开发||
|甘肃青年|待开发||
|山西青年|待开发||
|河北共青团|待开发||
|福建共青团|待开发||
|内蒙古青年|待开发||
|云南共青团|待开发||
|吉青飞扬|待开发||
|三秦青年|待开发||
|青春北京|待开发||
|海南共青团|待开发||
|津彩青春|待开发||
|青春黔言|待开发||
|广东共青团|待开发||
|青春柳州|待开发||
|辽宁共青团|待开发||
|宁夏共青团|待开发||
|新疆共青团|待开发||
|西藏共青团|待开发||
</details>


##  安装及更新

<details>
<summary>第一种方式(不推荐)</summary>

- 使用`git clone https://github.com/ZM25XC/TeenStudy.git`指令克隆本仓库或下载压缩包文件

</details>

<details>
<summary>第二种方式(二选一)</summary>

1、使用`pip install TeenStudy`来进行安装,使用`pip install TeenStudy -U`进行更新
2、使用`nb plugin install TeenStudy`来进行安装,使用`nb plugin install TeenStudy -U`进行更新

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
|    指令    |               指令格式               |                               说明                               |
| :--------: | :----------------------------------: | :--------------------------------------------------------------: |
| 添加大学习 |           添加大学习`地区`           |                    添加大学习湖北 添加大学习                     |
| 我的大学习 |              我的大学习              |                           查询个人信息                           |
| 提交大学习 |         提交大学习 戳一戳Bot         |                        提交最新一期大学习                        |
|   大学习   |     大学习答案、大学习、答案截图     |                    获取最新一期青年大学习答案                    |
|  完成截图  | 完成截图、大学习截图、大学习完成截图 |            获取最新一期青年大学习完成截图（带状态栏）            |
| 完成大学习 |        完成大学习、全员大学习        | 团支书可用，需要成员填写团支书ID，填写后团支书可发指令提交大学习 |
|  重置配置  |          重置配置、刷新配置          |                   超管可用，刷新Web UI默认配置                   |
|  重置密码  |               重置密码               |                   重置登录Web UI的密码为用户ID                   |
|删除大学习|删除大学习|用户申请清除数据库的信息|
|导出用户数据|导出用户数据、导出数据|将数据导出至TeenStudy目录下|
|更新用户数据|更新用户数据、刷新用户数据|将用户数据导入到数据库|
|更新资源数据|更新资源数据、刷新资源数据|更新数据库中的资源数据（江西共青团团支部数据）|


## ToDo


- [ ] 增加更多地区支持
- [ ] 优化 Bot


## 更新日志

###2023/04/12
- 因河南地区cookie时效小于1周，移除河南地区
- 添加`删除大学习`功能，用户可自行删除数据
- 添加`导出用户数据`功能
- 添加`更新用户数据`功能
- 添加`更新资源数据`功能，江西地区更新后请使用下此功能刷新团支部数据
- 添加戳一戳提交大学习开关，默认开启，请在Web UI后台配置页面进行修改
- 添加大学习提醒开关，默认开启，支持修改时间，请在Web UI后台配置页面进行修改
- 添加自动提交大学习开关，默认开启，支持修改时间，请在Web UI后台进行修改
- 调整安徽地区添加方式[#9](https://github.com/ZM25XC/TeenStudy/issues/9)，无需抓包，感谢[@yhzcake](https://github.com/yhzcake)测试提供方法
- 修复Web UI 首页公网IP显示异常
- 修复浙江地区用户重复显示
- 更新江西共青团团支部数据



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