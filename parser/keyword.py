import types
from parser import compare

class Keyword:
    def __init__(self, word, *alternatives, normalized = False):
        if not normalized:
            self.keyword = word
            self.words = [self.keyword]
            self.words.extend(alternatives)
        else:
            self.keyword = normalize(word)
            self.words = [self.keyword]
            self.words.extend([normalize(alt) for alt in
                alternaties])

    def match(self, wordcompare, normalized = False):
        """Return the best match to the word or function, if any are
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

        # Pick the best tuple of (score, word) using the proximity
        # as the key, and return the word.
        score, word = min(proximity_words, key = lambda pair: pair[0])
        return word
