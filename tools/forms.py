# -*- coding: utf-8 -*-
from wtforms import Form  # 导入父类
from wtforms.fields import StringField, PasswordField, IntegerField  # 导入字段
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError  # 导入验证器
from model.CRUD import CRUD

# 定义注册表单验证器
class RegistForm(Form):
    name = StringField(
        "昵称",
        validators=[
            DataRequired('昵称不能为空！')
        ]
    )
    pwd = PasswordField(
        "密码",
        validators=[
            DataRequired("密码不能为空！")
        ]
    )
    repwd = PasswordField(
        "确认密码",
        validators=[
            DataRequired("确认密码不能为空！"),
            EqualTo('pwd', message="两次输入密码不一致！")
        ]
    )
    email = StringField(
        "邮箱",
        validators=[
            DataRequired("邮箱不能为空！"),
            Email("邮箱格式不正确！")
        ]
    )
    phone = StringField(
        "手机",
        validators=[
            DataRequired("手机不能为空！"),
            Regexp("1[345789]\\d{9}", message="手机格式不正确！")
        ]
    )

    # 自定义验证昵称
    def validate_name(self, field):
        data = CRUD.user_unique(field.data)
        if data:
            raise ValidationError("昵称已经存在！")

    # 自定义验证邮箱
    def validate_email(self, field):
        data = CRUD.user_unique(field.data, 2)
        if data:
            raise ValidationError("邮箱已经存在！")

    # 自定义验证手机
    def validate_phone(self, field):
        data = CRUD.user_unique(field.data, 3)
        if data:
            raise ValidationError("手机已经存在！")


# 定义登录表单验证模型
class LoginForm(Form):
    name = StringField(
        "账号",
        validators=[
            DataRequired("账号不能为空！")
        ]
    )

    pwd = PasswordField(
        "密码",
        validators=[
            DataRequired("密码不能为空！")
        ]
    )

    def validate_name(self, field):
        data = CRUD.user_unique(field.data)
        if not data:
            raise ValidationError("账号不存在！")

    def validate_pwd(self, field):
        data = CRUD.check_login(self.name.data, field.data)
        if not data:
            raise ValidationError("密码不正确！")

# 定义个人资料编辑验证表单模型
class UserProfileEditForm(Form):
    id = IntegerField(
        "编号",
        validators=[
            DataRequired("编号不能为空！")
        ]
    )
    role = StringField(
        "身份",
        validators=[
            DataRequired("身份不能为空！")
        ]
    )
    name = StringField(
        "昵称",
        validators=[
            DataRequired("昵称不能为空！")
        ]
    )
    email = StringField(
        "邮箱",
        validators=[
            DataRequired("邮箱不能为空！"),
            Email("邮箱格式不正确！")
        ]
    )
    phone = StringField(
        "手机",
        validators=[
            DataRequired("手机不能为空！"),
            Regexp("1[345789]\\d{9}", message="手机格式不正确！")
        ]
    )
    face = StringField(
        "头像",
        validators=[
            DataRequired("头像不能为空！")
        ]
    )
    info = StringField(
        "个性签名",
        validators=[
            DataRequired("个性签名不能为空！")
        ]
    )
    sex = IntegerField(
        "性别",
        validators=[
            DataRequired("性别不能为空！")
        ]
    )
    xingzuo = IntegerField(
        "星座",
        validators=[
            DataRequired("星座不能为空！")
        ]
    )


class StreamBuildForm(Form):

    def validate_url(self, field):
        if not field.data.startswith("http://"):
            raise ValidationError("推流地址只支持http")
    
    title = StringField(
        "直播标题",
        validators=[
            DataRequired("直播标题不能为空！")
        ]
    )

    url = StringField(
        "推流地址",
        validators=[
            DataRequired("推流地址不能为空！")
        ]
    )

    userid = StringField(
        "创建者名称",
        validators=[
            DataRequired("创建者名称不能为空！")
        ]
    )


class courseBuildForm(Form):
    
    
    title = StringField(
        "课程标题",
        validators=[
            DataRequired("课程标题不能为空！")
        ]
    )

    face = StringField(
        "头像",
        validators=[
            DataRequired("头像不能为空！")
        ]
    )

    content = StringField(
        "课程介绍",
        validators=[
            DataRequired("课程介绍不能为空！")
        ]
    )

    userid = StringField(
        "教师",
        validators=[
            DataRequired("课程介绍不能为空！")
        ]
    )