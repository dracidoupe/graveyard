
.. _migration:

##########################
Migration and Co-Existence
##########################

This section covers design decisions that are driven by how the existing PHP application is structured. All of those should be considered technical debt and eliminated when possible or when the original application is abandoned. 


********
Database
********

Database is the main integration point. The original structure is just inspection of the original data, so do not pay attention to its design. List of consideration follows. 


.. _db-encoding:

Database encoding
=================

The original data are misencoded: while stored in field that pretends to be ISO-8859-2/latin2, the data is in fact stored in win1250/cp1250 encoding.

This is transparently handled by ``ddcz.models.magic``; for original tables, `MisencodedTextField` or `MisencodedCharField` **must** be used. 

New models respect the connection setting and store data as latin2. Once the old application is shut down, everything should be recoded in a way 21st century people store data (UTF-8). 


.. _db-migration:

Django's (database model) migration strategy
============================================

Django provides `a reasonable framework for handling migration <https://docs.djangoproject.com/en/2.0/topics/migrations/>`_ that is used in our application. Initial structure has been done using :cmd:`inspectdb`, which automatically creates unmanaged models and has been placed into :mod:`ddcz.models.legacy`.

When model/table is incorporated into application with all bells and whistles required for it to actually run and be read- and write-able, it's moved into :mod:`ddcz.models.used`.

There is one problem: unmanaged models are not created during the normal setup, hence tests are failing and application is unusable for anyone without access to database structured backup. To work around it, there is a hack:

* In the initial migration, the default managed is set depending on `SETTINGS.IS_DATABASE_SEEDED`. This *has* to be set depending on whether database is restored from original data
* This means that migration from unmanaged to managed model will work correctly with seeded database and will be "noop" migration for seeded database
* 


.. _user-model-migration:

User Model
==========

In order to leverage Django's authentication framework (meaning reasonable forward-compatible safety), tricks are needed.

Original data is stored in ``uzivatele`` table. For usability, this is exposed as `UserProfile` model and `appropriate relation is used <https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#extending-the-existing-user-model>`_. 

.. warning::
    Always use `ddcz.users.create_user` for creating users, instead of `django.auth.models.User.create_user`


.. warning::
    To avoid the need for complete database migration, `django.auth.models.User` is **not** prepopulated and the migration is to be transparently handled on user login until the old application exist.

    Hence, the application **must** use `UserProfile` model **only** when displaying user data (i.e. in user stats).


During the initial setup, the arbitrary value of 20000 has been selected for `django.auth.models.User`'s auto_increment value to distinguish between users from pre-migration to post-migration and to allow old users to retain their IDs.
