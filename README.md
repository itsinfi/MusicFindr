# MusicFindr
MusicFindr is a tool to find music more easily.

What do you need to run the project?
- install python vers. 3.12.1 https://www.python.org/downloads/release/python-3121/
- install flask -> execute "pip install flask" inside the root folder
- install bcrypt -> execute "pip install bcrypt" inside the root folder
- install requests -> execute "pip install requests" inside the root folder

- dependencies can also be installed using the requirements.txt:
- create a venv inside the project root -> execute "python3 -m venv ./"
- use the newly created venv -> execute "source bin/activate"
- pip install requirements -> execute "pip install -r requirements.txt"

- execute "python run.py" inside the root folder
- can be accessed from here: http://localhost:5000/


# Basic Explanation of the code structure

run.py:
- runs the application

.gitignore:
- defines what git does not track when making changes
    .pyc and /__pycache__/ in order to not commit automatically created cache files

templates:
- .html files used for the project
- meta.html is the global header
    - .html files in "wrapper" subfolder include it
    - include "wrapper" .html files when creating a new page

static:
- .css files
    - includes bootstrap
    - includes custom css file "styles.css"
- .js files
    - includes bootstrap
    - includes custom js file "script.js"
- assets
    - used for image assets etc

app/__init__.py:
- defines basic app configurations options
- defines the 404 default route
- defines the error default route
    - triggered if there are runtime exceptions caused from functions inside the page (and only from there!)
    - loads the error dialog page with the error message of the exception

app/components/__init__.py:
- used to define the package for components
- import components from here to other sections of the app
- always define new imports when creating new components

app/components:
- used to define and generate components that are used needed multiple times inside the app (e.g. a search bar)

app/models/__init__.py:
- used to define the package for models
- import models from here to other sections of the app
- always define new imports when creating new models

app/models:
- objects to store data from the database (e.g. Users)
- represent the entity classes

app/services/__init__.py:
- used to define the package for services
- import services from here to other sections of the app
- always define new imports when creating new services

app/services:
- each service includes a service class and a service error class
    - service class includes all functions needed to manipulate/CRUD the models (e.g. UserService.createUser())
    - service error class derives from Python's Exception class and is put out for custom exceptions
        => so make sure to always consider if you need appropiate error handling (functions are described accordingly)

app/views/__init__.py:
- defines page routes used for the app in @blueprint and executes functions to load the view pages accordingly
    - is imported into app/__init__.py to define the routing blueprint of the app
- used to define the package for views
- import views from here to other sections of the app
- always define new imports when creating new views

app/views:
- every view includes a function to render the page
- define pages and basic ui logic here


# Currently testable stuff (05.01.2024)

- crud testing cases (without db connection) -> app/__init__.py
- 404 handling -> (just open any undefined route)
- open profile page or dialog if not found (just for testing, change it anytime :)) -> "/profile/<uid>"
- open start page (just for testing, feel free to change the design and logic :)) -> "/"
