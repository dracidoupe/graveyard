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


Architecture and Setup
======================

We are using:

* Heroku for hosting the main application process
* [AWS RDS](https://aws.amazon.com/rds/) for hosting database
* [AWS S3](https://aws.amazon.com/s3/) for hosting static data and uploaded content

Old version is running on an [EC2 instance](https://aws.amazon.com/ec2/).

User Content Hosting
--------------------

User-uploaded content (user icons, gallery pictures etc.) is hosted on S3 im the `uploady.dracidoupe.cz` budket/domain.

There is no sharing with the old version: content from current production needs to be uploaded/synchronized manually. This needs to happen on a bastion host as the EC2 instance can't talk to Amazon APIs because of obsoleted openssl. Use [aws s3 sync . s3://uploady.dracidoupe.cz/whatever](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html) command.

Static File Hosting
--------------------

Static files (like CSS) are now hosted from within Heroku [using whitenoise](http://whitenoise.evans.io/en/stable/django.html). They [should be migrated to CDN](https://github.com/dracidoupe/graveyard/issues/2).


Error Reporting
---------------

Exceptions are sent to [Sentry](https://sentry.io/welcome/). Sentry is configured to push information about new exceptions into [#production-feed Slack channel](https://dracidoupe.slack.com/archives/C029JA38AAV).

Logs are scanned using [Papertrail](https://www.papertrail.com/) and matching events are send to [#production-feed](https://dracidoupe.slack.com/archives/C029JA38AAV). Alerts currently configured:

* `Warning: OR [WARNING] -("[WARNING] Worker with pid" AND ("was terminated due to signal 19" OR "was terminated due to signal 15")) -"[WARNING] Not Found: /favicon.ico"` (sent every 10 minutes)


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

Test can be run locally, but there is a testing infrastructure run on every push. We are using `Github Actions <https://github.com/dracidoupe/graveyard/actions>`_ for that.

To have the Selenium running properly, we are running the Docker container version of everything and with dedicated ``docker-compose.circle.yml``.

Main web container exposes the application server to the Docker network and the Selenium server uses the generated hostname.
