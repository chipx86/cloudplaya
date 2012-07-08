class Artist(object):
    COLUMNS = [
        'artistName', 'objectId', 'sortArtistName', 'artistAsin',
    ]

    def __init__(self, client, payload):
        self.client = client

        metadata = payload['metadata']
        self.id = metadata['objectId']
        self.name = metadata['artistName']
        self.asin = metadata.get('artistAsin', None)
        self.sort_name = metadata['sortArtistName']
        self.num_tracks = payload['numTracks']

    def __repr__(self):
        return '<Artist "%s">' % self.name

    def __str__(self):
        return self.name
