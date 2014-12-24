import nltk

def split_phrases(paragraphs):
    """Extract individual sentences or phrases from a paragraph *or* a
    list of paragraphs. The resulting phrases will be returned in a
    flat list."""

    phrases = []

    # If the input type is not a list of paragraphs, then turn it into
    # one.
    if type(paragraphs) != list:
        paragraphs = [paragraphs]

    # Parse each paragraph in the list of paragraphs.
    for paragraph in paragraphs:
        # Break each paragraph down into sentences.
        # XXX: Ideally, we would want to identify individual phrases,
        # not just sentences.
        phrases.extend(nltk.sent_tokenize(paragraph))

    return phrases

def split_words(sentences):
    """Identify individual words in a list of sentences, and return a
    list containing lists of the tagged words."""

    list_of_words = []

    # If only one sentence is provided, turn it into a list.
    if type(sentences) != list:
        sentences = [sentences]

    # Parse each sentence.
    for sentence in sentences:
        list_of_words.append(nltk.word_tokenize(sentence))

    return list_of_words

def part_of_speech_tag(word_lists):
    """Use the NLTK part-of-speech (POS) tagger on each list of words,
    and return a flat list of the parsed trees."""
    
    tagged = []

    # If word_lists is not actually a list of word lists, but instead a
    # single word list, wrap it in another list.
    if len(word_lists) > 0 and type(word_lists[0]) != list:
        word_lists = [word_lists]

    for word_list in word_lists:
        tagged.append(nltk.pos_tag(word_list))

    return tagged
