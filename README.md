# In Summary

Sometimes, it is simpler to author text describing a piece of data than
to explicitly fill out a form, particularly if the data is coming from
another pre-written source, such as a syllabus. Here, I am trying to use
natural language processing to extract
[EduPal](http://edupal.co)-relevant information from short summaries of
syllabus information.

# Problems

Extracting information from English is hard. It's full of ambiguities,
bizarre conventions, inconsistencies, and idioms. In fact, success in
the field of natural language processing is relatively new.

There are a number of intricacies to natural language processing, and
familiarizing one's self with them is a nontrivial feat. Reaching
EduPal's goals will take time and effort.

### Identifying sentences, compound and otherwise

The Python NLTK has a sentence tokenizer, which can be used to split
paragraphs of data down into individual sentences. However, we are not
necessarily looking for sentences; instead, we are looking for
independent clauses.

For example, consider the single sentence "The instructor's name is John
Smith, and his email is jsmith@umbc.edu." It contains two distinct
pieces of information, a name and an email address, and should be
processed just like the sentences "The instructor's name is John Smith.
His email is jsmith@umbc.edu."

### Identifying the subject and object in sentences

After tokenizing a clause, extracting what the sentence is *about* is
the next issue. To do that in English-like grammars, we would identify
the subject and object, which correlate fairly strongly to the field we
are trying to fill out, and the data with which we will do so,
respectively.

To do this, we might use part-of-speech (POS) tagging to find
combinations of words which resemble subjects and objects, called "noun
pairs."

After doing so, we could naively select the subject and object by order,
but this will fail in instances such as "Tuesday and Thursdays are the
meeting days." A more robust approach is to compare a potential subject
to a pre-determined list of key phrases we are searching for, such as
"course id," "instructor name," and the like. (How to compare key
phrases to potential subjects is another issue.)

With potential objects already tagged as noun pairs, we might have
reasonable success assuming that every noun pair in a sentence aside
from the subject is an object, or piece of data that should be
associated with it. If better results are desired, then rudimentary
sanity checks could be implemented on a per-keyword basis. For example,
a "start time" key phrase might ensure that there is just one object,
and it can be parsed as a time of day.

#### Comparing Strings to Identify Subjects

A simple solution to fuzzy-matching for subject identification is to
inspect edit distance, which is the number of elementary modifications
required for one string to be equal to another. Key phrases could be
sorted for their nearness (in edit distance) to a potential subject, and
the best one could be selected, assuming it is close within a
pre-determined threshold.

## Sources of Information

http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
