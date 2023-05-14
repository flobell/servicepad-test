This project has two (2) parts:

# PART 1: ServicePad Logic Test

There are three (3) files in this project as part of the logic test

* `logic_test_1.py`
* `logic_test_2.py`
* `logic_test_3.py`

You can run them with the command `python logic_test_#.py` after making the installation part, also they have unit tests at `/tests` but you have to do the installation part to run them.

# PART 2: ServicePad Backend Test

The folder `/app` contains the definition of the API as part of the backend test

### Requirements

**[python=3.9.6](https://www.python.org/downloads/)**

**[postgresql=13.4](https://www.postgresql.org/download/)**

**[pyenv](https://github.com/pyenv/pyenv#installation)**

# Installation

The following steps to start web server and swagger for the `ServicePad Backend Test` part:

* Clone the repository.
* Install Python version 3.9.6 with `pyenv install 3.9.6`. The version may vary according to the requirements, check the version in the Pipfile.
* Set the Python version in the working directory with `pyenv local version`.
* Inside the working directory, install `pipenv` with the command `pip install pipenv`.
* To create the virtual environment and install the required packages, use the command `pipenv install` within the working directory. For pipenv, virtual environments are defined by the directory. Then install the development packages with `pipenv install --dev`, it is mandatory to install the --dev packages.
* To activate the virtual environment, run `pipenv shell`.
* After activating the virtual environment, the installed packages will be available.

### Set configurations

* There is an example configuration file `/config/config.yaml.example`
* Then copy it on the same folder and rename it like `/config/config.yaml`.
* Set the configuration variable `SQLALCHEMY_DATABASE_URI` in the file `/config/config.yaml` with the PostgreSQL database URI standard. Example: `postgresql://user:password@host:port/dbname`.
* Then set the enviroment variable depending on your system to make know the application where is the configuration file.

On Linux:
```
export APP_CONFIG=$(pwd)/config/config.yaml
```

On Windows:
```
set APP_CONFIG=%cd%/config/config.yaml
```

### Initialize `Database tables`

To set up the database locally, follow these steps:

* Execute the command `app db create-all` to create the model tables in the database.
* You can use `app db drop-all` to delete al database table (BE CAUTIOUS!)

### Unit testing

All unit tests are run with `pytest` in the foldes `/tests`, to run them just execute the command pytest at console.

* IMPORTANT: The unit tests of the backend test part does create and delete the database using `fixtures` so be careful setting
the `SQLALCHEMY_DATABASE_URI` as it can delete all tables of the database setted

### Initialize `local web server`

* Execute the command `app web run` or `python main.py`.

# Screenshots

Here are some screenshots of the project:

![logic_test_1](screenshots/image1.png)
![logic_test_2](screenshots/image2.png)
![logic_test_3](screenshots/image3.png)
![backend_test](screenshots/image4.png)
![database](screenshots/image5.png)
![unit_tests](screenshots/image6.png)