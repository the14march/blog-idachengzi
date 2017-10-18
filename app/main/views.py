# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, abort, session, redirect, url_for, current_app, flash
from flask_login import login_required, current_user

from app.decorators import admin_required
from app.main import main
from app.main.forms import EditProfileForm, EditProfileAdminForm, PostForm
from app import db
from app.models import User, Role, Permission, Post, Category
from app.email import send_email


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object(),
                    category=Category.query.get(form.category.data))
        db.session.add(post)
        return redirect(url_for('main.index', form=form, posts=posts))
    return render_template('index.html', form=form, posts=posts)


@main.route('/edit-post', methods=['GET', 'POST'])
def edit_post():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object(),
                    category=Category.query.get(form.category.data))
        db.session.add(post)
        return render_template('index.html', post=[post])
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)


@main.route('/test-posts')
def test_posts():
    return render_template('tem_posts.html')


@main.route('/about-me')
def about_me():
    return render_template('about_me.html')


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
