import nltk

# Define a grammar, and identify the Noun Pairs and Noun PhRases in the
# sentences.
# TODO: Look into using exclusive grammars to discard prepositional
# phrases, and such.
_chunk_parser_ = nltk.RegexpParser("""
EMAIL: {<NN><:><JJ>}
VP: {<VBZ><NN>?}
NP: {<PRP|NN|NNP|CD|EMAIL>+}
NPR: {((<DT|PRP\$>)?<JJ>*(<NP|CC>)+)}
""")

def identify_constructs(sentences):
    # If we are only given a single sentence, wrap it in a list.
    if len(sentences) > 0 and type(sentences[0]) != list:
        sentences = [sentences]

    return [_chunk_parser_.parse(sentence) for sentence in sentences]
