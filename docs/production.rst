.. production:

###########
Production
###########

This section contains production-specific information and runbook. 

**********************
Installation
**********************

Graveyard is not yet intended to be universally installable, but it plans to be. Current assumptions about production follows. 

Configuration
=============

* Production code is currently copied into a directory (let's call it appdir)
* In appdir's parent directory, ``production.py`` is assumed. That should contain all configuration directives from production's example file, but with correct secrets

* Graveyard currently assumes Sentry account. This should change (we should run our own Sentry instance)
