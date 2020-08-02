from flask_script import Manager
from flask_migrate import MigrateCommand , Migrate

from apps import app , db
from apps.model import User , Role

migrate = Migrate(app , db)
manager = Manager(app)
manager.add_command('db' , MigrateCommand)

if __name__ == "__main__":
    manager.run()

"""
python ./initDB.py db init
python ./initDB.py db migrate
python ./initDB.py db upgrade
"""
