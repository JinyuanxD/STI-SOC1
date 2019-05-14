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

---

## Approach

We will have to first extract features of the malware from the bytes and asm files given. After extracting the features, we will use K-Nearest Neighbour (KNN) Algorithm to group malwares into different categories based on their features.

Below are the list of features to extract:
1. File Size of File (Byte and ASM)

