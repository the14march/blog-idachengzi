# -*- coding: utf-8 -*-
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from markdown import markdown

from app import create_app, db
from app.models import User, Role, Post, Category

app = create_app(os.getenv('IDACHENGZI_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def markdown2html(text):
    return markdown(text, ['extra'])


app.add_template_filter(markdown2html)
app.add_template_filter(markdown)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Category=Category)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
