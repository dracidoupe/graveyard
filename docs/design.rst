******
Design 
******

Technically, DDCZ is kinda CMS with simple workflow meeting very simple social network. This section covers most of the legacy design and lists its pages for reference. 

Considerations
==============

* MySQL is the database of choice and integration layer between old and new. For all its awfulness, this will stay. While database pretends to be in latin2 (and even the site's connectin to it is explicitly set to latin2), the actual content is stored in cp1250. This is a major fuckup that will render most default tools unusable with the database. "Proper" Python way to present a record is to connect using `latin2` encoding and then convert individual records using `record.encode("latin2").decode("cp1250").encode("utf-8")`
* Page load speed is a concern. Everybody loves fast pages
* General speed and scalability is not a concern. Whole dataset can fit into modern memory. Please do not optimise on bare metal and single node
* Maintenance cost is a concern. The less it costs to run, the more likely it will stay with us
* Stability of an ecosystem is a concern. This site is going to run for another decade. Which technologies do you think are going to stay for so long, preferably with no need for upgrade? That site, this has been always my playground for failed experiments. Judge me

*******************
Pages & Data Design
*******************

Oh boy, this thing has a *lot* of dubiously designed data underneath. However, from a high-level perspective, they would be normalised as follows.

There is a Czech/English tension in the naming. Decision TBD. 

Public pages
============

* Common attributes for all "creation" pages: Author, External source (for *very* legacy articles from bootstrapped version of the page), rating (AVG of all votes, expressed in starts, 0-5) and read and print counters
* Creation pages: "Articles", containing annotation and text
* Creation pages: System extensions (roughly dozen of them), containing arbitrary amount of additional attributes, rendered in a table-like structure
* Creation pages: Gallery and Photogallery (photo uploads included)
* Creation page: Adventures / Dungeons (random uploads included)
* Creation page: Downloads (various programs available for download)

---

* Ad section and dating section (both surprisingly active)
* Links to other sites (now defuct)
* Few system pages (search in users, news, newsfeed, artices being in the approval process, top stats etc.)
* Forum (as in public discussion place)
* Head of Golden Dragon competition (best articles for a given time period)
* Polls
* Chat

* Registration (subject to approval)
* Wise Owl / Phorum (as in Phorum installation, separate from the page, with various hand-made wires to make it kinda works)

Private pages
=============

* "Table discussions" (~600 tables): categories, "flat" discussion list with post rating, book/ignore, notice board, access stats and polls
* Discussion voting
* User levels (based on activity)
* Private Messages (with groups)
* Ability to send new creations into approval queue (with cathegory-specific directions)
* Settings
    * Personal settings (user attributes change...ICQ status icon present!)
    * Mentoring system for new users
    * Mailing list for new creations
    * Default filters configuration
    * Login configuration / API key / skin settings
    * News groups (used in private messages)

Administration pages
====================

* Approval and comments for approval queue
* User registration approvals
* Article edit
* Head of Gold Dragon award management