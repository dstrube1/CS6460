# CS6460-Project

* Originally created here:
* * https://github.gatech.edu/dstrube3/CS6460-Project

Collaborators:
* Sophia Maianh Nguyen - snguyen45
* Rudolfs Praulins - rpraulins3 
* David Strube - dstrube3

# Details

In this project, we are adapting the Diamant / Incan Gold board game for an educational context.

This project uses the following:

* Front-end:
* * HTML
* * CSS
* * JavaScript
* Back-end:
* * Python
* * [Python Flask framework](https://flask.palletsprojects.com)
* * Sqlite3 library for connecting to database
* Database:
* * [SQLite](https://docs.python.org/3/library/sqlite3.html)
* Source control:
* * GitHub
* Hosting
* * PythonAnywhere. Try it out at https://diamant.pythonanywhere.com/

* Python: 3.11.5
* Flask: 2.3.3

To run the Hello World flask project, run the following from Terminal:

* export FLASK_APP=hello.py
* export FLASK_ENV=development
* flask run

On Windows:
* Create a venv:
  * python -m venv env
* Activate env
  * env\Scripts\activate.bat
* Install flask and other packages in the venv:
  * pip install -r .\requirements.txt
* To run flask hello.py:
  * flask --app .\hello.py run

On Mac:
* Create a venv:
  * python -m venv env
* Activate the venv
  * source venv/bin/activate
* Install flask and other packages in the venv:
  * pip install -r ./requirements.txt
* To run flask hello.py:
  * flask --app ./hello.py run

To run the actual application:

* TIP: Before running anything check the contents of your db with DB Browser, so you don't do double work. You can get it here https://sqlitebrowser.org/dl/ 
* IMPORTANT: Make sure to close the db connection after you have viewed the contents in DB Browser (upper right side, red "Close Database" button) as otherwise the database will be locked and you will not be able to enter data via python.

* Make sure the necessary tables are created in the instances/database.db
  * First make sure you have a `instances` directory in your project root. If not, create it.
  * Then run `flask shell` in the cmd
    * when the shell starts, type `from app import db` end press ENTER
    * then type `from models.all_models import *` and press ENTER
    * then type `db.create_all()` and press ENTER
    * At this point a new `database.db` file will be placed in `instances` directory. 
    It will represent the database with all of the newly created tables. 
      * You can double-check this with the previously mentioned DB Browser tool
    * You can exit the shell by typing `exit()` and pressing ENTER
* Once the database is set up and you have your tables, you can run `flask run`
  * If it breaks, maybe you don't have FLASK_APP env var set, so run `set FLASK_APP=app.py` (on Windows)
 or `export FLASK_APP=app.py` on Mac.
  * Then go here in your browser:
    * http://127.0.0.1:5000

To quickly populate database with test data:
* If you want to reset the database and populate it with some testing data, you can do so by passing a python script to the flask shell console.
* An example script can be found in root under `reset_db.py` name.
  * To use the script delete the current `database.db` in instances directory.
    * run the flask server as usual with the `flask run` or `flask run --debug`command.
    * open a new terminal, activate the environment again and run `flask shell < reset.db.py`. This will create the database and populate it with data that's specified in `reset_db.py`


* Useful Queries: 
  * to create your user:
    * insert into user (name, last_name) values ('[replace_this_with_first_name]','[replace_this_with_last_name]');
  * to delete a user:
    * delete from user where id=[id];
