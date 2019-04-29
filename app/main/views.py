import os

from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, send_from_directory
from flask_login import login_required, current_user
from flask_uploads import UploadNotAllowed

from nlp.process import nlp
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, \
    VersionForm, KeywordForm, single_KeywordForm, TitleForm
from .. import db, files
from ..models import Permission, Role, User, File
from ..decorators import admin_required, permission_required



@main.route('/', methods=['GET', 'POST'])
def index():
    form = VersionForm()
    if current_user.can(Permission.WRITE) and  form.validate_on_submit():
        try:
            filename = files.save(form.file.data)
            path = str(str(current_app.config['UPLOADED_FILES_DEST']) + '\\' + filename)
            test = nlp(path)
            keywords = test.keyword_extraction()
            seg = test.cut()
            keyword1=keywords[0][0]
            keyword2=keywords[1][0]
            keyword3=keywords[2][0]
            keyword4=keywords[3][0]
            keyword5=keywords[4][0]
            sum=keywords[0][1]+keywords[1][1]+keywords[2][1]+keywords[3][1]+keywords[4][1]
            keyword_weight1=keywords[0][1]/sum
            keyword_weight2=keywords[1][1]/sum
            keyword_weight3=keywords[2][1]/sum
            keyword_weight4=keywords[3][1]/sum
            keyword_weight5=keywords[4][1]/sum
            file = File(file_name=filename,
                        keyword1=keyword1,
                        keyword2=keyword2,
                        keyword3=keyword3,
                        keyword4=keyword4,
                        keyword5=keyword5,
                        keyword_weight1=keyword_weight1,
                        keyword_weight2=keyword_weight2,
                        keyword_weight3=keyword_weight3,
                        keyword_weight4=keyword_weight4,
                        keyword_weight5=keyword_weight5,
                        seg="  ".join(seg),
                        author=current_user._get_current_object())
            flash('上传文档成功！')
            db.session.add(file)
            db.session.commit()

            # file_url = files.url(filename)
            print(filename)
            # print(file_url)
        except UploadNotAllowed as e:
            print(e)
            flash('失败，温馨提示：文件名称不可以含中文！')
        else:
            return redirect(url_for('.index'))

    file = request.args.get('file', 1, type=int)
    show_followed = False
    if show_followed:
        query = current_user.followed_posts
    else:
        query = File.query
    pagination = query.order_by(File.timestamp.desc()).paginate(
        file, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    filess = pagination.items
    return render_template('index.html', form=form,
                           show_followed=show_followed, pagination=pagination,files=filess)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    file = request.args.get('file', 1, type=int)
    pagination = user.files.order_by(File.timestamp.desc()).paginate(
        file, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    files = pagination.items
    return render_template('user.html', user=user, files=files,
                           pagination=pagination)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)



@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    file = File.query.get_or_404(id)
    if current_user != file.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = KeywordForm()
    if form.validate_on_submit():
        file.keyword1 = form.keyword1.data
        file.keyword2 = form.keyword2.data
        file.keyword3 = form.keyword3.data
        file.keyword4 = form.keyword4.data
        file.keyword5 = form.keyword5.data
        db.session.add(file)
        db.session.commit()
        flash('关键字修改成功！')
        return redirect(url_for('.index', id=file.id))
    form.keyword1.data = file.keyword1
    form.keyword2.data = file.keyword2
    form.keyword3.data = file.keyword3
    form.keyword4.data = file.keyword4
    form.keyword5.data = file.keyword5
    return render_template('edit_file_keywords.html', form=form)



@main.route('/keyword_search', methods=['GET', 'POST'])
@login_required
def keyword_search():
    form = single_KeywordForm()
    if form.validate_on_submit():
        keyword=form.keyword.data
        file_list = File.query.all()
        files = list()
        for file in file_list:
            if (file.keyword1 == keyword or file.keyword2 == keyword or file.keyword3 == keyword or file.keyword4 == keyword or file.keyword5 == keyword):
                files.append(file.id)
        # print(files[0])
        if(len(files)==0):
            flash('不存在此关键字的文档！')
            return redirect(url_for('.keyword_search'))
        flash('查找成功！')
        return redirect(url_for('.file', id = files[0]))
    return render_template('keyword_search.html', form=form)

@main.route('/title_search', methods=['GET', 'POST'])
@login_required
def title_search():
    form = TitleForm()
    if form.validate_on_submit():
        title = form.title.data
        file_list = File.query.all()
        files = list()
        for file in file_list:
            filename = os.path.splitext(file.file_name)
            if (filename[0]==title):
                files.append(file.id)
        # print(files[0])
        if(len(files)==0):
            flash('不存在此标题的文档！')
            return redirect(url_for('.title_search'))
        flash('查找成功！')
        return redirect(url_for('.file', id = files[0]))
    return render_template('title_search.html', form=form)

@main.route('/file/<int:id>', methods=['GET', 'POST'])
@login_required
def file(id):
    file = File.query.get_or_404(id)
    return render_template('file.html', file=file)


@main.route('/downloads_file/<int:id>', methods=['GET', 'POST'])
@login_required
def downloads_file(id):
    file = File.query.get_or_404(id)
    directory = current_app.config['UPLOADED_FILES_DEST']
    filename = file.file_name
    return send_from_directory(directory, filename, as_attachment=True)



@main.route('/tree_search', methods=['GET', 'POST'])
@login_required
def tree_search():
    return render_template('tree_search.html')