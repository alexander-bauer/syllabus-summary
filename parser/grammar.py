import nltk

# Define a grammar, and identify the Noun Pairs and Noun PhRases in the
# sentences.
# TODO: Look into using exclusive grammars to discard prepositional
# phrases, and such.
_chunk_parser_ = nltk.RegexpParser(r"""
EMAIL: {<NN><:><JJ>}
V: {<RB|RBR|RBS>*<VB|VBD|VBN|VBP|VBZ>}
N: {<NN|NNS|NNP|NNPS|CD|EMAIL>+}
PPR: {<IN>}
NP: {<DT|PRP|PRP\$>?<JJ>*<N>?(<,>?<CC>?<N>)*}
VP: {<V><PPR>?<NP>?}
INDEP: {(<NP><VP>|<VP><NP>)}
""")

def identify_constructs(sentences):
    # If we are only given a single sentence, wrap it in a list.
    if len(sentences) > 0 and type(sentences[0]) != list:
        sentences = [sentences]

    return [_chunk_parser_.parse(sentence) for sentence in sentences]

def independent_clauses(sentences):
    """Returns a flat list containing all independent clauses."""
    clauses = []
    trees = identify_constructs(sentences)
    for tree in trees:
        clauses.extend(tree.subtrees(lambda t: t.label() == "INDEP"))

    return clauses
