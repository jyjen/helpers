import pandas as pd
import re
import spacy
import str_helpers as strh
import nltk
# nltk.download('punkt')

#? class Process
def split_sents_df(df: pd.core.frame.DataFrame,
                   sent_col: str,
                   segmenter: str):

    """Splits sentences in a DataFrame and stacks the sentences into a new DataFrame.

    Arguments:
        df: pd.core.frame.DataFrame - DataFrame containing text to segment
        sent_col: str - Name of column containing paragraphs to segment
        segmenter: str - Sentence segmenter to use. Either 'nltk_punkt', 'regex' or 'spacy'
    """

    temp_df = df.copy(deep = True)
    split = temp_df[sent_col].apply(lambda text: strh.split_sents(text, segmenter))

    return pd.DataFrame({'sent':[item for sublist in split.tolist()
                                 for item in sublist]})

# ? class Sniffer
def check_in_row(df: pd.core.frame.DataFrame,
                 pattern: str,
                 re_flags=0,
                 use_regex=True):

    """Returns the rows of a dataframe which contain either a specific substring or regex pattern.

    Arguments:
        df: pd.core.frame.DataFrame - DataFrame to search for substrings or regex patterns in
        pattern: str - The specific substring or regex pattern to search for
        re_flags: RegexFlag - re module flags to use
        use_regex: boolean - If True use regex search; else search for substring
    """

    re_series = [df[colname].str.contains(pattern,
                                          flags=re_flags,
                                          regex=use_regex) for colname in df.columns]
    re_df = pd.concat(re_series, axis=1)
    any_re = re_df.apply(lambda row: any(row), axis=1)

    return df[any_re]


class ReplaceTokens:

    """
    For replacing tokens in a DataFrame.
    Substitutes tokens in a dataframe column using key-value pairs in the specified dictionary.

    Arguments:
        df: pd.core.frame.DataFrame - DataFrame containing sentences with tokens to be replaced.

        re_dict: dict - A dictionary containing with keys-value pairs which
                            correspond to the word/phrase to be replaced and it's replacement.
                            i.e. {'phrase2replace':'replacement phrase'}  
    """

    def __init__(self,
                 df: pd.core.frame.DataFrame,
                 re_dict: dict):

        self.temp_df = df.copy(deep=True)
        self.replacer = self.make_xlat(re_dict)

    @staticmethod
    def make_xlat(re_dict):

        """
        Sets up a function which performs multi-string substitution in a single pass.
        For reference: https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html

        Arguments:
            re_dict: dict - A dictionary containing with keys-value pairs which
                            correspond to the word/phrase to be replaced and it's replacement.
                            i.e. {'phrase2replace':'replacement phrase'}
        """

        rx = re.compile('|'.join(map(re.escape, re_dict)))

        def one_xlat(match):
            return re_dict[match.group(0)]

        def xlat(text):
            return rx.sub(one_xlat, text)

        return xlat

    def replace_in_col(self,
                       str_col: str):

        """
        Replaces tokens specified in self.re_dict in a specified column in self.df.

        Arguments:
            str_col: str - The name of the DataFrame column with tokens to be replaced.
        """

        self.temp_df[str_col] = self.temp_df[str_col].apply(lambda sent: self.replacer(sent))

        return self.temp_df

    def replace_all(self):

        """
        Replaces tokens specified in self.re_dict in all columns containing strings in self.df.
        """

        text_cols = [colname for colname in self.temp_df.columns
                     if all(self.temp_df[colname].apply(lambda item: isinstance(item, str)))]

        for col in text_cols:

            self.temp_df[col] = self.temp_df[col].apply(lambda sent: self.replacer(sent))

        return self.temp_df

