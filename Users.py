__author__ = 'jsuit'

import numpy as np
"""
Users holds user: "artistid + songid": ratings
and user:userweights
"""


class Users(object):
    def __init__(self):
        self.users = {}
        self.userWeights = {}
        self.userBias = {}

    def addUser(self, uid):
        assert uid not in self.users
        self.users[uid] = []
        self.userWeights[uid] = np.random.random(1)
        self.userBias[uid] = None

    def addRatings(self, uid, artistID, songID, rating):
        artistID = str(artistID)
        songID = str(songID)
        if uid not in self.users:
            self.users[uid] = [("{0},{1}".format(artistID, songID), rating)]
        else:
            ratings = self.users[uid]
            ratings.append(("{0},{1}".format(artistID, songID), rating))
            self.users[uid] = ratings

    def getRatings(self,uid):
        assert uid in self.users
        return self.users[uid]

    def computeAvgRatingForUser(self,uid):
        assert uid in self.users
        avg = sum(float(r[1]) for r in self.users[uid])/float(len(self.users[uid]))
        if self.userBias[uid] is None:
            self.userBias[uid] = avg
            return avg
        else:
            return self.userBias[uid]

    def computeGlobalBias(self):
        assert self.users
        #sum of the ratigns for each user
        sumRatings = sum([sum(float(r[1]) for r in self.users[uid]) for uid in self.users])
        #num of ratings for each user
        numMovies = sum([len(self.users[uid]) for uid in self.users])
        avg = sumRatings/float(numMovies)
        assert avg > 0
        return avg

    def getWeights(self):
        return self.userWeights

    def getWeight(self, uid):
        assert uid in self.userWeights
        return self.userWeights[uid]

    def setBias(self, uid, bias):
        assert uid in self.userBias
        self.userBias[uid] = bias

    def getBias(self,uid):
        assert uid in self.userBias
        if self.userBias[uid] is None:
            avg = self.computeAvgRatingForUser(uid)
            return avg
        return self.userBias[uid]