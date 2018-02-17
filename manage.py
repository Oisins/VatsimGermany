# -*- coding: utf-8 -*-
import os
from app import create_app, db
from flask_script import Manager
from app.utils import register_processors
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv("FLASK_ENV") or "default")

register_processors(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


if __name__ == "__main__":
    manager.run()
