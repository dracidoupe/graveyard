############
Decision Log
############

We capture major decisions about the development here. Similar to `architecture decision log <https://adr.github.io/>`_, it helps us remember important context and gives us more confidence when revisiting decisions in the future.

****
2021
****

September
=========

* There is small enough active users that we'll be using Mailgun even for batch sending
* Batch sending is thus decoupled and send using database as a queue as a starter


June
====

* For URLs, we prefer longer and more expressive URLs that explain the particular resource or resource list. Hence, displaying posts in Tavern is `/tavern/table/id/posts/` as opposed to just `/tavern/table/id/`, especially since we have `/tavern/table/id/notice-board/` etc. In the same fashion, root url `/` redirects to `/news/` instead of being served directly since we may (and actually want) to redo the landing page.

* Models missing integer foreign key should have it added (as opposed to working on the character foreign keys). Pattern:
    * Add nullable column
    * Write ``migrate$modelname`` management command
    * Run it upon deploy
    * Write it to the `data migration ticket <https://github.com/dracidoupe/graveyard/issues/128>`_ for final migration when old version is shut down

* For comments and tavern posts, we are using the same endpoint and POST action. Action is designated by a POST attribute. "Correctly", this would be done better by using different HTTP method, unfortunately `Mike's proposal is not implemented <http://amundsen.com/examples/put-delete-forms/>`_

* All attributes for all models are now in English and in accordance with the :ref:`dictionary`. Czech names should be hidden under ``db_column`` attributes and under ``Enum``s

