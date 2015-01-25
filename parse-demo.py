#!/usr/bin/python3

import sys, os
import nltk
import parser.tokenize
import parser.compare
import parser.grammar
import parser.keyword as keyword
import parser.sentence
import parser.datatype as datatype

if len(sys.argv) < 2:
    print("Please supply a filename.")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

# Declare a list of keywords we might be looking for in the subjects of
# sentences in input.
compare_threshold = 3
keywordlist = keyword.KeywordList([
    keyword.Keyword("course id", "catalog id",
        datamodel = datatype.DataType(None, 1)),
    keyword.Keyword("start time", "begin time", "meeting time", "starts",
        datamodel = datatype.TimeData(1)),
    keyword.Keyword("end time", "ends",
        datamodel = datatype.TimeData(1)),
    keyword.Keyword("meeting days",
        datamodel = datatype.DataType(None, 7)),
    keyword.Keyword("email",
        datamodel = datatype.DataType(None, 1)),
    keyword.Keyword("name", "professor", "teacher",
        datamodel = datatype.DataType(None, 1))
    ])

# Keep a list of any usable information we gather.
information_gathered = {}

# Break the input down into sentences, then into words, and position tag
# those words.
raw_sentences = parser.tokenize.split_phrases(data)
sentences = parser.tokenize.part_of_speech_tag(
        parser.tokenize.split_words(raw_sentences))

trees = parser.grammar.identify_constructs(sentences)

for index, tree in enumerate(trees):
    print("===\nSentence: %s\nNoun phrases:" %
            raw_sentences[index].replace('\n', ' '))
    for subtree in tree.subtrees(filter = lambda t: t.label() == 'NPR'):
        print("  %s" % subtree)
    print(tree)

    # Now, parse the key elements, identifying the subject and
    # object(s).
    print("Key elements:")
    sentencemodel = parser.sentence.Sentence(keywordlist)
    for subtree in tree.subtrees(filter = lambda t: t.label() == 'N' or
            t.label() == 'V'):

        # Return the element to string form, and then try to compare it
        # with the keyword list, if a subject has not already been
        # found.
        as_string = ' '.join(word for (word, tag) in subtree.leaves())

        # If the subtree is a verb, then it cannot be an object, so try
        # to add it as a subject. Otherwise, add it as either.
        if subtree.label() == 'V':
            sentencepart = sentencemodel.new_subject(as_string)
        else:
            print(as_string)
            sentencepart = sentencemodel.include_word(as_string)

        if not sentencepart:
            sentencepart = 'Unusable'

        print("  %-16s - %s" % (as_string, sentencepart))

    # Record the subject and objects from this sentence, if they are
    # both nonempty.
    if sentencemodel.keyword != None and len(sentencemodel.data) > 0:
        information_gathered[sentencemodel.keyword.primary] = \
            sentencemodel.data


# At the end, print out information we successfully gathered.
print("\n\n=======\nInformation Gathered:\n")
for field, data in information_gathered.items():
    print("%s: %s" % (field, data))
