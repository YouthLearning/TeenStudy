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
- 需要抓包的地区，绑定后尽量别进官方公众号，避免token或cookie刷新导致无法提交
- 本项目需要部署在公网可访问的容器中，并开放端口（nonebot配置的port），否则大部分功能将出现异常
- 欢迎加入[QQ群](https://jq.qq.com/?_wv=1027&k=NGFEwXyS)，交流讨论。
- 时间精力有限，目前只维护湖北和江西两个地区，其他地区出问题请提交Issues,我找个时间修，需要增加地区请进群帮忙测试，个别地区没账号无法测试
- 觉得项目不错，不妨点个stars.

## 支持地区

### 以下地区无需抓包

- 湖北
- 江西

### 以下地区使用微信扫码进行绑定

- 浙江
- 上海

### 以下地区需要抓包

- 江苏
- 安徽
- 河南
- 四川
- 山东
- 重庆



##  安装及更新

1. 使用`git clone https://github.com/ZM25XC/TeenStudy.git`指令克隆本仓库或下载压缩包文件
2. 使用`pip install TeenStudy`来进行安装,使用`pip install TeenStudy -U`进行更新

## 导入插件
**使用第一种安装方式**

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

    

**使用第二种安装方式**
- 在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["TeenStudy"]`


## 机器人配置

- 在nonebot的`.env` 或 `.env.prod`配置文件中设置好超管账号和公网IP

  ```py
  SUPERUSERS=[""]
  DXX_IP=""
  ```

## 使用方式

- 启动nb,等待插件加载数据，加载完毕后登录后台，账号默认为`nonebot配置文件中的超管账号`，密码默认为：`admin`,开放端口（默认为.env中配置的port）
- 在管理后台的推送列表中添加需要开启大学习使用的群聊

## 功能列表
|            指令            |                 指令格式                  |                             说明                             |
| :------------------------: | :---------------------------------------: | :----------------------------------------------------------: |
|         添加大学习         |     添加大学习`地区`     |     添加大学习湖北 添加大学习     |
|         我的大学习         |                我的大学习                 |                         查询个人信息                         |
|         提交大学习         |                提交大学习 戳一戳Bot                 |                      提交最新一期大学习                      |
|           大学习           |            大学习答案、大学习、答案截图             |                  获取最新一期青年大学习答案                  |
|          完成截图          |   完成截图、大学习截图、大学习完成截图    |          获取最新一期青年大学习完成截图（带状态栏）          |
|          完成大学习          |   完成大学习、全员大学习    |        团支书可用，需要成员填写团支书ID，填写后团支书可发指令提交大学习          |
|          重置配置          |   重置配置、刷新配置    |         超管可用，刷新Web UI默认配置          |
|          重置密码          |   重置密码    |          重置登录Web UI的密码为用户ID          |


## ToDo


- [ ] 增加更多地区支持
- [ ] 优化 Bot


## 更新日志

### 2023/03/18
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


### 2023/03/05

- 适配浙江地区，使用微信扫码进行绑定
- 适配上海地区，使用微信扫码进行绑定
- 适配江苏地区，需要自行抓包
- 适配安徽地区，需要自行抓包


### 2023/03/01

- 将代码上传至pypi，可使用`pip install TeenStudy`指令安装本插件
- 上传基础代码
- 适配湖北地区，无需抓包，安装即用
- 适配江西地区，无需抓包，安装即用