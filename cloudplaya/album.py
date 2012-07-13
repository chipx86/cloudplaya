class Album(object):
    COLUMNS = [
        'albumArtistName', 'albumName', 'artistName', 'objectId',
        'primaryGenre', 'sortAlbumArtistName', 'sortAlbumName',
        'sortArtistName', 'albumCoverImageMedium', 'albumAsin',
        'artistAsin', 'gracenoteId', 'albumReleaseDate',
    ]

    def __init__(self, client, payload):
        self.client = client

        metadata = payload['metadata']
        self.id = metadata['objectId']
        self.name = metadata['albumName']
        self.asin = metadata.get('albumAsin', None)
        self.num_tracks = int(payload['numTracks'])
        self.release_date = metadata.get('albumReleaseDate', None)
        self.artist_asin = metadata.get('artistAsin', None)
        self.artist_name = metadata['artistName']
        self.primary_genre = metadata['primaryGenre']
        self.album_artist_name = metadata['albumArtistName']
        self.cover_image_url = metadata.get('albumCoverImageMedium', None)
        self.sort_album_artist_name = metadata['sortAlbumArtistName']
        self.sort_artist_name = metadata['sortArtistName']
        self.sort_album_name = metadata['sortAlbumName']

    def get_songs(self, *args, **kwargs):
        return self.client.get_track_list(self)

    def __repr__(self):
        return '<Album "%s">' % self.name

    def __str__(self):
        return self.name
