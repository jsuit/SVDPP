__author__ = 'jsuit'
from MusicMatrix import *
from UserMatrix import *
import json




def buildUserMusicMatrix(uMatrix, mMatrix, filename = "users.json"):
    extension = filename.split(".")[-1]
    if(extension.lower() == "json"):
        data = json.load(open(filename, "r"))
        for key in data:
            assert key not in uMatrix.getUsersDict()
            uMatrix.addUser(key, 20)
            row = data[key]
            for mdict in row:
                if "TrainData" in mdict:
                    mdict2 = mdict["TrainData"]
                    artID = mdict2["Artist"]
                    songID = mdict2["Track"]
                    rating = mdict2["Rating"]
                    mMatrix.addArtistSong(artID, songID, 20, rating)
                    uMatrix.addUserRating(key, rating, songID, artID)

def setup(file="/Users/jsuit/Documents/workspaceGT/RecommendationCS6242/users.json"):
    mMatrix = MusicMatrix()
    uMatrix = UserMatrix()
    buildUserMusicMatrix(uMatrix,mMatrix, file)
    return uMatrix,mMatrix