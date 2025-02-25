# This python scripts is used to combine all the extracted features 
# And save it into a csv file

import pandas as pd
import numpy as np

file1 = r"F:/datasets/train/file_sizes.csv"
file2 = r"F:/datasets/train/api_calls.csv"
file3 = r"F:/datasets/train/imports_count.csv"
outputName = r"F:/datasets/features_combine.csv"

datasetA = pd.read_csv(file1)
datasetB = pd.read_csv(file2)
datasetC = pd.read_csv(file3)

# Function to merge both datasets together 
# and remove duplicated "category" columns

def CombineDatasets(fileA, fileB):
    mergeDataset = pd.merge(fileA, fileB, how='left', left_on='id', right_on='id')
    mergeDataset.rename(columns = {'category_y':'category'}, inplace=True)
    mergeDataset.drop('category_x', axis=1, inplace=True)

    return mergeDataset

combineDataset = CombineDatasets(datasetA, datasetB)
combineDataset = CombineDatasets(combineDataset, datasetC)

print(combineDataset.head())
print(np.shape(combineDataset))

combineDataset.to_csv(r"F:/datasets/features_combine.csv", index=False)