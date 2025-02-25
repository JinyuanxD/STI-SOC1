from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
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

# Predefine Settings for Classifier
estimators_col = (100,)
learning_rates = (0.085,)
max_depths = (1,)

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
            
            # Validate the model using the other 30% of the dataset
            print("Validate")
            yhat=clf.predict(test_X)
            test_y = test_y[:].astype(int)
            yhat = yhat[:].astype(int)
            
            # Accuracy of Test Data
            accuracy = metrics.accuracy_score(yhat, test_y)
            print("Test Accuracy: " + str(accuracy) + "\n")


