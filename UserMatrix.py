import numpy as np
from Implicit import *
from Users import *

class UserMatrix(object):
    def __init__(self):
        self.Users = {}
        self.UsersImplicit = {}
        self.U = Users()
        self.F = 0

    def addUser(self,userID,F):
        assert userID not in self.Users
        assert isinstance(F, int)
        assert userID not in self.UsersImplicit
        self.UsersImplicit[userID] = Implicit(userID)
        self.Users[userID] = np.random.random(F)
        self.U.addUser(userID)
        self.F= F

    def addUserRating(self,uid,rating, songId, artID):
        self.U.addRatings(uid, artID, songId, rating)

    def getUserRatings(self,uid):
        return self.U.getRatings(uid)

    def getUserAverage(self, uid):
        return self.U.computeAvgRatingForUser(uid)
    """
    avg rating of all movies
    """
    def getGlobalAverage(self):
        return self.U.computeGlobalBias()

    def getUserLatent(self, keyID):
        return self.Users[keyID]

    def getUsersDict(self):
            return self.Users;

    def getSizeFeatures(self, id):
        assert id in self.Users[id]
        return len(self.Users[id])
    
    def getFeatures(self, uid ):
        assert uid in self.Users
        return self.Users[uid]
    
    def updateFeatures(self, uid, features):
        assert uid in self.Users
        self.Users[uid] = np.array(features)

    def updateFeature(self,uid, feature, pos):
        assert uid in self.Users
        assert isinstance(pos, int)
        self.Users[uid][pos] = np.float(feature)

    def getFeature(self, uid, pos):
        assert uid in self.Users
        assert isinstance(pos, int)
        return self.Users[uid][pos]

    def hasRatings(self,uid):
        return len(self.U.getRatings(uid)) > 0

    def getUsers(self):
        return self.U.users

    def getUser(self, uid):
        assert uid in self.U.users
        return self.U.users[uid]

    def getBias(self, uid):
        return self.U.getBias(uid)

    def setBias(self, uid, bias):
        self.U.setBias(uid, bias)




