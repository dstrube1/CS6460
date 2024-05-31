from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

my_app = Flask(__name__)
my_app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'instances/database.db')
my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

my_app.config['WTF_CSRF_ENABLED'] = False

my_app.config['SECRET_KEY'] = 'super_secret_string_for_sessions_that_should_be_changed_to_env_var_when_live'
my_app.config['SESSION_TYPE'] = 'filesystem'

# Initialize the SQLAlchemy extension
db = SQLAlchemy(my_app)

from routes.routes import * # noqa

if __name__ == '__main__':
    my_app.run(debug=True)