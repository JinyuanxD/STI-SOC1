from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

import pandas as pd

# Function to separate the dataset into columns to fit in the prediction model
# Train_X and test_y are the Malware ID and Features
# Test_X and test_y are the actual malware family value (1 - 9)
# 
# Function will separate the dataset into 70% to train the model
# The other 30% will be used to validate the model's accuracy
def prepareDataset(labeledCsv):
    
    df = pd.read_csv(labeledCsv)
    ds = df.values
    train_X, test_X, train_y, test_y = train_test_split(ds[:,1:-1], ds[:,-1], test_size=0.3, random_state=0) 
    return (train_X, train_y, test_X, test_y)


Dataset = r"F:\Security Technology and Innovation - STI\Malware Codeset\STI-MalwareClassifier\datasets\features_combine.csv"
(train_X, train_y, test_X, test_y) = prepareDataset(Dataset)

# K-Nearest Neighbour
knn = KNeighborsClassifier(n_neighbors = 3)

# Fit the model with the training data
print("\nK-Nearest Neighbour\n")
train_y = train_y[:].astype(int)
knn.fit(train_X, train_y)

# Accuracy of training data
yhat = knn.predict(train_X)
yhat = yhat[:].astype(int)

print("Training Stats")
print("Classification Accuracy: " + str(metrics.accuracy_score(yhat, train_y)) + "\n")

# Validate model with test data
yhat = knn.predict(test_X)
test_y = test_y[:].astype(int)
yhat = yhat[:].astype(int)

print("Testing Stats")
print("Classification Accuracy: " + str(metrics.accuracy_score(yhat, test_y)))
