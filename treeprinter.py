#!/usr/bin/python3

import sys
import parser.tokenize
import parser.grammar

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

raw_sentences = parser.tokenize.split_phrases(data)
sentences = parser.tokenize.part_of_speech_tag(
        parser.tokenize.split_words(raw_sentences))

trees = parser.grammar.identify_constructs(sentences)

for index, tree in enumerate(trees):
    print("===\n%s\n%s\n\n" % (raw_sentences[index].replace('\n', ' ') \
        .strip(), tree))
