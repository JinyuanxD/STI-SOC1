from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import label_binarize
from sklearn import metrics
from sklearn.metrics import roc_curve, auc


import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


def prepareDataset(labeledCsv):
    
    df = pd.read_csv(labeledCsv)
    ds = df.values
    train_X, test_X, train_y, test_y = train_test_split(ds[:,1:-1], ds[:,-1], test_size=0.3, random_state=0)
    return (train_X, train_y, test_X, test_y)

Dataset = r"F:\Security Technology and Innovation - STI\Malware Codeset\STI-MalwareClassifier\datasets\features_combine.csv"
(train_X, train_y, test_X, test_y) = prepareDataset(Dataset)

# Since there are 9 classes of malware, we need to binarize them.
# E.g. Malware 4 will be [0, 0, 0, 1, 0, 0, 0, 0]
df = pd.read_csv(Dataset)
ds = df.values
category = np.asarray(df.pop("category"))
label = label_binarize(category, classes=[1,2,3,4,5,6,7,8,9])
n_classes = label.shape[1]


# Settings/Variables for Gradient Boostings
estimators_col = (100,)
learning_rates = (0.085,)
max_depths = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
#max_depths = (1,2,3)

train_results = []
test_results = []

for estimators in estimators_col:
    for learning_rate in learning_rates:
        for max_depth in max_depths:
            
            print("Gradient Boosting Classifier. Estimators: " + str(estimators) + ", Learning Rate: " + str(learning_rate) + ", max_depth: " + str(max_depth) +"\n")
            clf = GradientBoostingClassifier(n_estimators=estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=0)
            
            # Place 70% of the dataset into the model and train it
            print("Training")
            train_y = train_y[:].astype(int)
            clf.fit(train_X, train_y)
            
            # Accuracy of the model after training it
            train_pred = clf.predict(train_X)
            accuracy = metrics.accuracy_score(train_pred, train_y)
            print("Train Accuracy: " + str(accuracy) + "\n")
            
            # Store the training results into array
            train_results.append(accuracy)

            # Validate the model using the other 30% of the dataset
            print('Validate')
            yhat=clf.predict(test_X)
            test_y = test_y[:].astype(int)
            yhat = yhat[:].astype(int)
            
            accuracy = metrics.accuracy_score(yhat, test_y)
            
            # Accuracy of Test Data
            accuracy = metrics.accuracy_score(yhat, test_y)
            print("Test Accuracy: " + str(accuracy) + "\n")

            # Add test accuracy to array
            test_results.append(accuracy)

# Plot the graph based on the accuracy collected from each test.
# X Axis is the Tree Depth
# Y Axis is the Accuracy
#
# The first line (in blue) is the Training Accuracy
# The second line (in red) is the Testing Accuracy

from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(max_depths, train_results, 'b', label="Train Accuracy")
line2, = plt.plot(max_depths, test_results, 'r', label="Test Accuracy")
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel("Accuracy")
plt.xlabel("Tree Depth")
plt.savefig('gradient_depth1.png')