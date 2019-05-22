# -*- coding: utf-8 -*-

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

import pandas as pd

def getDatasetsFom1CSVFile(labeledCsv):
    
    df = pd.read_csv(labeledCsv)
    ds = df.values
    train_X, test_X, train_y, test_y = train_test_split(ds[:,1:-1], ds[:,-1], test_size=0.3, random_state=0)
    return (train_X, train_y, test_X, test_y)

def getDatasetsFrom1Dataframe(dfTrain):
    pass


# -----------------------------------------------------------------------------

trainFolder = r"D:/STI Dataset/train"
testFolder = r"D:/STI Dataset/test"

dsTrain = "SSabs+FSasm+ADN1abs+ADN2abs+ADN1rel+ADN2rel_Train.csv"
dsTest = "SSabs+FSasm+ADN1abs+ADN2abs+ADN1rel+ADN2rel_Test.csv"

(train_X, train_y, test_X, test_y) = getDatasetsFom1CSVFile(trainFolder+"/"+dsTrain)

# k Nearest Neighbour
knn = KNeighborsClassifier(n_neighbors = 3)
train_y = train_y[:].astype(int)
knn.fit(train_X, train_y)

yhat = knn.predict(train_X)


yhat = yhat[:].astype(int)

print "\nTRAINING STATS:"
print "classification accuracy:", metrics.accuracy_score(yhat, train_y)

yhat = knn.predict(test_X)

test_y = test_y[:].astype(int)
yhat = yhat[:].astype(int)

print "\nTESTING STATS:"
print "classification accuracy:", metrics.accuracy_score(yhat, test_y)
