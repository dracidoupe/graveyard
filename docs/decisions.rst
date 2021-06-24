############
Decision Log
############

We capture major decisions about the development here. Similar to `architecture decision log <https://adr.github.io/>`_, it helps us remember important context and gives us more confidence when revisiting decisions in the future.

****
2021
****

June
====

* Models missing integer foreign key should have it added (as opposed to working on the character foreign keys). Pattern:
    * Add nullable column
    * Write ``migrate$modelname`` management command
    * Run it upon deploy
    * Write it to the `data migration ticket <https://github.com/dracidoupe/graveyard/issues/128>`_ for final migration when old version is shut down

* For comments and tavern posts, we are using the same endpoint and POST action. Action is designated by a POST attribute. "Correctly", this would be done better by using different HTTP method, unfortunately `Mike's proposal is not implemented <http://amundsen.com/examples/put-delete-forms/>`_

* All attributes for all models are now in English and in accordance with the :ref:`dictionary`. Czech names should be hidden under ``db_column`` attributes and under ``Enum``s

