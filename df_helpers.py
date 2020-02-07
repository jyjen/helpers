import pandas as pd

class EzConditionals:
# ? TBD - would this be a useful util?
    """For composing conditional statements for filtering Pandas DataFrames.

    Arguments:
        df {pd.core.frame.DataFrame} -- DataFrame

    Keyword arguments:
    """

    def __init__(self,
                 df: pd.core.frame.DataFrame,
                 **kwargs):

        self.df = df
        self.kwargs = kwargs

    def write_conditional(self):
        pass

class Filters:

    @staticmethod
    def num_filter(df:pd.core.frame.DataFrame,
                   num_set: set,
                   num_colname: str = None):

        if num_colname:
            _bool = df[num_colname].apply(lambda num: num in num_set)

        # if not num_colname, filters out any row which contains a permitted num
        # need to check which columns contain numbers
        num_df = # filter out the columns which contain numbers
        _bool_df = num_df.apply(lambda num: num in num_set,
                            axis = 1)
        _bool = reduce(and_, _bool_df)

        return df[_bool].reset_index(drop=True)

    @staticmethod
    def datetime_filter(df: pd.core.frame.DataFrame,
                        min_dt: str = None,
                        min_dt_colname: str = None,
                        max_dt: str = None,
                        max_dt_colname: str = None):

        """Filter rows in a DataFrame by date.

        Arguments:
            df {pd.core.frame.DataFrame} -- DataFrame to filter by date
            min_dt {str} -- Date lower limit; formatted as "%d/%m/%Y %z"
                e.g. "DD/MM/YYY +HHMM"
            min_dt_colname {str} -- Name of column containing date lower limit
            max_dt {str} - Date upper limit; formatted as "%d/%m/%Y %z"
                e.g. "DD/MM/YYY +HHMM"
            max_dt_colname {str} -- Name of column containing date lower limit
        """

        dt_to_usec = lambda _dt: datetime.strptime(
            _dt, "%d/%m/%Y %z").timestamp()*1000000

        _bools = []

        if min_dt:
            min_time_usec = dt_to_usec(min_dt)
            min_bool = pd.Series(df[min_dt_colname] > min_time_usec)
            _bools += [min_bool]

        if max_dt:
            max_time_usec = dt_to_usec(max_dt)
            max_bool = pd.Series(df[max_dt_colname] > max_time_usec)
            _bools += [max_bool]

        filtered = df[reduce(and_, _bools)]

        return filtered

if __name__ == "__main__":

    from sklearn.datasets import load_iris

    iris_data = load_iris()
    target_names = np.apply_along_axis(lambda target: iris_data.target_names[target],
                                       axis = 0,
                                       arr = iris_data.target)
    iris_df = pd.DataFrame(data=np.c_[iris_data['data'], target_names],
                           columns=iris_data['feature_names'] + ['target'])