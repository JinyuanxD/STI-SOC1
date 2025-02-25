import csv
import random

import os
import os.path
import re

from collections import Counter

import pandas as pd
import numpy as np

# Function to get file size (.asm and .byte files)
def getFileSize(folder, id):
    path = folder + "/" + id

    size=[]
    if os.path.exists(path + ".asm"):
        asmSize = os.path.getsize(path + ".asm")
    else:
        return False
    if os.path.exists(path + ".bytes"):
        bytesSize = os.path.getsize(path + ".bytes")
    else:
        return False
    
    size = []
    size.append(asmSize)
    size.append(bytesSize)   
    
    return size

# This program is used to get the file size of the
# .asm and .bytes files of the malware

folder = r"D:/STI Dataset/train"
labels = r"F:/datasets/trainLabels.csv"
outputName = r"F:/datasets/train/file_sizes.csv"

allMalware = pd.read_csv(labels)
totalMalware = len(allMalware)

results = []
# Read all the ID in the dataframe
count = 0
for index, row in allMalware.iterrows():
    
    # All results will be stored in this array
    # [malwareId, asmSize, byteSize, class]

    resultRow = []
    if(getFileSize(folder, row['Id'])):
        size = getFileSize(folder, row['Id'])
        resultRow.append(row['Id'])
        resultRow.append(size[0])
        resultRow.append(size[1])
        resultRow.append(row['Class'])

        # Save file size row to results array
        results.append(resultRow)

    # Print Percentage done
    count += 1
    percentage = (float(count)/totalMalware)*100
    print("Percentage Done: " + str(percentage))  

print(np.asarray(results))

# Save malware into a CSV File
fileColumns = ['id', 'asm_size', 'bytes_size', 'category']
values = np.asarray(results)
df = pd.DataFrame(data=values, columns=fileColumns)

df.to_csv(outputName, index=False)