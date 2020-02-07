import pandas as pd
import re
import spacy
import nltk
# nltk.download('punkt')

def make_xlat(re_dict):

    """
    Sets up a function which performs multi-string substitution in a single pass.
    For reference: https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html

    Arguments:
        re_dict {dict} -- A dictionary containing with keys-value pairs which
            correspond to the word/phrase to be replaced and it's replacement.
            i.e. {'phrase2replace':'replacement phrase'}

    Returns:
        xlat {func} -- Function which performs multi-string substitution
    """

    rx = re.compile('|'.join(map(re.escape, re_dict)))

    def one_xlat(match):
        return re_dict[match.group(0)]

    def xlat(text):
        return rx.sub(one_xlat, text)

    return xlat

def split_sents(chunk: str,
                segmenter: str = {'nltk_punkt', 'regex', 'spacy'}):

    """Splits a single input paragraph/chunk into sentences using a given segmenter.

    Arguments:
        chunk: str - Paragraph to segment
        segmenter: str - Sentence segmenter to use. Either 'nltk_punkt', 'regex' or 'spacy'
    """


    if segmenter == 'nltk_punkt':

        return nltk.tokenize.sent_tokenize(chunk)

    elif segmenter == 'regex':

        # simple regex segmenter - doesn't work super reliably

        re_pattern = r"([A-Za-z0-9_,\-'’&\(\) ]{3,}[.!\?]) ?"

        return [string for string in re.split(re_pattern, chunk, maxsplit=0, flags=0)
                if len(string) > 0]

    elif segmenter == 'spacy':

        if 'nlp' not in globals():

            global nlp
            nlp = spacy.load('en_core_web_lg')

        return [str(sent) for sent in nlp(chunk).sents]

    else:
        raise ValueError("{} is not a valid type of sentence segmenter.\
            Please input either 'nltk_punkt', 'regex' or 'spacy'".format(segmenter))
