import nltk

EDIT_DISTANCE_THRESHOLD = 3

_stemmer_ = nltk.stem.PorterStemmer()

# I borrowed some fuzzy matching code from StreamHacker.
# http://streamhacker.com/2011/10/31/fuzzy-string-matching-python/
def normalize(string):
    words = nltk.tokenize.wordpunct_tokenize(string.lower().strip())
    return ' '.join([_stemmer_.stem(w) for w in words])

def edit_distance(string1, string2, normalized1 = False, normalized2 =
        False):

    if not normalized1:
        string1 = normalize(string1)
    if not normalized2:
        string2 = normalize(string2)

    return nltk.edit_distance(string1, string2)

def compare_metric(string1, string2, normalized1 = False, normalized2 =
        False):
    return edit_distance(string1, string2, normalized1, normalized2)

def compare(string1, string2, normalized1 = False, normalized2 = False):
    """Returns tuple containing whether or not the match was successful,
    and its score (with zero being the closest match)."""
    score = compare_metric(string1, string2, normalized1, normalized2)
    if score <= EDIT_DISTANCE_THRESHOLD:
        return (True, score)
    else:
        return (False, None)

def compare_to(string1, normalized1 = False):
    """This function is used to curry the compare function. It returns a
    function which calls compare using the arguments passed to it."""
    if not normalized1:
        string1 = normalize(string1)

    def curried_compare(string2, normalized = False):
        return compare(string1, string2, normalized1 = True,
            normalized2 = normalized)

    return curried_compare
