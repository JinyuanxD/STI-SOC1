# -*- coding: utf-8 -*-

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
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

estimators_col = (100,)
learning_rates = (0.085,)
max_depths = (1,)

fileOutput = open('c:/tmp/test.txt', 'w')

for estimators in estimators_col:
    for learning_rate in learning_rates:
        for max_depth in max_depths:
            
            print 'get classifier instance: Estimators: '+str(estimators)+', learning_rate: '+str(learning_rate)+', max_depth: '+str(max_depth)+'\n'
            
            
            clf = GradientBoostingClassifier(n_estimators=estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=0)
            
            print 'fit\n'
            train_y = train_y[:].astype(int)
            clf.fit(train_X, train_y)
            print 'predict\n'
            yhat=clf.predict(test_X)
            test_y = test_y[:].astype(int)
            yhat = yhat[:].astype(int)
            
            accuracy = metrics.accuracy_score(yhat, test_y)
            
            line = 'GradientBoosting\t Estimators: '+str(estimators)+' \t Learning Rate: '+str(learning_rate)+' \t MaxDepth: '+str(max_depth)+' \t Accuracy: '+str(accuracy)
            print line+'\n'
            line = 'GradientBoosting,'+str(estimators)+','+str(learning_rate)+','+str(max_depth)+','+str(accuracy) + '\n'
            
            fileOutput.write(line)
            fileOutput.flush()
            
fileOutput.close()

