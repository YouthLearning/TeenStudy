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
- 本项目安装后，必须登录后台配置公网ip，开放端口，否则无法进行绑定操作
- 需要抓包的地区，绑定后尽量别进官方公众号，避免token或cookie刷新导致无法提交
- 欢迎加入[QQ群](https://jq.qq.com/?_wv=1027&k=NGFEwXyS)，交流讨论。
- 时间精力有限，目前只维护湖北和江西两个地区，其他地区出问题请提交Issues,我找个时间修，需要增加地区可以提交Pull requests
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
    ├── 📜 .env
    ├── 📜 .env.dev
    ├── 📜 .env.prod
    ├── 📜 .gitignore
    ├── 📜 docker-compose.yml
    ├── 📜 Dockerfile
    ├── 📜 pyproject.toml
    └── 📜 README.md
    ```

    

**使用第二种安装方式**
- 在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["TeenStudy"]`


## 机器人配置

- 在nonebot的`.env` 或 `.env.prod`配置文件中设置好超管账号

  ```py
  SUPERUSERS=[""]
  ```
## 使用方式

- 启动nb,等待插件加载数据，加载完毕后登录后台，账号默认为`超管账号`，密码默认为：`admin`,请务必修改配置中的公网访问ip,开放端口（默认为.env中配置的port）

## 功能列表
|            指令            |                 指令格式                  |                             说明                             |
| :------------------------: | :---------------------------------------: | :----------------------------------------------------------: |
|         添加大学习         |     添加大学习`地区`     |     添加大学习湖北 添加大学习     |
|         我的大学习         |                我的大学习                 |                         查询个人信息                         |
|         提交大学习         |                提交大学习 戳一戳Bot                 |                      提交最新一期大学习                      |
|           大学习           |            大学习答案、大学习             |                  获取最新一期青年大学习答案                  |
|          完成截图          |   完成截图、大学习截图、大学习完成截图    |          获取最新一期青年大学习完成截图（带状态栏）          |


## ToDo


- [ ] 增加更多地区支持
- [ ] 优化 Bot


## 更新日志

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