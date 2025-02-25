import csv
import random
import os
import os.path
import re

import pandas as pd
import numpy as np

from collections import Counter

def getSamples(seed, bucketSize, descriptorPath):
    samplesStruct = {'my_hash':{}, 'my_list':[]}
    
    random.seed(seed)
    
    csvfile = open(descriptorPath, 'rb')
    samples = csv.reader(csvfile, delimiter=',')
    
    for row in samples:
        
        sampleName = row[0]
        sampleCategory = row[1]
        samplesStruct['my_hash'][sampleName] = sampleCategory
        samplesStruct['my_list'].append(sampleName)
        
    if (bucketSize > len(samplesStruct['my_list'])):
        bucketSize = len(samplesStruct['my_list'])
    samplesStruct['my_list'] = random.sample(samplesStruct['my_list'], bucketSize)
    
    return samplesStruct
    
def getImportedSysCalls(folder, filename):
    
    filePath = folder + "/" + filename + ".asm"
    
    sysCallFilterIDataSection = re.compile(
        "^(\.idata):([0-9a-zA-Z]{8,8})"
        "\s(.*)extrn\s(.*):dword"
    )
    
    importedSysCalls = []
    
    if os.path.exists(filePath):
        inputLines = open(filePath).readlines()

        for line in inputLines:
            match1 = sysCallFilterIDataSection.search(line)
            if (match1):
                syscall = match1.group(4)
                importedSysCalls.append(syscall)
                
    return importedSysCalls

def extractSysCalls(folder, filename, importedSyscallsList, threshold):
    
    sysCallCounter = Counter()
    
    filePath = folder + "/" + filename + ".asm"
    
    instructionFilter = re.compile(
        "^(\.text|\.icode):([0-9a-zA-Z]{8,8})"
        "("
          "(\s[0-9a-zA-Z]{2,2}[\+]{0,1})+(\t+)(\s*)"
          "("
            "(?!\s*;)(.*)"
          ")"
        ")"
    )
    
    callsFilter = re.compile(
        "^\s*call(\t|\s)*(ds:)*(.*)"
    )

    if os.path.exists(filePath):
        inputLines = open(filePath).readlines()

        for line in inputLines:
            match1 = instructionFilter.search(line)
            if (match1):
                instructionLine = match1.group(7)
                match2 = callsFilter.search(instructionLine)
                if (match2):
                    callOperand = match2.group(3)
                    
                    if (not callOperand.startswith('_')):
                        if any(callOperand in s for s in importedSyscallsList):                        
                            #print callOperand + " - " + instructionLine
                            sysCallCounter[callOperand] += 1
    
    sysCallCounter = Counter(el for el in sysCallCounter.elements() if sysCallCounter[el] >= threshold)

    return sysCallCounter

def simpleNormalizeBag(bag):
    normalizedBag = []
    
    if len(bag) > 0:
        labels, values = zip(*bag)
        totalSum = float(sum(values))
        
        for tpl in bag:
            occurrences = tpl[1]
            normalizedOccurrences = occurrences/totalSum
            normalizedTuple = (tpl[0], normalizedOccurrences)
            normalizedBag.append(normalizedTuple)
        
    return normalizedBag
        
def getSysCallsCount_FromFile(folder, filename, threshold):
    importedSyscallsList = getImportedSysCalls(folder, filename)
    sysCallsStats = extractSysCalls(folder, filename, importedSyscallsList, threshold)
    return sysCallsStats

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

def loadAndGetWin32APIFilters():
    
    filepath = "win32_api_filter_functions.txt"
    apiCalls = set([])
    
    if os.path.exists(filepath):
        inputLines = open(filepath).readlines()
        for line in inputLines:
            strippedLine = line.strip()
            if strippedLine != '':
                apiCalls.add(strippedLine)
                
    
    return sorted(list(apiCalls))

def filterWin32ApiCalls(calls):
    outputCalls = []
    filterCalls = set(loadAndGetWin32APIFilters())
    
    for call in calls:
        if call in filterCalls:
            outputCalls.append(call)
            
    return outputCalls
    
def filterNonFilter(calls):
    return calls
    
# -----------------------------------------------------------------------------

def launch(theSeed, samplesNumber, threshold, win32CallFilter, descriptorPath, folder, outputName):
    samples = getSamples(theSeed, samplesNumber, descriptorPath)
    doneSamples = 0
    
    statsList = []
    for sampleId in samples['my_list']:
        fileSysCallsStats = getSysCallsCount_FromFile(folder, sampleId, threshold)
        sysCallStruct = {}
        #sysCallStruct['counter'] = fileSysCallsStats.most_common()
        sysCallStruct['counter'] = fileSysCallsStats
        sysCallStruct['id'] = sampleId
        statsList.append(sysCallStruct)
        
        pcDone = (float(doneSamples)/samplesNumber)*100
        doneSamples+=1
        print "Extracting Syscalls. Percent finished: " + str(pcDone)

    matrix = []
    vocabulary = buildLexicon(statsList)
    vocabulary = win32CallFilter(vocabulary)

    statsLen = len(statsList)
    statsDone = 0
    for struct in statsList:
        doc = struct['counter'].most_common()
        sampleId = struct['id']
       
        tf_vector = [termFreq(word, doc) for word in vocabulary]
        tf_vector.insert(0, sampleId)
        tf_vector.append(samples['my_hash'][sampleId])    
        matrix.append(tf_vector)
        
        pcDone = (float(statsDone)/statsLen)*100
        statsDone += 1
        print "Calculating Term Matrix. Percent finished: " + str(pcDone)
        
    vocabulary = list(vocabulary)
    vocabulary.insert(0, 'id')
    vocabulary.append('category')
    
    docTermMatrix = (vocabulary, matrix)
    vocabulary, nDocTermMatrix = np.asarray(docTermMatrix)
    df = pd.DataFrame(data=nDocTermMatrix, columns=vocabulary)
    
    df.to_csv(outputName, index=False)
    
    print "Vocabulary Shape: " + str(np.shape(vocabulary))

# -----------------------------------------------------------------------------

def extractTrainFeatures():
    seed = "my_seed"    
    folder = r"D:/STI Dataset/train"
    samplesNumber = 11000
    descriptor = r"F:/datasets/trainLabels.csv"
    outputName = r"F:/datasets/train/win32_api_calls_1_filter_1.csv"
    
    #launch(seed, samplesNumber, 0, filterNonFilter, descriptor, folder, outputName)    
    launch(seed, samplesNumber, 0, filterWin32ApiCalls, descriptor, folder,outputName)
    
def extractTestFeatures():
    seed = "my_seed"    
    folder = "D:/STI Dataset/test"
    samplesNumber = 11000
    descriptor = r"F:/datasets/testLabels.csv"
    outputName = r"F:/datasets/test/win32_api_calls_1_filter_1.csv"
    
    #launch(seed, samplesNumber, 0, filterNonFilter, descriptor, folder, outputName)
    launch(seed, samplesNumber, 0, filterWin32ApiCalls, descriptor, folder,outputName)
    
# -----------------------------------------------------------------------------

extractTrainFeatures()
extractTestFeatures()
    

