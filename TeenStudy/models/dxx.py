from tortoise import fields
from tortoise.models import Model


class Answer(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    code: str = fields.TextField()
    """大学习期数标识"""
    catalogue: str = fields.TextField()
    """大学习期数名称"""
    time: int = fields.IntField()
    """更新时间戳"""
    url: str = fields.TextField()
    """大学习网址"""
    end_url: str = fields.TextField()
    """完成截图网址"""
    answer: str = fields.TextField()
    """答案"""
    cover: bytes = fields.BinaryField()
    """大学习完成截图"""

    class Meta:
        table = 'Answer'
        table_description = '大学习答案'
        indexes = ('time',)


class Area(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField(null=True)
    """更新时间戳"""
    area: str = fields.TextField()
    """地区"""
    host: str = fields.TextField()
    """请求host"""
    referer: str = fields.TextField(null=True)
    """请求Referer"""
    origin: str = fields.TextField(null=True)
    """请求Origin"""
    url: str = fields.TextField()
    """检查更新url"""
    status: bool = fields.BooleanField(default=True, null=True)
    """是否为最新一期"""
    catalogue: str = fields.TextField(null=True)
    """大学习期数名称"""

    class Meta:
        table = 'Area'
        table_description = '地区列表'
        indexes = ('time',)


class Resource(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """创建时间"""
    name: str = fields.TextField()
    """资源名称"""
    type: str = fields.TextField()
    """资源类型"""
    url: str = fields.TextField()
    """文件下载链接"""
    file: bytes = fields.BinaryField(null=True)
    """资源内容"""
    size: str = fields.TextField(null=True)
    """文件大小"""

    class Meta:
        table = 'Resource'
        table_description = '大学习插件资源'
        indexes = ('time',)


class PushList(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """创建时间"""
    self_id: int = fields.IntField()
    """机器人Id"""
    user_id: int = fields.IntField()
    """添加人员"""
    group_id: int = fields.IntField()
    """通知群聊"""
    status: bool = fields.BooleanField(default=True)
    """通知状态"""

    class Meta:
        table = 'PushList'
        table_description = '通知群列表'
        indexes = ('time',)
