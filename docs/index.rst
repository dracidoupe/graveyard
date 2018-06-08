###########################################
Documentation for DraciDoupe.cz development
###########################################

This documentation is intended for developers intersted in joining development of https://www.dracidoupe.cz/ .

It assumes you have local working copy of the site. If not, follow installation guide from `repository's README <https://github.com/dracidoupe/graveyard/>`_. 

.. note::

    *Proč to tady neni česky?*

    Stránka je česky, dokumentace pro uživatele taky. Prográmátoři to ale vždycky měli těžší, protože základní stavební kameny programovacích jazyků jsou anglické, stejně jako mnoho komponent, které jsou zde použity. Původní verze doupěte je česko-anglický mišmaš s českými názvy proměnných apod. Výsledek bohužel není moc dobrý.

    Nová verze má proto jasné rozhraní: veřejně viditelné texty (stránky, popisky stránek, URL adresy atd.) jsou české, ale v kódu je konzistentně použita angličtina. Protože mít programátorskou dokumentaci v češtině by vedlo ke zmatení (jazyků), je pro konzistenci použita angličtina i zde.

    Pochopitelně to má i své nevýhody. Jednou z nich je reprezentace některých čistě českých názvů v angličtině. K tomuto účelu je udržován :ref:`konzistentní slovník <dictionary>`, který se všude používá.

    Pro popis toho co se to tu děje a proč vlastně navštivte sekci :ref:`faq`.

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    faq
    migration
    design
    dictionary



******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
