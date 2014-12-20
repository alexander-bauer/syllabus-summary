#!/usr/bin/python3

import sys, os
import nltk

if len(sys.argv) < 2:
    print("Please supply a filename.")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

# Break the input down into sentences, then into words, and position tag
# those words.
sentences = [nltk.pos_tag(nltk.word_tokenize(sentence)) \
    for sentence in nltk.sent_tokenize(data)]

# Define a grammar, and identify the noun phrases in the sentences.
chunk_parser = nltk.RegexpParser(r"NP: {<DT>?<JJ>*<NN>}")

trees = [chunk_parser.parse(sentence) for sentence in sentences]

for tree in trees:
    print(tree)
    #for subtree in tree.subtrees(filter = lambda t: t.label() == 'NP'):
        #print(subtree)
