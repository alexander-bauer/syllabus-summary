#!/usr/bin/python3

import sys, os
import nltk

if len(sys.argv) < 2:
    print("Please supply a filename.")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

# I borrowed some fuzzy matching code from StreamHacker.
# http://streamhacker.com/2011/10/31/fuzzy-string-matching-python/
stemmer = nltk.stem.PorterStemmer()
def normalize(string):
    words = nltk.tokenize.wordpunct_tokenize(string.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])

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
raw_sentences = nltk.sent_tokenize(data)
sentences = [nltk.pos_tag(nltk.word_tokenize(sentence)) \
    for sentence in raw_sentences]

# Define a grammar, and identify the Noun Pairs and Noun PhRases in the
# sentences.
# TODO: Look into using exclusive grammars to discard prepositional
# phrases, and such.
chunk_parser = nltk.RegexpParser("""
NP: {<PRP|NN|NNP|CD>+}
NPR: {((<DT|PRP\$>)?<JJ>*(<NP|CC>)+)}
""")

trees = [chunk_parser.parse(sentence) for sentence in sentences]

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
            # Sort the list of keywords based on how closely they
            # compare to our subject candidate, along with the exactly
            # how close they are to the subject letterwise, and select
            # the first element.
            # TODO: This is obscure. If anyone else has the misfortune
            # of reading this code, I apologize. I should not be writing
            # Haskell in Python.
            distance, keyword = sorted([pair_with_f(
                edit_distance_to(as_string), keyword) for keyword in
                keywordlist])[0]

            # If the distance is not over the threshold, mark this as
            # the subject.
            if distance <= compare_threshold:
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
