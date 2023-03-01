from tortoise import fields
from tortoise.models import Model


class User(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """创建时间戳"""
    user_id: int = fields.IntField()
    """用户ID"""
    password: str = fields.TextField(null=True)
    """登录密码，用于登录web端"""
    group_id: int = fields.IntField(null=True)
    """通知群号"""
    name: str = fields.TextField()
    """姓名"""
    gender: str = fields.TextField(null=True)
    """性别"""
    mobile: str = fields.TextField(null=True)
    """手机号"""
    area: str = fields.TextField()
    """地区"""
    leader: int = fields.IntField(null=True)
    """团支书ID"""
    openid: str = fields.TextField(null=True)
    """微信认证ID"""
    dxx_id: str = fields.TextField(null=True)
    """大学习用户id,nid或uid"""
    university_type: str = fields.TextField(null=True)
    """学校类型"""
    university_id: str = fields.TextField(null=True)
    """学校id"""
    university: str = fields.TextField()
    """学校名称"""
    college_id: str = fields.TextField(null=True)
    """学院id"""
    college: str = fields.TextField()
    """学院名称"""
    organization_id: str = fields.TextField(null=True)
    """团支部id"""
    organization: str = fields.TextField(null=True)
    """团支部名称"""
    token: str = fields.TextField(null=True)
    """提交需要的token"""
    cookie: str = fields.TextField(null=True)
    """提交要用的cookie"""
    catalogue: str = fields.TextField(null=True)
    """提交期数"""
    commit_time: int = fields.IntField(null=True)
    """提交时间"""

    class Meta:
        table = 'User'
        table_description = '用户列表'
        indexes = ('time', 'user_id',)


class Commit(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """提交时间"""
    user_id: int = fields.IntField()
    """用户ID"""
    name: str = fields.TextField()
    """提交姓名"""
    area: str = fields.TextField()
    """提交地区"""
    university: str = fields.TextField()
    """学校名称"""
    college: str = fields.TextField()
    """学院名称"""
    organization: str = fields.TextField(null=True)
    """团支部名称"""
    catalogue: str = fields.TextField(null=True)
    """提交期数"""
    status: bool = fields.BooleanField(default=False)
    """提交状态"""

    class Meta:
        table = 'Commit'
        table_description = '提交记录'
        indexes = ('time', 'user_id',)


class Admin(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """token失效时间"""
    user_id: int = fields.IntField()
    """用户ID"""
    password: str = fields.TextField()
    """登录密码"""
    key: str = fields.TextField()
    """哈希秘钥"""
    algorithm: str = fields.TextField()
    """加密算法"""
    ip: str = fields.TextField(null=True, default="127.0.0.1")
    """"""

    class Meta:
        table = 'Admin'
        table_description = '管理员'


class AddUser(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """申请时间"""
    user_id: int = fields.IntField()
    """用户ID"""
    group_id: int = fields.IntField()
    """申请群号"""
    area: str = fields.TextField()
    """申请地区"""
    message_id: int = fields.IntField()
    """申请消息ID"""
    status: str = fields.TextField(default="未通过")
    """状态"""

    class Meta:
        table = 'AddUser'
        table_description = '申请列表'
