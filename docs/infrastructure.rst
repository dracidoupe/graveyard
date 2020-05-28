.. infrastructure:
.. infra:

###############
Infrastructure
###############

.. production:

***********
Production
***********

This section contains production-specific information and runbook. 


Installation
============

Graveyard is not yet intended to be universally installable, but it plans to be. Current assumptions about production follows. 

Configuration
-------------

The application assumes following environment variables to be set in production (see settings directory for more info):

* DJANGO_SECRET_KEY
* SENTRY_DSN
* DB_NAME
* DB_USERNAME
* DB_PASSWORD
* DB_HOST
* DB_PORT

THE FOLLOWING IS LIKELY DEPRECATED:
* Production code is currently copied into a directory (let's call it appdir)
* In appdir's parent directory, ``production.py`` is assumed. That should contain all configuration directives from production's example file, but with correct secrets

* Graveyard currently assumes Sentry account. This should change (we should run our own Sentry instance)



.. testing-infra:

*******
Testing
*******

For automated testing, we're using standard Django tests suite. In case of end-to-end browser tests, Selenium is used.

All Selenium tests are in the ``ddcz/tests/test_ui`` directory.

Test can be run locally, but there is a testing infrastructure run on every push. We are using CircleCI for that.

To have the Selenium running properly, we are running the Docker container version of everything and with dedicated ``docker-compose.circle.yml``.

Main web container exposes the application server to the Docker network and the Selenium server uses the generated hostname.
