from os import listdir
import string
import re
import numpy as np
import os



# clean a list of lines
def clean_lines(lines):
    cleaned = list()
    # prepare a translation table to remove punctuation
    table = str.maketrans('', '', string.punctuation)
    for line in lines:

        # replace tokens with numbers in them to isnumber
        line = re.sub('\d+', 'isnumber', line)
        # tokenize on white space
        line = line.split()
        # convert to lower case
        line = [word.lower() for word in line]
        # remove punctuation from each token
        line = [w.translate(table) for w in line]

        line = [word for word in line if word.isalpha()]
        # store as string
        cleaned.append(' '.join(line))
    # remove empty strings
    cleaned = [c for c in cleaned if len(c) > 0]
    return cleaned


def load_word_embeddings():
    word_embeddings = {}
    f = open('/Users/lakshkotian/Documents/ly_final/Text summarization/data/glove/glove.6B.300d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs

    f.close()
    return word_embeddings

def get_sentence_vectors(word_embeddings,sentences):
    sentence_vectors=[]
    for sentence in sentences:
        if len(sentence)>0:
            v = sum([word_embeddings.get(w, np.zeros((300,))) for w in sentence.split()]) / (len(sentence.split()) + 0.001)
        else:
            print("len sentence not greater than 0")
            v = np.zeros((300,))
        sentence_vectors.append(v)
    return sentence_vectors

def get_summary_from_indices(summary_indices,sentences):
    summary=[]
    for i,sentence in sentences:
        if i in summary_indices:
            summary.append(sentence)
    return '.'.join(summary)
