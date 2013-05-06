cloudplaya
==========

cloudplaya is a Python library and command line utility for querying Amazon's
Cloud Player service. It can be used to build playlists, download songs, or
integrate with other software that needs to talk to Cloud Player.


Installation
------------

To install cloudplaya, just run::

    $ sudo easy_install cloudplaya


Authenticating
--------------

You will need to first authenticate with Amazon Cloud Player. This will store
.cloudplayarc file in your home directory containing some session information.
Note that it's possible you may have to repeat this on occasion.

To authenticate, run::

    $ cloudplaya authenticate --username <email_address> --password <password>

Replace ``<email_address>`` and ``<password>`` with your Amazon account
e-mail and password above.

You're then ready to use cloudplaya!


Commands
--------

cloudplaya has a few different commands that are used to fetch data from
Amazon Cloud Player. They each have their own arguments, and are invoked like::

    $ cloudplaya command [options]


get-album
~~~~~~~~~

Displays information on an album. It requires the ``--artist`` and ``--name``
options, and will show some basic information on the album.

For example::

    $ cloudplaya get-album --artist "The Birthday Massacre" --name "Walking With Strangers"
    Walking With Strangers by The Birthday Massacre (12 tracks)

You can use ``--format`` to specify the format for display. This defaults to
``%(name)s by %(artist_name)s (%(num_tracks)s tracks)``. Use ``%r`` with any
query to see all the available options. (This will display a Python dictionary
of the data.)


get-albums
~~~~~~~~~~

Lists all the albums in the account, or all matching the given options.

You can use ``--artist`` to specify an artist name. In this case, it will
show all albums by that artist. If you don't specify an artist, all albums
in your account will be listed.

For example::

    $ cloudplaya get-albums --artist "Greg Edmonson"
    Firefly


You can use ``--format`` to specify the format for display. This defaults to
``%(name)s by %(artist_name)s (%(num_tracks)s tracks)``. Use ``%r`` with any
query to see all the available options. (This will display a Python dictionary
of the data.)


get-artists
~~~~~~~~~~~

Lists all artists with albums in your account.


For example::

    $ cloudplaya get-artists
    ...
    Trent Reznor and Atticus Ross (56 tracks)
    Various Artists (1 tracks)
    Video Games Live (18 tracks)
    ...

You can use ``--format`` to specify the format for display. This defaults to
``%(name)s (%(num_tracks)s tracks)``. Use ``%r`` with any query to see all the
available options. (This will display a Python dictionary of the data.)


get-songs
~~~~~~~~~

Lists all songs in the account, or all matching the given options.

You can narrow down the results by using one or more of ``--artist``,
``--album``, or ``--title``.

For example::

    $ cloudplaya get-songs --album "Walking With Strangers"
    The Birthday Massacre - Falling Down
    The Birthday Massacre - Goodnight
    The Birthday Massacre - Kill The Lights
    The Birthday Massacre - Looking Glass
    The Birthday Massacre - Movie
    The Birthday Massacre - Red Stars
    The Birthday Massacre - Remember Me
    The Birthday Massacre - Science
    The Birthday Massacre - To Die For
    The Birthday Massacre - Unfamiliar
    The Birthday Massacre - Walking With Strangers
    The Birthday Massacre - Weekend

You can use ``--format`` to specify the format for display. This defaults to
``%(artist_name)s - %(title)s'``. Use ``%r`` with any query to see all the
available options. (This will display a Python dictionary of the data.)


get-stream-urls
~~~~~~~~~~~~~~~

Lists URLs for one or more songs. These can be used to download or stream the
songs.

This command takes song IDs as parameters. You can retrieve a song ID by
using the ``%(id)s`` format argument to ``get-songs`` above.

For example::

    $ cloudplaya get-songs --album "Walking With Strangers" --format "%(id)s"
    12fad491-033f-43f2-9fff-c65a96ccf173
    ...

    $ cloudplaya get-stream-urls 12fad491-033f-43f2-9fff-c65a96ccf173
    http://blahblah.amazonaws.com/lotsandlotsofstuff

(IDs and URLs have been changed to protect the innocent.)


download-album
~~~~~~~~~~~~~~

Downloads all the songs in an album.

This command requires the ``--album`` and ``--artist`` options. It can also
take a ``--out-directory`` (or ``-o``) to specify where to save the files
(defaults to the current directory).

It also can take a ``--format`` option to specify the filename format (defaults
to ``%(album_name)s/%(track_num)s. %(title)s.%(extension)s``). This will
create any directories as needed.

For example::

    $ cloudplaya download-album --album "Walking With Strangers" --artist "The Birthday Massacre"

Progress will be reported as the album downloads.

download-all
~~~~~~~~~~~~

Downloads all songs by artist.

This command has a ``--start-at-artist`` option, which will start downloading based on a
specified artist name, skipping any entries are lexicographically smaller. To test this
command, ``--dry-run`` will run through the steps without actually downloading. It can also
take a ``--out-directory`` (or ``-o``) to specify where to save the files
(defaults to the current directory).

It also can take a ``--format`` option to specify the filename format (defaults
to ``%(album_name)s/%(track_num)s. %(title)s.%(extension)s``). This will
create any directories as needed.

For example::

    $ cloudplaya download-all --start-at-artist "Fartbarf" --dry-run --out-directory /tmp/

Progress will be reported as the songs are downloaded.

