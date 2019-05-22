# -*- coding: utf-8 -*-

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import pandas as pd

def getDatasetsFrom2CSVFiles(csvTrainFile, csvTestFile):
    
    dfTrain = pd.read_csv(csvTrainFile)
    dfTest = pd.read_csv(csvTestFile)
    
    return getDatasetsFrom2Dataframes(dfTrain, dfTest)

def getDatasetsFrom2Dataframes(dfTrain, dfTest):
    
    dsTrain = dfTrain.values
    dsTest = dfTest.values
    
    train_X = dsTrain[:,1:-1] # remove first and last columns ('id', 'category')
    train_y = dsTrain[:,-1] # get only last column 'category', the labels
    train_y = train_y[:].astype(int)
    
    test_X = dsTest[:,1:-1] # remove first and last columns ('id', 'category')
    test_y = dsTest[:,-1] # get only last column 'category', the labels
    test_y = test_y[:].astype(int)
    
    return (train_X, train_y, test_X, test_y)

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
#dsTrain = "files_sizes_train.csv"
dsTest = "SSabs+FSasm+ADN1abs+ADN2abs+ADN1rel+ADN2rel_Test.csv"

(train_X, train_y, test_X, test_y) = getDatasetsFom1CSVFile(trainFolder+"/"+dsTrain)
#(train_X, train_y, test_X, test_y) = getDatasetsFom1CSVFile(csv)
#(train_X, train_y, test_X, test_y) = getDatasetsFrom2Dataframes(dsTrain, dsTest)
#print (train_X, train_y, test_X, test_y)


random_state = 123
n_jobs = 1
verbose = 2
clf = RandomForestClassifier(n_estimators=100, random_state=random_state, n_jobs=n_jobs, verbose = verbose)

# Start training
#print('training started')

train_y = train_y[:].astype(int)
clf.fit(train_X, train_y)

#print('training completed')

#Check on the training set and visualize performance
yhat=clf.predict(train_X)


yhat = yhat[:].astype(int)

print "\nTRAINING STATS:"
print "classification accuracy:", metrics.accuracy_score(yhat, train_y)

yhat=clf.predict(test_X)

test_y = test_y[:].astype(int)
yhat = yhat[:].astype(int)

print "\nTESTING STATS:"
print "classification accuracy:", metrics.accuracy_score(yhat, test_y)
