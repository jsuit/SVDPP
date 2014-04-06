__author__ = 'jsuit'
import numpy as np


class MusicMatrix(object):
    def __init__(self):
        self.musicMatrix = {}
        #self.artists? ... probably don't need this
        self.artists = {}
        self.artistsSongBias={}

    def addArtistSong(self, artistID,songID,F,rating):
        artistID = str(artistID)
        songID = str(songID)
        mhash = "{0},{1}".format(artistID, songID)
        assert isinstance(F, int)
        self.musicMatrix[mhash] = np.random.random(F)
        self.artistsSongBias[mhash] = None
        if artistID in self.artists:
            self.artists[artistID].append((songID, rating))
        else:
            self.artists[artistID] = [(songID, rating)]

    def getArtistSong(self, artistID, songID):
        artistID = str(artistID)
        songID = str(songID)
        hash = "{0},{1}".format(artistID, songID)
        return self.musicMatrix[hash]

    def returnSongsForArtist(self, artistID):
        assert artistID in self.artists
        return self.artists[artistID]

    def findArtistBySong(self,songID ):
        mlist = []
        for artist in self.artists.iterkeys():
            if songID in self.artists[artist]:
                mlist.append(artist)
        return mlist

    def getFeatures(self, artistID,songID):
        artistID = str(artistID)
        songID = str(songID)
        hash = "{0},{1}".format(artistID, songID)
        return self.musicMatrix[hash]

    """
    songID : "artistID,songID"
    """
    def getFeatures(self, songID):
        assert songID in self.musicMatrix
        return self.musicMatrix[songID]

    def setFeatures(self,songID, features):
        assert songID in self.musicMatrix
        self.musicMatrix[songID] = features

    def setFeatures(self, songID, features):
        assert songID in self.musicMatrix
        assert len(self.musicMatrix[songID]) == len(features)
        self.musicMatrix[songID] = features

    def getFeature(self, artistID,songID, pos):
        artistID = str(artistID)
        songID = str(songID)
        hash = "{0},{1}".format(artistID, songID)
        assert isinstance(pos, int)
        return self.musicMatrix[hash][pos]

    def getSongs(self):
        return self.musicMatrix

    def getArtists(self):
        return self.artists

    def computeAvg1(self, artID, songID):
        assert artID in self.artists
        mhash = "{0},{1}".format(artID, songID)
        assert mhash in self.musicMatrix
        s = sum([float(rating[1]) for rating in self.artists[artID] if rating[0] == songID])
        leng = sum([1 for rating in self.artists[artID] if rating[0] == songID])
        return s/float(leng)

    def computeAvg(self, songID):
        #surprise: songID is really artistID,songID string
        assert songID in self.musicMatrix
        keys = songID.split(",")
        #keys[0] == artistID
        #keys[1] == songID
        return self.computeAvg1(keys[0], keys[1])

    def setBias(self, songID, bias):
        assert songID in self.artistsSongBias
        self.artistsSongBias[songID] = bias

    def getBias(self, songID):
        assert songID in self.artistsSongBias
        if self.artistsSongBias[songID] is None:
            avg = self.computeAvg(songID)
            self.artistsSongBias[songID] = avg
            return avg
        else:
            return self.artistsSongBias[songID]