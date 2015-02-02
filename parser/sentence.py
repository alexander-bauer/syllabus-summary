import nltk
from parser import datatype

class Sentence:
    def __init__(self, keywordlist):
        self.kwlist = keywordlist
        self.keyword = None
        self.data = None

        # Iterator or generator for possible keyword matches.
        self.subject_iter = None

    def include_word(self, word):
        # If the keyword has not yet been found, look for it.
        if self.keyword == None:
            return self.new_subject(word)
        else:
            return self.new_object(word)

        return False

    def new_subject(self, subject):
        """Try to set the sentence subject to the given subject word. If
        a match is discovered in the given keywordlist, return True.
        Otherwise, False."""
        if self.keyword != None:
            return False

        matches = self.kwlist.all_matches(subject)
        if matches:
            self.subject_iter = (pair[1] for pair in matches)

            self.next_subject();

            return 'Subject'
        else:
            return False

    def next_subject(self):
        self.keyword = next(self.subject_iter)
        self.data = self.keyword.datatype()

    def new_object(self, obj):
        """Try to add the given value as an object. This should not be
        called until the subject is set; if it is, it will return False.
        If the object can be added, return True. Otherwise, return
        False."""

        if self.keyword == None:
            return False
        
        try:
            self.data.enter_data(obj)
            return 'Object'
        except datatype.DataType.ConstructorException as e:
            return False
