#!/usr/bin/env python
import os
import sys
from optparse import OptionGroup, OptionParser

import requests

from cloudplaya.client import Client, RequestError
from cloudplaya import VERSION


class Command(object):
    def add_options(self, parser):
        pass

    def run(self):
        pass

    def output_item_formatted(self, item):
        try:
            fmt = self.options.format.decode('string_escape')
            s = fmt % item.__dict__

            print s.encode('utf-8')
        except KeyError, e:
            sys.stderr.write('Invalid format string key: %s' % e)
            sys.exit(1)


class Authenticate(Command):
    """Authenticates with Amazon Cloud Player and generates a session file."""
    def add_options(self, parser):
        parser.add_option('--username', default=None,
                          help='the username to log in as')
        parser.add_option('--password', default='%(name)s',
                          help='the password for your user')

    def run(self):
        try:
            if self.client.authenticate(self.options.username,
                                        self.options.password):
                print 'Authenticated successfully.'
            else:
                sys.stderr.write('Authentication failed.\n')
                sys.exit(1)
        except IOError, e:
            sys.stderr.write('Unable to write authentication data: %s' % e)
            sys.exit(1)


class DownloadAlbum(Command):
    """Downloads all the songs in an album."""
    DEFAULT_FORMAT = os.path.join('%(album_name)s',
                                  '%(track_num)s. %(title)s.%(extension)s')

    def add_options(self, parser):
        parser.add_option('--format', default=self.DEFAULT_FORMAT,
                          help='format string for filenames')
        parser.add_option('--artist', default=None,
                          help='the artist name for listed songs')
        parser.add_option('--album', default=None,
                          help='the album name for listed songs')
        parser.add_option('-o', '--out-directory', default=None,
                          help='the directory to save the files')

    def run(self):
        search = []

        if self.options.artist:
            search.append(('artistName', 'EQUALS', self.options.artist))

        if self.options.album:
            search.append(('albumName', 'EQUALS', self.options.album))

        print 'Loading album information..'

        try:
            songs = list(self.client.get_songs(search))
        except RequestError, e:
            sys.stderr.write('Failed to download song information: %s\n' % e)
            sys.exit(1)

        song_ids = [song.id for song in songs]

        try:
            urls = self.client.get_song_stream_urls(song_ids)
        except RequestError, e:
            sys.stderr.write('Failed to get stream URLs: %s\n' % e)
            sys.exit(1)

        out_dir = self.options.out_directory or os.getcwd()

        for song, url in zip(songs, urls):
            try:
                out_filename = self.options.format % song.__dict__
            except KeyError, e:
                sys.stderr.write('Invalid format string key: %s' % e)
                sys.exit(1)

            out_path = os.path.join(out_dir, out_filename)
            os.makedirs(os.path.dirname(out_path))

            print 'Downloading %s...' % out_path
            r = requests.get(url)

            try:
                f = open(out_path, 'w')

                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)

                f.close()
            except IOError, e:
                sys.stderr.write('Unable to write file %s: %s' % (out_path, e))
                sys.exit(1)

class GetAlbums(Command):
    """Lists all the albums"""
    DEFAULT_FORMAT = '%(name)s by %(artist_name)s (%(num_tracks)s tracks)'

    def add_options(self, parser):
        parser.add_option('--artist', default=None,
                          help='list albums by the given artist')
        parser.add_option('--format', default=self.DEFAULT_FORMAT,
                          help='format string for each listed album')

    def run(self):
        search = []

        if self.options.artist:
            search.append(('artistName', 'EQUALS', self.options.artist))

        try:
            for album in self.client.get_albums(search):
                self.output_item_formatted(album)
        except RequestError, e:
            sys.stderr.write('Failed to get albums: %s\n' % e)
            sys.exit(1)


class GetAlbum(Command):
    """Displays information on an album"""
    DEFAULT_FORMAT = '%(name)s by %(artist_name)s (%(num_tracks)s tracks)'

    def add_options(self, parser):
        parser.add_option('--artist', default=None,
                          help='the name of the artist')
        parser.add_option('--name', default=None,
                          help='the name of the album')
        parser.add_option('--format', default=self.DEFAULT_FORMAT,
                          help='format string for the album')

    def run(self):
        if not self.options.artist or not self.options.name:
            sys.stderr.write('get-album requires --artist and --name\n')
            sys.exit(1)

        try:
            album = self.client.get_album(self.options.artist,
                                          self.options.name)
            self.output_item_formatted(album)
        except RequestError, e:
            sys.stderr.write('Failed to get albums: %s\n' % e)
            sys.exit(1)


class GetArtists(Command):
    """Lists all the artists"""
    DEFAULT_FORMAT = '%(name)s (%(num_tracks)s tracks)'

    def add_options(self, parser):
        parser.add_option('--format', default=self.DEFAULT_FORMAT,
                          help='format string for each listed album')

    def run(self):
        try:
            for artist in self.client.get_artists():
                self.output_item_formatted(artist)
        except RequestError, e:
            sys.stderr.write('Failed to get artists: %s\n' % e)
            sys.exit(1)


class GetSongs(Command):
    """Lists all songs, or songs matching a criteria"""
    DEFAULT_FORMAT = '%(artist_name)s - %(title)s'

    def add_options(self, parser):
        parser.add_option('--format', default=self.DEFAULT_FORMAT,
                          help='format string for each listed album')
        parser.add_option('--artist', default=None,
                          help='the artist name for listed songs')
        parser.add_option('--album', default=None,
                          help='the album name for listed songs')
        parser.add_option('--title', default=None,
                          help='the title of the song')

    def run(self):
        search = []

        if self.options.artist:
            search.append(('artistName', 'EQUALS', self.options.artist))

        if self.options.album:
            search.append(('albumName', 'EQUALS', self.options.album))

        if self.options.title:
            search.append(('title', 'EQUALS', self.options.title))

        try:
            for song in self.client.get_songs(search):
                self.output_item_formatted(song)
        except RequestError, e:
            sys.stderr.write('Failed to get artists: %s\n' % e)
            sys.exit(1)


class GetStreamURLs(Command):
    """Lists stream/download URLs for songs."""
    def run(self):
        search = []

        if not self.args:
            sys.stderr.write('One or more song IDs must be specified\n')
            sys.exit(1)

        try:
            for url in self.client.get_song_stream_urls(self.args):
                print url
        except RequestError, e:
            sys.stderr.write('Failed to get stream URLs: %s\n' % e)
            sys.exit(1)


COMMANDS = {
    'authenticate': Authenticate(),
    'download-album': DownloadAlbum(),
    'get-albums': GetAlbums(),
    'get-album': GetAlbum(),
    'get-artists': GetArtists(),
    'get-songs': GetSongs(),
    'get-stream-urls': GetStreamURLs(),
}

def parse_options(args):
    usage = '%prog command [options] path\n\n'
    usage += 'The following commands are available:\n\n'

    max_name_len = 0

    for name in COMMANDS.keys():
        max_name_len = max(max_name_len, len(name))

    for name in sorted(COMMANDS.keys()):
        usage += '  %s - %s\n' % (name.ljust(max_name_len),
                                  COMMANDS[name].__doc__.strip())

    parser = OptionParser(usage=usage,
                          version='%prog ' + VERSION)
    parser.add_option('--session-file', default=None,
                      help='the session file to use')
    parser.disable_interspersed_args()

    options, args = parser.parse_args(args)

    # We expect at least a command
    if len(args) == 0 or args[0] not in COMMANDS.keys():
        parser.print_help()
        sys.exit(1)

    command_name = args[0]
    command = COMMANDS[command_name]

    parser = OptionParser(usage='%prog ' + command_name + ' [options]',
                          version='%prog ' + VERSION)
    command.add_options(parser)
    command.options, command_args = parser.parse_args(args)
    command.args = command_args[1:]

    return options, command


def main():
    options, command = parse_options(sys.argv[1:])

    client = Client(session_file=options.session_file)

    if not client.authenticated and command != COMMANDS['authenticate']:
        sys.stderr.write('You must authenticate before you can use '
                         'cloudplaya:\n')
        sys.stderr.write('    $ cloud-playa authenticate --username <username> '
                         '--password <password>\n')
        sys.exit(2)

    command.client = client
    command.run()

if __name__ == '__main__':
    main()
