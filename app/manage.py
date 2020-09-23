from flask_script import Manager
from flask_migrate import MigrateCommand

from application import create_app

application = create_app()
manager = Manager(application)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
