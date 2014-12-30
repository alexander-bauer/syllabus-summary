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
    return compare_metric(string1, string2, normalized1, normalized2) \
            <= EDIT_DISTANCE_THRESHOLD
