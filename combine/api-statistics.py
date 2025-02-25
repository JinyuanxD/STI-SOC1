import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def filterColumns(csv, category):
    # Read the CSV File, get all the columns that is the category == x (where x is the malware family number)
    # After that, remove all columns with no zeroes in it
    apiData = pd.read_csv(csv)
    apiData = apiData.loc[apiData["category"] ==  category]
    apiData = apiData.loc[:, (apiData != 0).any(axis=0)]

    # Save API Name and Total Calls to Array
    apiList = apiData.columns.tolist()
    
    apiStats = []
    
    repeat = len(apiList)
    for i in range (1, repeat-1):
        apiName = apiList[i]
        apiCount = apiData[apiName].sum()
        apiStats.append([apiName,apiCount])

    # Save to CSV File
    folder = "F:/Security Technology and Innovation - STI/Malware Codeset/STI-MalwareClassifier/statistics/"
    outputFile = "family" + str(category) + ".csv"
    
    outputName = folder + outputFile
    print(outputName)

    df = pd.DataFrame(apiStats, columns = ['API Call', 'Count'])
    df.to_csv(outputName, index=False)

    ## Plot a bar graph
    #title = "API Calls for Malware Family " + str(category)

    ##objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    #y_pos = np.arange(len(apiCall))
    ##performance = [10,8,6,4,2,1]

    #plt.bar(y_pos, apiCallCount, align='center')
    #plt.xticks(y_pos, apiCall)
    #plt.ylabel('Frequency')
    #plt.title(title)
    #plt.rcParams['figure.figsize'] = (30,20)
    #plt.show()

# === Main ===

csv = r"F:\Security Technology and Innovation - STI\Malware Codeset\STI-MalwareClassifier\datasets\api_calls.csv"

for category in range (1,9):
    filterColumns(csv,category)
