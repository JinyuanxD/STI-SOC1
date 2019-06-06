from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import label_binarize
from sklearn import metrics
from sklearn.metrics import roc_curve, auc


import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


def getDatasetsFom1CSVFile(labeledCsv):
    
    df = pd.read_csv(labeledCsv)
    ds = df.values
    train_X, test_X, train_y, test_y = train_test_split(ds[:,1:-1], ds[:,-1], test_size=0.3, random_state=0)
    return (train_X, train_y, test_X, test_y)

trainFolder = r"F:/datasets"

dsTrain = "features_combine.csv"
(train_X, train_y, test_X, test_y) = getDatasetsFom1CSVFile(trainFolder+"/"+dsTrain)

df = pd.read_csv(trainFolder+"/"+dsTrain)
ds = df.values
category = np.asarray(df.pop("category"))
label = label_binarize(category, classes=[1,2,3,4,5,6,7,8,9])
n_classes = label.shape[1]
#print(n_classes)

estimators_col = (100,)
learning_rates = (0.085,)
max_depths = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
#max_depths = (1,2,3)

train_results = []
test_results = []

fileOutput = open('c:/tmp/test.txt', 'w')

for estimators in estimators_col:
    for learning_rate in learning_rates:
        for max_depth in max_depths:
            
            print 'get classifier instance: Estimators: '+str(estimators)+', learning_rate: '+str(learning_rate)+', max_depth: '+str(max_depth)+'\n'
            clf = GradientBoostingClassifier(n_estimators=estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=0)
            
            print 'fit\n'
            train_y = train_y[:].astype(int)
            clf.fit(train_X, train_y)
            train_pred = clf.predict(train_X)
            
            accuracy = metrics.accuracy_score(train_pred, train_y)
            print("Train Accuracy: " + str(accuracy) + "\n")
            train_results.append(accuracy)
            #print(train_pred)
            #
            #false_positive_rate, true_positive_rate, thresholds = roc_curve(train_y[:, i], train_pred[:, i])
            #roc_auc = auc(false_positive_rate, true_positive_rate)
            #train_results.append(roc_auc)

            print 'predict\n'
            yhat=clf.predict(test_X)
            test_y = test_y[:].astype(int)
            yhat = yhat[:].astype(int)
            #false_positive_rate, true_positive_rate, thresholds = roc_curve(test_y[:, i], yhat[:, i])
            #roc_auc = auc(false_positive_rate, true_positive_rate)
            #test_results.append(roc_auc)
            
            accuracy = metrics.accuracy_score(yhat, test_y)
            
            line = 'GradientBoosting\t Estimators: '+str(estimators)+' \t Learning Rate: '+str(learning_rate)+' \t MaxDepth: '+str(max_depth)+' \t Accuracy: '+str(accuracy)
            print line+'\n'
            line = 'GradientBoosting,'+str(estimators)+','+str(learning_rate)+','+str(max_depth)+','+str(accuracy) + '\n'
            test_results.append(accuracy)
            fileOutput.write(line)
            fileOutput.flush()
            
fileOutput.close()

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(max_depths, train_results, 'b', label="Train Accuracy")
line2, = plt.plot(max_depths, test_results, 'r', label="Test Accuracy")
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel("Accuracy")
plt.xlabel("Tree Depth")
plt.savefig('gradient_depth.png')