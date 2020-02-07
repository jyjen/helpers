# from functools import filter, partial, reduce
# import pandas as pd
# import re
import spacy

class DocFilter:

    """Class for selecting specific words and phrases from a
    SpaCy document.

    Arguments:
        text {str} -- Text to analyse"""

    def __init__(self,
                 text: str):

        if 'nlp' not in globals():

            global nlp
            nlp = spacy.load('en_core_web_lg')

        self.doc = nlp(text)
        self.conditional = None

    def build_conditional(self,
                          **kwargs):

        """Builds the conditional for filtering words and phrases with SpaCy.

        Keyword arguments:
            Each kwarg is a whitelist (set) of tags to filter words/phrases with.
                pos_whitelist {set} -- Simple part-of-speech tag
                tag_whitelist {set} -- Detailed part-of-speech tag
                dep_whitelist {set} -- Dependency tag
        """

        valid_kwargs = {'pos_whitelist', 'tag_whitelist', 'dep_whitelist'}
        invalid_kwargs = set(kwargs.keys()).difference(valid_kwargs)

        if invalid_kwargs:
            raise ValueError ('Invalid kwargs - {} - were passed.'.format(invalid_kwargs))

        # TODO: is there a way of constructing the conditional without eval?
        # ? partials + reduce (fail)
        # ? eval (questionable)
        # ? filter
        # ? using pandas
        eval_phrases =  {'pos_whitelist': 'word.pos_ in ',
                         'tag_whitelist': 'word.tag_ in ',
                         'dep_whitelist': 'word.dep_ in '}

        kwarg_phrases = [str("{} {}".format(eval_phrases[k],
                                            str(repr(v))))
                         for k,v in kwargs.items()]

        self.conditional = reduce(lambda x,y: "{} and {}".format(x,y),
                                  kwarg_phrases)

    def get_words(self):

        """Finds words based on the kwarg whitelists passed.

        Returns:
            filtered_words {list} -- List of words which match the
                tag whitelists (kwargs)
        """

        filtered_words = [word for word in self.doc
                          if eval(self.conditional)]

        return filtered_words

    def find_phrases(self):

        """Finds phrases based on the kwarg whitelists passed.

        Returns:
            phrase_list {list} -- List of phrases which match
                the tag whitelists (kwargs)
        """

        filtered_words = [word for word in self.doc
                          if eval(self.conditional)]
        subtree_spans = [self.doc[word.left_edge.i : word.right_edge.i + 1]
                         for word in filtered_words]
        phrase_list = [span.text for span in subtree_spans]

        return phrase_list
