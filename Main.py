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


def testUni(s, num, C_En, C_Fr, C_Ge, C_It, C_Sp):
    unigrams = extractUnigrams(s)
    probability_En = 0
    probability_Fr = 0
    probability_Ge = 0
    probability_It = 0
    probability_Sp = 0
    sum_C_En = 0
    sum_C_Fr = 0
    sum_C_Ge = 0
    sum_C_It = 0
    sum_C_Sp = 0
    l = 27

    for c in C_En:
        sum_C_En += c
    for c in C_Fr:
        sum_C_Fr += c
    for c in C_Ge:
        sum_C_Ge += c
    for c in C_It:
        sum_C_It += c
    for c in C_Sp:
        sum_C_Sp += c

    output = s + '\n\n' + 'UNIGRAM MODEL:\n'

    print(s)

    for ug in unigrams:
        probability_En += log10(C_En[charIndex(ug)] / sum_C_En)
        probability_Fr += log10(C_Fr[charIndex(ug)] / sum_C_Fr)
        probability_Ge += log10(C_Ge[charIndex(ug)] / sum_C_Ge)
        probability_It += log10(C_It[charIndex(ug)] / sum_C_It)
        probability_Sp += log10(C_Sp[charIndex(ug)] / sum_C_Sp)
        output += '\nUNIGRAM: ' + ug + '\n'
        output += 'ENGLISH: P(' + ug + ') = ' + \
                  str(log10(C_En[charIndex(ug)] / sum_C_En)) + ' ==>  log prob of sentence so far: ' + str(
            probability_En) + '\n'
        output += 'FRENCH: P(' + ug + ') = ' + \
                  str(log10(C_Fr[charIndex(ug)] / sum_C_Fr)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Fr) + '\n'
        output += 'GERMANIC: P(' + ug + ') = ' + \
                  str(log10(C_Ge[charIndex(ug)] / sum_C_Ge)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Ge) + '\n'
        output += 'ITALIAN: P(' + ug + ') = ' + \
                  str(log10(C_It[charIndex(ug)] / sum_C_It)) + ' ==>  log prob of sentence so far: ' + str(
            probability_It) + '\n'
        output += 'SPANISH: P(' + ug + ') = ' + \
                  str(log10(C_Sp[charIndex(ug)] / sum_C_Sp)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Sp) + '\n'

    if probability_En >= max(probability_Fr, probability_Ge, probability_It, probability_Sp):
        output += '\nAccording to the unigram model, the sentence is in English'
        print('According to the unigram model, the sentence is in English')
    elif probability_Fr >= max(probability_En, probability_Ge, probability_It, probability_Sp):
        output += '\nAccording to the unigram model, the sentence is in French'
        print('According to the unigram model, the sentence is in French')
    elif probability_Ge >= max(probability_En, probability_Fr, probability_It, probability_Sp):
        output += '\nAccording to the unigram model, the sentence is in Germanic'
        print('According to the unigram model, the sentence is in Germanic')
    elif probability_It >= max(probability_En, probability_Fr, probability_Ge, probability_Sp):
        output += '\nAccording to the unigram model, the sentence is in Italian'
        print('According to the unigram model, the sentence is in Italian')
    else:
        output += '\nAccording to the unigram model, the sentence is in Spanish'
        print('According to the unigram model, the sentence is in Spanish')

    with open("out" + str(num) + ".txt", "w") as text_file:
        text_file.write(output)


def testBi(s, num, C_En, C_Fr, C_Ge, C_It, C_Sp):
    bigrams = extractBigrams(s)
    probability_En = 0
    probability_Fr = 0
    probability_Ge = 0
    probability_It = 0
    probability_Sp = 0
    sum_C_En = 0
    sum_C_Fr = 0
    sum_C_Ge = 0
    sum_C_It = 0
    sum_C_Sp = 0
    l = 27

    for i in range(l):
        for j in range(l):
            sum_C_En += C_En[i][j]
            sum_C_Fr += C_Fr[i][j]
            sum_C_Ge += C_Ge[i][j]
            sum_C_It += C_It[i][j]
            sum_C_Sp += C_Sp[i][j]

    output = '\n' + 20 * '-' + '\n' + 'BIGRAM MODEL:\n'

    for bg in bigrams:
        probability_En += log10(C_En[charIndex(bg[0])][charIndex(bg[1])] / sum_C_En)
        probability_Fr += log10(C_Fr[charIndex(bg[0])][charIndex(bg[1])] / sum_C_Fr)
        probability_Ge += log10(C_Ge[charIndex(bg[0])][charIndex(bg[1])] / sum_C_Ge)
        probability_It += log10(C_It[charIndex(bg[0])][charIndex(bg[1])] / sum_C_It)
        probability_Sp += log10(C_Sp[charIndex(bg[0])][charIndex(bg[1])] / sum_C_Sp)
        output += '\nBIGRAM: ' + bg[0] + bg[1] + '\n'
        output += 'ENGLISH: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_En[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_En)) + ' ==>  log prob of sentence so far: ' + str(
            probability_En) + '\n'
        output += 'FRENCH: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_Fr[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_Fr)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Fr) + '\n'
        output += 'GERMANIC: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_Ge[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_Ge)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Ge) + '\n'
        output += 'ITALIAN: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_It[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_It)) + ' ==>  log prob of sentence so far: ' + str(
            probability_It) + '\n'
        output += 'SPANISH: P(' + bg[1] + '|' + bg[0] + ') = ' + \
                  str(log10(C_Sp[charIndex(bg[0])][
                                charIndex(bg[1])] / sum_C_Sp)) + ' ==>  log prob of sentence so far: ' + str(
            probability_Sp) + '\n'

    if probability_En >= max(probability_Fr, probability_Ge, probability_It, probability_Sp):
        output += '\nAccording to the bigram model, the sentence is in English'
        print('According to the bigram model, the sentence is in English')
    elif probability_Fr >= max(probability_En, probability_Ge, probability_It, probability_Sp):
        output += '\nAccording to the bigram model, the sentence is in French'
        print('According to the bigram model, the sentence is in French')
    elif probability_Ge >= max(probability_En, probability_Fr, probability_It, probability_Sp):
        output += '\nAccording to the bigram model, the sentence is in Germanic'
        print('According to the bigram model, the sentence is in Germanic')
    elif probability_It >= max(probability_En, probability_Fr, probability_Ge, probability_Sp):
        output += '\nAccording to the bigram model, the sentence is in Italian'
        print('According to the bigram model, the sentence is in Italian')
    else:
        output += '\nAccording to the bigram model, the sentence is in Spanish'
        print('According to the bigram model, the sentence is in Spanish')

    print('\n')

    with open("out" + str(num) + ".txt", "a") as text_file:
        text_file.write(output)


def run():
    EnPath = 'English.txt'
    FrPath = 'French.txt'
    GePath = 'Germanic.txt'
    ItPath = 'Italian.txt'
    SpPath = 'Spanish.txt'
    testSetPath = 'test.txt'

    C_uni_En = trainUnigramModel(EnPath)
    C_uni_Fr = trainUnigramModel(FrPath)
    C_uni_Ge = trainUnigramModel(GePath)
    C_uni_It = trainUnigramModel(ItPath)
    C_uni_Sp = trainUnigramModel(SpPath)

    C_bi_En = trainBigramModel(EnPath)
    C_bi_Fr = trainBigramModel(FrPath)
    C_bi_Ge = trainBigramModel(GePath)
    C_bi_It = trainBigramModel(ItPath)
    C_bi_Sp = trainBigramModel(SpPath)

    sentences = open(testSetPath, 'r').readlines()

    counter = 1
    for s in sentences:
        testUni(s.strip(), counter, C_uni_En, C_uni_Fr, C_uni_Ge, C_uni_It, C_uni_Sp)
        testBi(s.strip(), counter, C_bi_En, C_bi_Fr, C_bi_Ge, C_bi_It, C_bi_Sp)
        counter += 1


run()
