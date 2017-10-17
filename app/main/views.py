# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash
from app.main import main
from app.main.forms import NameForm
from app import db
from app.models import User
from app.email import send_email


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        app = current_app._get_current_object()
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['IDACHENGZI_ADMIN']:
                send_email(app.config['IDACHENGZI_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())
