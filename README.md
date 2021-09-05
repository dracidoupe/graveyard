# Graveyard: Place for Dead (and Undead)

[![Documentation Status](https://readthedocs.org/projects/ddcz/badge/?version=latest)](https://ddcz.readthedocs.io/?badge=latest)

Graveyard is an attempt at open-source reimplementation of [DraciDoupe.cz](https://www.dracidoupe.cz/) (referred to as DDCZ in this text).

Developer's documentation is [at Read the Docs](https://ddcz.readthedocs.io/en/latest/).

Production is running at http://nove.dracidoupe.cz/ . But be warned, we are heading for the root domain soon!

## Contributions

Contributions are welcome provided you agree your work will be shared under the same license as Graveyard (MIT). Please use [black](https://pypi.org/project/black/) for code formatting.

If you don't know where to start, take a look [at the roadmap](https://github.com/dracidoupe/graveyard/milestones) or ask Almad on [development Slack](https://dracidoupe.slack.com/messages/C7F0YCTFU) or in Pošta on [DraciDoupe.cz](https://www.dracidoupe.cz/).

*Please install [EditorConfig](https://editorconfig.org/) support for your editor* ([plugin for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig), [plugin for PyCharm/WebStorm/IDEAJ](https://plugins.jetbrains.com/plugin/7294-editorconfig))

## Installation

You can run Graveyard either directly on your machine or inside [Docker](https://www.docker.com/). Arm64 systems (like M1 Mac) are supported.

Installing and running Graveyard directly is faster (on some systems) and removes one lever of indirection, but it makes the setup more complicated.

Running in Docker requires familiarity with it, but it makes setup easier and guarantees consistency with the testing environment (and hopefully in the future, production environment as well).

In both cases, first clone this repository and run all commands in its directory.

### Installing in Docker

Requirements:

* You have [Docker CE installed](https://www.docker.com/community-edition)
* You have [installed docker-compose](https://docs.docker.com/compose/install/)

* Createyour own copy of [docker-compose configuration](docker-compose.example.yml)

  * `cp docker-compose.example.yml docker-compose.yml`
  * You can locally change your port if you do not want to run it at 8000

* Create your own copy of [local configuration](graveyard/settings/local.example.py)

  * `cp graveyard/settings/local.example.py graveyard/settings/local.py`

Verify you have everything ready by running the test suite:

* `docker-compose run web python3 manage.py test`

If you see output like this:

```
(graveyard-venv) almad@zeruel:~/projects/graveyard$ docker-compose run web python3 manage.py test
Starting graveyard_db_1 ... done
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
Destroying test database for alias 'default'...
(graveyard-venv) almad@zeruel:~/projects/graveyard$

```

You are all set. Afterwards, install database schema by running

*  `docker-compose run web python3 manage.py migrate`

and load data about pages

*  `docker-compose run web python3 manage.py loaddata pages`

You are done! Now you can just run the project and develop using

*  `docker-compose start`

Verify your application works and open `http://localhost:8000` (`localhost` may be a different host if you are not working on linux). If so, create yourself a superuser.

For all commands in the manual that ask for `python manage.py command`, run `docker-compose run web python3 manage.py command` instead

### Installing on your machine

Graveyard is currently written in [Django](https://www.djangoproject.com/). Requirements to develop it:

* You have working Python 3 installation on your machine
* You have working MySQL installation on your machine

To use the project, clone this repository, enter its directory with `cd graveyard` and:

* Create a virtual environment: `python3 -m venv gvenv`
   * If this fails and you are on Ubuntu, you may need to `sudo apt-get update && sudo apt-get install python3-pip && sudo pip3 install virtualenv`
* Enter it (on Mac OS X or Linux): `source gvenv/bin/activate`
* Install dependencies within the `pip install -r requirements.txt`
* Copy settings template: `cp graveyard/settings/local.example.py graveyard/settings/local.py`
* Edit the settings above, especially enter credentials to your local MySQL ([see Stack Overflow](https://stackoverflow.com/questions/1720244/create-new-user-in-mysql-and-give-it-full-access-to-one-database) on how to do that)
  * When creating database, for compatibility, use latin2 as default charset: `CREATE DATABASE dracidoupe_cz DEFAULT CHARACTER SET latin2;`
* Verify you have correct installation and run tests with `python manage.py test`. You should see output like this:

```
(graveyard-venv) almad@zeruel:~/projects/graveyard$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 0.031s

OK
Destroying test database for alias 'default'...
(graveyard-venv) almad@zeruel:~/projects/graveyard$
```
  * If you see error like `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home`, you have to go to [the linked page](https://sites.google.com/a/chromium.org/chromedriver/home) and download the chromedriver to your computer. Place it somewhere in `$PATH` like `/usr/local/bin`
* Create the database schema: `python manage.py migrate`
* Load data about pages to see what's on production: `python manage.py loaddata pages`
* Run the thing! `python manage.py runserver`
* Observe if you have contact at `http://localhost:8000`

### Installing on Windows

Follow the list above, except:

* It is strongly recommended to use Python 3.7 and MySQL 8, otherwise you'll have to compile mysqlclient manually
* Activate virtualenv using `gvenv\Scripts\activate` instaed of `source gvenv/bin/activate`


## After Installation

* Load initial version of editorial articles: `python manage.py loaddata editorarticles`
* Create a superuser for yourself: `python manage.py createsuperuser`
* Look around the administration interface at `http://localhost:8000/admin/`


#### Installation issues

*  Installation failes with "mysql_config not found"

If you get something like this:

```
    File "/tmp/pip-install-wfhe9zue/mysqlclient/setup_posix.py", line 29, in mysql_config
        raise EnvironmentError("%s not found" % (_mysql_config_path,))
    OSError: mysql_config not found
```

you may be using MariaDB fork of MySQL that the Python client is not equipped to talk to, installation-wise. You need to manually symlink the appropriate command:

`ln -s /usr/bin/mariadb_config /usr/bin/mysql_config`

If even `mysql_config` is not there, you have to install development headers for the database. That's `apt-get install libmariadbclient-dev` on Debian.

* `error: invalid command 'bdist_wheel'`

Old setuptools: `pip install setuptools -U`

## Setup

### Create user account

Use ``python manage.py registeruser`` command, see ``manage.py registeruser --help`` for parameters.

### Debugging with Django Debug Toolbar

* `pip install django-debug-toolbar==2.2.1`
* Add to local.py:

```
from .base import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(
    0,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

INTERNAL_IPS = ["127.0.0.1", "::1"]
```
