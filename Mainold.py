import re
import string
from math import log10

import unidecode


def trainUnigramModel(path):
    l = 27
    C = [.5 for y in range(l)]
    s = open(path, 'r').read()
    unigrams = extractUnigrams(s)
    for ug in unigrams:
        C[charIndex(ug)] += 1
    return C


def trainBigramModel(path):
    l = 27
    C = [[.5 for x in range(l)] for y in range(l)]
    s = open(path, 'r').read()
    bigrams = extractBigrams(s)
    for bg in bigrams:
        C[charIndex(bg[0])][charIndex(bg[1])] += 1
    return C


def extractBigrams(s):
    s = unidecode.unidecode(s).lower().replace('.', ' ')
    s = re.compile('[^a-zA-Z ]').sub('', s)
    bigrams = list()
    for i in range(len(s) - 1):
        bigrams.append(s[i] + s[i + 1])
    return bigrams


def extractUnigrams(s):
    s = unidecode.unidecode(s).lower().replace('.', ' ')
    s = re.compile('[^a-zA-Z]').sub('', s)
    unigrams = list()
    for c in s:
        unigrams.append(c)
    return unigrams


def charIndex(c):
    alphabet = list(string.ascii_lowercase)
    alphabet.append(' ')
    return alphabet.index(c)


def testUni(s, num, C_En, C_Fr, C_oth):
    unigrams = extractUnigrams(s)
    probability_En = 0
    probability_Fr = 0
    probability_oth = 0
    sum_C_En = 0
    sum_C_Fr = 0
    sum_C_oth = 0
    l = 27

    for c in C_En:
        sum_C_En += c
    for c in C_Fr:
        sum_C_Fr += c
    for c in C_oth:
        sum_C_oth += c

    output = s + '\n\n' + 'UNIGRAM MODEL:\n'

    print(s)

    for ug in unigrams:
        probability_En += log10(C_En[charIndex(ug)] / sum_C_En)
        probability_Fr += log10(C_Fr[charIndex(ug)] / sum_C_Fr)
        probability_oth += log10(C_oth[charIndex(ug)] / sum_C_oth)
        output += '\nUNIGRAM: ' + ug + '\n'
        output += 'ENGLISH: P(' + ug + ') = ' + \
                  str(log10(C_En[charIndex(ug)] / sum_C_En)) + ' ==>  log prob of sentence so far: ' + str(
            probability_En) + '\n'
        output += 'FRENCH: P(' + ug + ') = ' + \
                  str(log10(C_Fr[charIndex(ug)] / sum_C_Fr)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Fr) + '\n'
        output += 'OTHER: P(' + ug + ') = ' + \
                  str(log10(C_oth[charIndex(ug)] / sum_C_oth)) + ' ==>  log prob of sentence so far: ' + str(
            probability_oth) + '\n'

    if probability_En >= max(probability_Fr, probability_oth):
        output += '\nAccording to the unigram model, the sentence is in English'
        print('According to the unigram model, the sentence is in English')
    elif probability_Fr >= max(probability_En, probability_oth):
        output += '\nAccording to the unigram model, the sentence is in French'
        print('According to the unigram model, the sentence is in French')
    else:
        output += '\nAccording to the unigram model, the sentence is in German'
        print('According to the unigram model, the sentence is in German')

    with open("out" + str(num) + ".txt", "w") as text_file:
        text_file.write(output)


def testBi(s, num, C_En, C_Fr, C_oth):
    bigrams = extractBigrams(s)
    probability_En = 0
    probability_Fr = 0
    probability_oth = 0
    sum_C_En = 0
    sum_C_Fr = 0
    sum_C_oth = 0
    l = 27

    for i in range(l):
        for j in range(l):
            sum_C_En += C_En[i][j]
            sum_C_Fr += C_Fr[i][j]
            sum_C_oth += C_oth[i][j]

    output = '\n' + 20 * '-' + '\n' + 'BIGRAM MODEL:\n'

    for bg in bigrams:
        probability_En += log10(C_En[charIndex(bg[0])][charIndex(bg[1])] / sum_C_En)
        probability_Fr += log10(C_Fr[charIndex(bg[0])][charIndex(bg[1])] / sum_C_Fr)
        probability_oth += log10(C_oth[charIndex(bg[0])][charIndex(bg[1])] / sum_C_oth)
        output += '\nBIGRAM: ' + bg[0] + bg[1] + '\n'
        output += 'ENGLISH: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_En[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_En)) + ' ==>  log prob of sentence so far: ' + str(
            probability_En) + '\n'
        output += 'FRENCH: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_Fr[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_Fr)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Fr) + '\n'
        output += 'OTHER: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_oth[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_oth)) + ' ==>  log prob of sentence so far: ' + str(
            probability_oth) + '\n'

    if probability_En >= max(probability_Fr, probability_oth):
        output += '\nAccording to the bigram model, the sentence is in English'
        print('According to the bigram model, the sentence is in English')
    elif probability_Fr >= max(probability_En, probability_oth):
        output += '\nAccording to the bigram model, the sentence is in French'
        print('According to the bigram model, the sentence is in French')
    else:
        output += '\nAccording to the bigram model, the sentence is in the German'
        print('According to the bigram model, the sentence is in German')

    print('\n')

    with open("out" + str(num) + ".txt", "a") as text_file:
        text_file.write(output)


def run():
    # EnPath = input("Enter the name of English training set:\n")
    # FrPath = input("Enter the name of French training set:\n")
    # othPath = input("Enter the name of other set:\n")
    # testSetPath = input("Enter the name of the file containing the sentences to be classified:\n")
    EnPath = 'English.txt'
    FrPath = 'French.txt'
    othPath = 'German.txt'
    testSetPath = 'test.txt'

    C_uni_En = trainUnigramModel(EnPath)
    C_uni_Fr = trainUnigramModel(FrPath)
    C_uni_oth = trainUnigramModel(othPath)

    C_bi_En = trainBigramModel(EnPath)
    C_bi_Fr = trainBigramModel(FrPath)
    C_bi_oth = trainBigramModel(othPath)

    sentences = open(testSetPath, 'r').readlines()

    counter = 1
    for s in sentences:
        testUni(s.strip(), counter, C_uni_En, C_uni_Fr, C_uni_oth)
        testBi(s.strip(), counter, C_bi_En, C_bi_Fr, C_bi_oth)
        counter += 1


run()
