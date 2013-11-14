
VoteIT Who's online
===================

.. image:: https://travis-ci.org/VoteIT/voteit.whosonline.png?branch=master
   :target: https://travis-ci.org/VoteIT/voteit.whosonline

This is a plugin for VoteIT that tracks who's online within meetings.
It displays the profile pictures of a number of users who were the latest online. (Default 8)

Online in this context means simply loading a page, or do something that generates a request.


Caveats
-------

* There's no persistence. When you restart, everything is gone.
* This package isn't thread safe, so only use one instance.
* It will cause writes on every request, but only to memory since nothing is stored on disk.


Installation
------------

Simply include the package in the paster config file under the section 'plugins', like:

plugins =
    voteit.whosonline
