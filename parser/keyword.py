import types
from parser import compare
from parser import sentence
from parser import datatype

class Keyword:
    class DataModelIncomplete(Exception): pass

    def __init__(self, word, *alternatives, datamodel = None, normalized
            = False):
        if datamodel != None and not issubclass(type(datamodel),
                datatype.DataType):
            raise self.DataModelIncomplete("Data model not instance of \
DataType (did you remember to construct one?): %s" % datamodel)
        self.datatype = datamodel

        if normalized:
            self.primary = word
            self.words = [self.primary]
            self.words.extend(alternatives)
        else:
            self.primary = word
            self.words = [compare.normalize(self.primary)]
            self.words.extend([compare.normalize(alt) for alt in
                alternatives])

    def all_matches(self, wordcompare, sort = True, normalized = False):
        """Return the best matches to the word or function, if any are
        above the EDIT_DISTANCE_THRESHOLD. Otherwise, None."""

        # If wordcompare is a function, then it is already a curried
        # function with the word to compare to. Otherwise, wrap it as
        # such.
        if type(wordcompare) == types.FunctionType:
            comparefunc = wordcompare
        else:
            # Build a function used to compare the given word with the
            # keyword.
            comparefunc = compare.compare_to(wordcompare, normalized)

        # For convenience, we'll decorate the list of words with their
        # closeness to the word match, and only include words which did
        # match within a threshold.
        proximity_words = []
        for kw in self.words:
            matched, score = comparefunc(kw, normalized = True)
            if matched:
                proximity_words.append((score, kw))

        # If there are no matches, return None.
        if len(proximity_words) == 0:
            return None

        if sort:
            proximity_words.sort(key = lambda pair: pair[0])

        return proximity_words

    def match(self, wordcompare, normalized = False):
        """Return the best match to the word or function, if any are
        above the EDIT_DISTANCE_THRESHOLD. Otherwise, None."""

        # Pick the best tuple of (score, word) using the proximity
        # as the key, and return the word.
        proximity_words = self.all_matches(wordcompare, sort = False,
                normalized = normalized)
        if proximity_words == None:
            return None, None

        score, word = min(proximity_words, key = lambda pair: pair[0])
        return (score, word)

class KeywordList(list):
    def __init__(self, keyword_list):
        self.kwlist = keyword_list

    def all_matches(self, wordcompare, sort = True, normalized = False):
        """Find the best match among all the listed keywords, if
        present. Return the matching Keyword object and its score."""

        # If wordcompare is a function, then it is already curried.
        # Otherwise, curry it.
        if type(wordcompare) == types.FunctionType:
            comparefunc = wordcompare
        else:
            comparefunc = compare.compare_to(wordcompare, normalized)

        proximity_keywords = []
        for kw in self.kwlist:
            score, word = kw.match(comparefunc)
            if word != None:
                proximity_keywords.append((score, kw))

        if len(proximity_keywords) == 0:
            return None

        if sort:
            proximity_keywords.sort(key = lambda pair: pair[0])

        return proximity_keywords

    def match(self, wordcompare, normalized = False):
        proximity_keywords = self.all_matches(wordcompare, sort = False,
                normalized = normalized)
        if proximity_keywords == None:
            return None, None

        return min(proximity_keywords, key = lambda pair: pair[0])
