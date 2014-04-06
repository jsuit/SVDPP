__author__ = 'jsuit'

import numpy as np
from UserMatrix import *
from MusicMatrix import *
import json
import setup
from copy import deepcopy
from pprint import pprint
from math import pow
from math import fabs
"""
Globals:
gamma1 = learningRate for b_u
gamma2 = learning Rate for b_i == gama1
gamma3 = lr for q_i = musicMatrix[i] and p_u = UserMatrix
gamma3 = also lr for Implicit
gamma4 = lr for k similar items/users
"""



#num of features

MAX = pow(10,6)
MIN = pow(10,-6)


def setupParams(pgamma1=pow(10,-4), pgamma2=pow(10,-4), pgamma3=pow(10,-4), pgamma4=pow(10,-4),
                puserReg=pow(10,-4), pitemProfileReg=pow(10,-4),
                puserProfileReg=pow(10,-4), pweightReg=pow(10,-4)):
    global gamma1, gamma2, gamma3, gamma4, userReg, itemProfileReg, userProfileReg, weightReg, itemReg
    gamma1 = pgamma1
    gamma2 = pgamma2
    gamma3 = pgamma3
    gamma4 = pgamma4
    userReg = puserReg
    itemProfileReg = pitemProfileReg
    userProfileReg = puserProfileReg
    weightReg = pweightReg
    itemReg = userReg

#void update(graphchi_vertex<VertexDataType, EdgeDataType> &vertex, graphchi_context &gcontext) {
"""
update for user
"""


def update(uID):
    global tolerance
    global uMatrix
    global mMatrix
    global itemProfileReg
    global weightReg
    global userReg
    global gamma1, gamma2, gamma3, gamma3, gamma4, itemReg
    if uMatrix.hasRatings(uID):
        loop = True
        while (loop):
            mu = globalMean
            b_u = uMatrix.getBias(uID)
            ratings = uMatrix.getUserRatings(uID)
            #ratings = [rating[1] for rating in ratings]

        #toDo use Implicit data
        #getImplicitData
        #do some things with it.

            for (songid, rating) in ratings:
                true_rating = float(rating)
                b_i = mMatrix.getBias(songid)
                 #songID is really artistID,songID
                error = true_rating - predictRating(uID, songid, true_rating)
                if fabs(error) <= tolerance:
                    loop = False
                else:
                    print fabs(error)
                q_i = mMatrix.getFeatures(songid)
                q_iold = deepcopy(q_i)
                p_u = uMatrix.getUserLatent(uID)
                #p_uold = deepcopy(p_u)
                #todo 0 should be sum of implicit data

                 #q_i = q_i + gamma2  *(e_ui*(p_u +  sqrt(N(U))\sum_j y_j) - lamba7   *q_i)
                q_i +=  gamma2 * (error * (p_u + 0) - itemProfileReg * q_i)
                mMatrix.setFeatures(songid, q_i)

                #p_u = p_u + gamma2    *(e_ui*q_i   -gamma7     *p_u)
                p_u += gamma2 * (error * q_iold - itemProfileReg * p_u)
                uMatrix.updateFeatures(uID, p_u)
                #b_i = b_i + gamma1*(e_ui - gmma6 * b_i)
                b_i += gamma1 * (error - itemReg * b_i)
                mMatrix.setBias(songid, b_i)
                #b_u = b_u + gamma1*(e_ui - gamma6 * b_u)
                b_u += gamma1 * (error - userReg * b_u)
                uMatrix.setBias(uID, b_u)

            #todo y_j = y_j  +   gamma2*(error*sqrt|N(u)|* q_i - itemProfReg * y_j


"""
songID = "artistID,songID"
"""


def predictRating(uid, songID, rating):
    #global bias
    prediction = globalMean
    # + user_bias + songBias
    prediction += uMatrix.getBias(uid) + mMatrix.getBias(songID)
    #now prediction == a baseline
    # + q_i^T *(p_u +sqrt(|N(u)|)\sum y_j)
    #todo add implicit data
    prediction += np.dot(uMatrix.getUserLatent(uid), mMatrix.getFeatures(songID))
    global MIN, MAX
    prediction = max(MIN, min(prediction, MAX))
    return prediction


if __name__ == "__main__":
    global uMatrix, mMatrix, globalMean, F
    tolerance = pow(10,-4)
    setupParams()
    uMatrix, mMatrix = setup.setup()
    F = uMatrix.F
    globalMean = uMatrix.getGlobalAverage()
    update("1000")
    pprint(uMatrix.getUserLatent("0"))




