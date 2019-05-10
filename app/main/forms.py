from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, Required
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from flask_uploads import UploadSet

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class VersionForm(FlaskForm):
    file = FileField('上传船舶文件', validators=[DataRequired()])
    submit = SubmitField('Submit')

class single_KeywordForm(FlaskForm):
    keyword = TextAreaField('keyword')
    submit = SubmitField('Submit')

class TitleForm(FlaskForm):
    title = TextAreaField('title')
    submit = SubmitField('Submit')


class KeywordForm(FlaskForm):
    keyword1 = TextAreaField('keyword1', validators=[DataRequired()])
    keyword2 = TextAreaField('keyword2', validators=[DataRequired()])
    keyword3 = TextAreaField('keyword3', validators=[DataRequired()])
    keyword4 = TextAreaField('keyword4', validators=[DataRequired()])
    keyword5 = TextAreaField('keyword5', validators=[DataRequired()])
    submit = SubmitField('Submit')

class modifycategoriesForm(FlaskForm):
    category = SelectField('文档类别', validators=[Required()],
                         choices=[('0', '航标处陆上备件仓库'), ('1', '防污染设备'), ('2', '自动化监测与遥控系统'), ('3', '压缩空气系统'),('4', '舱底水系统'),
                                  ('5', '辅锅炉'),('6', '装卸货设备'),('7', '海水系统'),('8', '电力系统'),('9', '安全与应急设备'),
                                  ('10', '柴油发电原动机'),('11', '生活设施'),('12', '舱体部分'),('13', '安全检查、日常检查'),
                                  ('14', '滑油系统'),('15', '柴油机主机'),('16', '船舶推进与操纵系统'),
                                  ('17', '通讯导航设备'),('18', '燃油设备'),('19', '冷藏空调通风系统'),('20', '维修工具'),
                                  ('21', '淡水系统')])
    submit = SubmitField('Submit')