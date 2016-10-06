#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from flask.ext.script import Server, Manager
import settings
from outhook import app

app.config.from_object(settings)
manager = Manager(app)
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
