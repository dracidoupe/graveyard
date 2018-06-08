
.. _migration:

##########################
Migration and Co-Existence
##########################

This section covers design decisions that are driven by how the existing PHP application is structured. All of those should be considered technical debt and eliminated when possible or when the original application is abandoned. 


********
Database
********

Database is the main integration point. The original structure is just inspection of the original data, so do not pay attention to its design. List of consideration follows. 


Database encoding
=================

The original data are misencoded: while stored in field that pretends to be ISO-8859-2/latin2, the data is in fact stored in win1250/cp1250 encoding.

This is transparently handled by ``ddcz.models.magic``; for original tables, :cls:`MisencodedTextField` or :cls:`MisencodedCharField` **must** be used. 

New models respect the connection setting and store data as latin2. Once the old application is shut down, everything should be recoded in a way 21st century people store data (UTF-8). 


User Model
==========

In order to leverage Django's authentication framework (meaning reasonable forward-compatible safety), tricks are needed.

Original data is stored in ``uzivatele`` table. For usability, this is exposed as :cls:`UserProfile` model and `appropriate relation is used <https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#extending-the-existing-user-model>`_. 

.. warning::
    To avoid the need for complete database migration, :cls:`django.auth.models.User` is **not** prepopulated and the migration is to be transparently handled on user login until the old application exist.

    Hence, the application **must** use :cls:`UserProfile` model **only** when displaying user data (i.e. in user stats).


During the initial setup, the arbitrary value of 20000 has been selected for :cls:`django.auth.models.User`'s auto_increment value to distinguish between users from pre-migration to post-migration and to allow old users to retain their IDs.
