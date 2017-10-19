# -*- coding: utf-8 -*-
from flask import render_template, abort, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user

from app.decorators import admin_required
from app.main import main
from app.main.forms import EditProfileForm, EditProfileAdminForm, PostForm
from app import db
from app.models import User, Role, Permission, Post, Category


@main.route('/')
def index():
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['IDACHENGZI_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, categories=categories)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post_detail(id):
    categories = Category.query.all()
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post, categories=categories)


@main.route('/category/<string:category_id>')
def posts_under_category(category_id):
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category_id=category_id).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['IDACHENGZI_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('posts_under_category.html', posts=posts, pagination=pagination, categories=categories)


@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    categories = Category.query.all()
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.summary = form.summary.data
        post.title = form.title.data
        post.category = Category.query.get(form.category.data)
        db.session.add(post)
        flash('This post has been updated.')
        return redirect(url_for('main.post_detail', id=post.id))
    form.title.data = post.title
    form.category.data = post.category
    form.body.data = post.body
    form.summary.data = post.summary
    return render_template('edit_post.html', form=form, categories=categories)


@main.route('/delete-post/<int:id>')
@login_required
def delete_post(id):
    pass


@main.route('/edit-new-post', methods=['GET', 'POST'])
@login_required
def edit_new_post():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    summary=form.summary.data,
                    body=form.body.data,
                    author=current_user._get_current_object(),
                    category=Category.query.get(form.category.data))
        db.session.add(post)
        return redirect(url_for('main.post_detail', id=Post.query.filter_by(title=post.title).first().id))
    return render_template('edit_new_post.html', form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@main.route('/about-me')
def about_me():
    return render_template('about_me.html')


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
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
        flash('The profile has been updated.')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
