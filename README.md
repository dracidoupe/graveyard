# Graveyard: Place for Dead (and Undead)

Graveyard is an attempt at open-source reimplementation of DraciDoupe.cz (referred to as DDCZ in this text).

## Installation

You can run Graveyard either directly on your machine or inside [Docker](https://www.docker.com/).

Installing and running Graveyard directly is faster (on some systems) and removes one lever of indirection, but it makes the setup more compliated. 

Running in Docker requires familiarity with it, but it makes setup easier and guarantees consistency with the testing environment (and hopefully in the future, production environment as well). 

In both cases, first clone this repository and run all commands in it. 

### Installing in Docker

Requirements:

* You have [Docker CE installed](https://www.docker.com/community-edition)
* You have [installed docker-compose](https://docs.docker.com/compose/install/)

Verify you have everything ready by running the test suite:

* `docker-compose run web python3 manage.py test`

If you see output like this:

```
(graveyard-venv) almad@zeruel:~/projects/graveyard$ docker-compose run web python3 manage.py test
Starting graveyard_db_1 ... done
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
Destroying test database for alias 'default'...
(graveyard-venv) almad@zeruel:~/projects/graveyard$ 

```

You are all set. Afterwards, install database schema by running

*  `docker-compose run web python3 manage.py migrate`

You are done! Now you can just run the project and develop using

*  `docker-compose start`


### Installing on your machine

Graveyard is currently written in [Django](https://www.djangoproject.com/). Requirements to develop it:

* You have working Python 3 installation on your machine
* You have working MySQL installation on your machine

To use the project, clone this repository and:

* Create a virtual environment: `python3 -m venv gvenv`
* Enter it (on Mac OS X or Linux): `source gvenv/bin/activte`
* Copy settings template: `cp graveyard/settings/local.example.py graveyard/settings/local.py`
* Edit the settings above, especially enter credentials to your local MySQL
* Create the database schema: `python manage.py migrate`
* Run the thing! `python manage.py runserver`
* Observe if you have contact at `http://localhost:8000`
* Maybe create a superuser in order to enter admin: `python manage.py createsuperuser`
* Look around the administration interface at `http://localhost:8000/admin/`


## QNEA (Questions Not Even Asked)

### What is it?

DraciDoupe.cz is a collaboration place for pen-and-paper RPG creativists, designed to host a single (dated) RPG system, Draci Doupe, from a single country, Czech Republic. Back in early 00's, it also served as a social network for (not only teen) fantasy fans.

In peak of its popularity, it enjoyed thousands of visitors per day (huge number back then). The popularity declined as both technology, the RPG system and the concept of community sites become dated (being consumed by Facebook and likes). It still treasures hundreds of articles and a lot of capture creativity.

Hence, it still attracts few hundred of visitors every day.

### Why work on it?

Because I want to keep it available, something to be discovered for both nostalgics and new player generation, if only for nostalgia reasons. That is unsustainable in current state, mainly for security reasons. 

Also, I am just grateful. This site shaped my life like nothing else.

### Why not fix the product in the process?

That was an idea of RPGPlanet, planned successor to DraciDoupe.cz. It, however, entered development hell, coupled with changing landscape of how sites are consumed. It was also never truly accepted by community, hence dying before bing born. 

Thus, I decided to instead fix the current state. 

### Why reimplementation instead of fix?

Because it has been born in a different time and is very hard to fix incrementally. 

Smartphone was not a thing, PDA barely was. Broadband was only available at universities, dial-up connection was a way to connect to internet. PHP just changed its name and came out as PHP 3. CSS was in version 1 and impossible to get working accross browsers consistently; tables were used to do page layouts. Netscape was something to be tested. Mozilla Suite was gaining traction, Firebird (later called Firefox) hasn't been born yet. Internet Explorer 5 was ruling it.

DDCZ has been kicked out by its hosting provider for consuming more than 1 GB of outbound traffic _per month_, moving on to be hosted on bare metal. The database was huge for its time, counting data in _hundreds of megabytes_. That's why UTF has been considered wasteful at the time and not adopted everywhere. 

JavaScript (called JScript in IE) was in its infancy, both DOM and language inconsistent accross browsers (without any façade library; jQuary hasn't been born yet), painfully slow and with security holes, as well as cookies. _The whole site has been designed to work with both JavaScript AND cookies to be turned off_. 

PHP, the implementation language of choice (not many other options, although ASP 3 implementation has been attempted) hasn't supported `register_globals` feature flag and it has been _on_. This created a huge problem for the future since it can't be turned on in "modern" PHPs. This renders the whole codebase unworkable and tricky to refactor.

At last, but not at least, the whole site has been architected, designed and implemented by three 16 year olds who learned programming on this. 

All of those contribute to architectural decisions that are very hard to reverse, and clean-slate rewrite is better option. 

### You don't have time to do this

I don't and I don't want this to be another RPGPlanet. Which is why this is going to be implemented in stages, fist one being very easy yet still useful. 

### What will stay?

Most of the things from user perspective. The goal is to preserve, not to rework. Some changes will be done in the name of usability, though.

* Public site still usable without cookies
* Privacy still considered important
* Original URLs. Redirects will be in place
* Site being Czech to the bones (and routes)
* Skins. They are terrible, make the site much harder to develop, makes maintenance costly and doesn't bring almost any value. I love them
* Filters, some of them. They are beautifully terrible in the same way skins are
* User registration approval. It's elitists, awful, unfriendly and it makes the site the way it is
* Focus on user privacy. All data is pseudonymous. No personal information collected

### What will change?

* Either cookies or local storage (TBD) will be required for skins and for log in. Those days, it's _more_ safe than URL parameter, trust me. It also means it is safer to have longer session length than terrible 15 minutes
* Public site still working without either, though
* SEO, those articles deserve it. Current site is _very_ unfriendly to search engines
* Security, on multiple levels
* Moudra Sova, the over-the-decade, manually-patched version of Phorum is going to either go away, or be sandboxed. It doesn't see almost any activity anyway
* Source now open (as opposed to old version)
* Filters, some of them. In a lot of places they don't really make sense; I want to keep them, but if they'd complicate implementation too much, they are (at least temporarily) gone

## Design 

Technically, DDCZ is kinda CMS with simple workflow meeting very simple social network. 

### Considerations

* MySQL is the database of choice and integration layer between old and new. For all its awfulness, this will stay. While database pretends to be in latin2 (and even the site's connectin to it is explicitly set to latin2), the actual content is stored in cp1250. This is a major fuckup that will render most default tools unusable with the database. "Proper" Python way to present a record is to connect using `latin2` encoding and then convert individual records using `record.encode("latin2").decode("cp1250").encode("utf-8")`
* Page load speed is a concern. Everybody loves fast pages
* General speed and scalability is not a concern. Whole dataset can fit into modern memory. Please do not optimise on bare metal and single node
* Maintenance cost is a concern. The less it costs to run, the more likely it will stay with us
* Stability of an ecosystem is a concern. This site is going to run for another decade. Which technologies do you think are going to stay for so long, preferably with no need for upgrade? That site, this has been always my playground for failed experiments. Judge me

### Separation of concerns

Precisely for the abovementioned reasons, decoupling data, frontend and backend is useful to be able to move forward carefully. Hence:

* Backend API for exposing data (cleaned up, normalised and in UTF-8) running on top of...nonideal database
* Frontend (server-rendered on public website for usability) consuming that API and displaying results
	* While SPA limit SEO and have their class of problems, they are useful in the initial prototype in order to avoid another layer of applications. Over time, public pages should be completely migrated to dedicated application, running reasonable framework and _generating_ site on public webpages
* Compatibility redirect, exchanging cookie authentication for URL authentication for the old DDCZ

## Pages & Data Design

Oh boy, this thing has a _lot_ of dubiously designed data underneath. However, from a high-level perspective, they would be normalised as follows.

There is a Czech/English tension in the naming. Decision TBD. 

### Public pages

* Common attributes for all "creation" pages: Author, External source (for _very_ legacy articles from bootstrapped version of the page), rating (AVG of all votes, expressed in starts, 0-5) and read and print counters
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

### Private pages

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

### Administration pages

* Approval and comments for approval queue
* User registration approvals
* Article edit
* Head of Gold Dragon award management

## Dictionary

Dictionary of words used during move and translation. 

## Universal domain names

* Sekce = Sections
* Nazev stranky / rubriky = Page Heading
* Nickname = nick (always shortened)

## Pages

* Aktuality = News
* Novinky = Newsfeed

## Rubriky (= Creative Pages)
