# Malware Classifier

We are given 2 types of files (hexdump and assembly file) of malware and are to categorise them into 9 different family types. We will build a model and use machine learning/AI to help categorise malwares into their different families.

The 9 Malware Families are stated below
1. Ramnit
2. Lollipop
3. Kelihos_ver3
4. Vundo
5. Simda
6. Tracur
7. Kelihos_ver1
8. Obfuscator.ACY
9. Gatak

## Approach

We will have to first extract features of the malware from the bytes and asm files given. After extracting the features, we will use K-Nearest Neighbour (KNN) Algorithm, Random Forest and Gradient Boosting classification algorithms to group malwares into different categories based on their features.

Below are the list of features to extract:
1. File Size of File (Byte and ASM)
2. DLL Imports
3. Common Win32 API Calls

## Settings
- Our K-Nearest neighbour was searching the nearby 3 neighbours (k=3)
- Our Random Forests has a total of 100 trees build
- Our gradient boosting have learning rate set to 0.085, max_depths set to 21 and Estimator Number of 100.

## Results
With a total of 586 features extracted from the dataset, the most accurate classifier was Gradient Boosting (Accuracy of 0.980374), follwed by Random Forests (Accuracy of 0.928549) and lastly K-Nearest Neighbour (Accuracy of 0.92486)

However, it is still worth it to fine tune the algorithm as the efficiency may vary based on the number of features used do the prediction. Our best bet is that both "Random Forests" and "Gradient Boosting" Classificaiton Algorithm are the most efficient.

## Usage
To run any of the script, open command prompt and type ```"python script.py"```

Remember to change the path of the dataset directory and the path you want to save the output file to.

The folder "Extract" contains the scripts to extract dataset, "Combine" contains the script to combine the dataset together and "Learn" is the classification algorithm.