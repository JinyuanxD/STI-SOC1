import csv
import random
import os
import os.path
import re

from collections import Counter

import pandas as pd
import numpy as np

def getSamples(seed, bucketSize, descriptorPath):    
    samplesStruct = {'my_hash':{}, 'my_list':[]}
    
    random.seed(seed)
    
    csvfile = open(descriptorPath, 'rb')
    samples = csv.reader(csvfile, delimiter=',')
    
    for row in samples:
        
        sampleName = row[0]
        sampleCategory = row[1]
        if sampleCategory == 'Class':
            continue
            
        samplesStruct['my_hash'][sampleName] = sampleCategory
        samplesStruct['my_list'].append(sampleName)
        
    if (bucketSize > len(samplesStruct['my_list'])):
        bucketSize = len(samplesStruct['my_list'])
        
    samplesStruct['my_list'] = random.sample(samplesStruct['my_list'], bucketSize)
    
    return samplesStruct
    
def getStats_FromFile(folder, filename):
    
    filePath = folder + "/" + filename + ".asm"
    
    importModuleFilter = re.compile(
        "^(\.idata):([0-9a-zA-Z]{8,8})"
        "\t+;\sImports from\s(.*)"
    )
    
    importedModulesCounter = Counter()

    if os.path.exists(filePath):
        inputLines = open(filePath).readlines()

        for line in inputLines:
            match1 = importModuleFilter.search(line)
            if (match1):
                module = match1.group(3)
                importedModulesCounter[module.upper()] += 1

    return importedModulesCounter

def buildLexicon(corpus):
    lexicon = set()
    for doc in corpus:
        if 'counter' in doc:
            bagOfWords = doc['counter']
            if bagOfWords != None:
                wordsList = list(bagOfWords)
                #print wordsList
                for word in wordsList:
                    lexicon.update([word])
            
    return lexicon 
    
def termFreq(term, doc):
    if (doc != None):
        for myTuple in doc:
            if myTuple[0] == term:
                return myTuple[1]
    return 0

def launch(theSeed, samplesNumber, descriptorPath, folder, outputName):
    samples = getSamples(theSeed, samplesNumber, descriptorPath)
    samplesDone=0
    
    statsList = []   
    for sampleId in samples['my_list']:
        importedModules = getStats_FromFile(folder, sampleId)

        struct = {}
        struct['id'] = sampleId
        struct['counter'] = importedModules
        statsList.append(struct)
        
        pcDone = (float(samplesDone)/samplesNumber)*100
        print "Samples parsed Percent: "+str(pcDone)
        samplesDone += 1
        
    matrix = []
    vocabulary = buildLexicon(statsList)
    for docStruct in statsList:
        doc = docStruct['counter'].most_common()
        sampleId = docStruct['id']
        
        tf_vector = [termFreq(word, doc) for word in vocabulary]
        tf_vector.insert(0, sampleId)
        tf_vector.append(samples['my_hash'][sampleId])    
        matrix.append(tf_vector)
        
    vocabulary = list(vocabulary)
    vocabulary.insert(0, 'id')
    vocabulary.append('category')
    
    docTermMatrix = (vocabulary, matrix)
    
    vocabulary, nDocTermMatrix = np.asarray(docTermMatrix)
    df = pd.DataFrame(data=nDocTermMatrix, columns=vocabulary)

    df.to_csv(outputName, index=False)
    
def extractTrainFeatures():
    seed = "my_seed"    
    folder = r"D:/STI Dataset/train"
    samplesNumber = 11000
    descriptor = r"F:/datasets/trainLabels.csv"
    outputName = r"F:/datasets/train/imports_count_all.csv"
    
    launch(seed, samplesNumber, descriptor, folder,outputName)

extractTrainFeatures()