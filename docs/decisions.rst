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
