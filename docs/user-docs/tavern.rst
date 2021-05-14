######
Tavern
######

Tavern is the discussion core of the server. Users can create arbitrary Tavern Tables and have a discussion there (entries are called Posts).

There are ways to list Tavern Tables:

    * All Tables
    * Only Tables with new post (shows only Tables that user visited previously and contain a new post since the last visit)
    * Bookmarked Tables
    * Only bookmarked Tables with new post


************
Access Model
************

Tables can be either public (all users can visit and view by default) or private (no user can visit or view by default). The default setting can be modified using nick allowlist (allow access even when table is private) or denylist (prevent user from visiting even when table is public).

In both cases, table can be set as read-only: only allowlisted users are able to write posts and noone else.

Owner of the table can designate assistants. Both the owner and the assistants can enter and post, regardless of other settings. In addition, they can both manage Notice Board and Pools.

.. note::
    Implementation Note: There are two models for managing access to ensure compatibility with the old version. See `relevant ticket for further information <https://github.com/dracidoupe/graveyard/issues/237>`_ and read the `Tavern models carefully <https://github.com/dracidoupe/graveyard/blob/master/ddcz/models/used/tavern.py>`_ before changing anything.

    `Migration script is in the repository as well <https://github.com/dracidoupe/graveyard/blob/master/ddcz/management/commands/migratetavernaccess.py>`_.
