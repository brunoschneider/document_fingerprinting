# coding: utf-8

from __future__ import division
import itertools
import math

import nltk

def simpsons_index(trecho):
    words = [w.lower() for w in trecho]
    n2 = len(words)
    den = n2 * (n2 - 1)
    per = itertools.permutations(words, 2)
    counter = 0
    for elemento in per:
        if elemento[0] == elemento[1]:
            counter += 1
    simpsonsindex = counter / den
    inv_simpsonsindex = 1 / simpsonsindex
    return inv_simpsonsindex

def lexical_diversity(text):
    words = [w.lower() for w in text]
    return len(set(words)) / len(words)

def hapax_legomena(text):
    words = [w.lower() for w in text]
    N = len(words)
    V = len(set(words))
    num = 100 * (math.log(N, 10))
    t = nltk.FreqDist(words)
    V1 = len(t.hapaxes())
    den = 1 - (V1 / V)
    return num / den
