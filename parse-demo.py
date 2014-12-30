#!/usr/bin/python3

import sys, os
import nltk
import parser.tokenize
import parser.compare
import parser.grammar

if len(sys.argv) < 2:
    print("Please supply a filename.")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

# Instantiate a hacky-curried function so we can use edit distance to
# compare strings. Note that the second string is not normalized.
def edit_distance_to(string1):
    string1 = normalize(string1)

    def edit_distance(string2):
        return nltk.edit_distance(string1, string2)

    return edit_distance

# Returns a tuple of (f(arg), arg)
# TODO: This whole mess should be less functional
def pair_with_f(f, arg):
    return (f(arg), arg)

# Declare a list of keywords we might be looking for in the subjects of
# sentences in input.
compare_threshold = 3
keywordlist = [ "course id", "start time", "end time", "meeting days",
"email", "name" ]

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

    # Now, parse the key elements, identifying the subject and
    # object(s).
    print("Key elements:")
    subjectkw = None
    objects = []
    for subtree in tree.subtrees(filter = lambda t: t.label() == 'NP'):

        # Return the element to string form, and then try to compare it
        # with the keyword list, if a subject has not already been
        # found.
        as_string = ' '.join(word for (word, tag) in subtree.leaves())

        if not subjectkw:
            # Define a convenience function for comparing one
            # already-normalized string with many others.
            def compare_to_subj(string):
                return parser.compare.compare_metric(as_string, string,
                        normalized1 = True)

            # Sort the list of keywords based on how closely they
            # compare to our subject candidate, along with the exactly
            # how close they are to the subject letterwise, and select
            # the first element.

            keyword = sorted(keywordlist, key = compare_to_subj)[0]
            # If even the best keyword doesn't compare to the subject,
            # drop it.
            if parser.compare.compare(as_string, keyword, normalized1 =
                    True):
                subjectkw = keyword
                sentencepart = 'Subject'
            else:
                sentencepart = 'Unusable'

        else:
            # Here, we might try to parse the data further, according to
            # exactly what information we're looking for from the
            # object, such as a time, a date, or an email address. But
            # we won't, in this demo.
            objects.append(as_string)
            sentencepart = 'Object'

        print("  %-16s - %s" % (as_string, sentencepart))

    # Record the subject and objects from this sentence, if they are
    # both nonempty.
    if subjectkw and len(objects) > 0:
        information_gathered[subjectkw] = objects


# At the end, print out information we successfully gathered.
print("\n\n=======\nInformation Gathered:\n")
for field, data in information_gathered.items():
    print("%s: %s" % (field, ', '.join(data)))
