"""
Definitions of Astro dataframes. These are essentially wrappers around the
pandas DataFrame class.
"""

import pandas as pd
from typing import Self
from contextlib import contextmanager

class AstroDataFrame:
    dataframe: pd.DataFrame

    def __init__(self, columns=[], dataframe=None) -> None:
        if dataframe is not None:
            self.dataframe = dataframe
        else:
            self.dataframe = pd.DataFrame(columns=columns)

    def __getitem__(self, key):
        return self.dataframe[key]

    def __str__(self):
        return self.dataframe.to_string(max_rows=20)

    def row_count(self) -> int:
        return len(self.dataframe.index)

    def get_columns(self) -> list:
        return self.dataframe.columns.tolist()

    def get_column_values(self, column=None) -> list:
        if column:
            return self.dataframe[column].tolist()

    def drop(self, index) -> None:
        self.dataframe.drop(index, inplace=True)

    def not_in(self, other) -> Self:
        """
        Return a dataframe consisting of rows which exist in `self`, but not in
        `other`.
        """
        merged = self.dataframe.merge(other.dataframe, how='outer', indicator=True)
        self_only = merged.query("_merge == 'left_only'").copy()
        if not self_only.empty:
            self_only.drop('_merge', axis=1, inplace=True)
            return AstroDataFrame(columns=self.dataframe.columns, dataframe=self_only)

        return None

    def apply(self, func, columns=[]) -> None:
        if columns:
            self.dataframe[columns] = self.dataframe.apply(func, axis=1)

    def empty(self) -> bool:
        return self.dataframe.empty

    def iterrows(self):
        for index, row in self.dataframe.iterrows():
            yield index, row

    def to_sql(self, db_table, db_conn, if_exists='fail') -> None:
        self.dataframe.to_sql(db_table, db_conn, index=False, if_exists=if_exists)


class CommentDataFrame(AstroDataFrame):
    columns = ['comment_id',
               'comment',
               'user',
               'date',
               'visible',
               'PSentiment',
               'NSentiment']

    def __init__(self, dataframe=None) -> None:
        super().__init__(columns=self.columns, dataframe=dataframe)

    def index(self) -> pd.Index:
        return self.dataframe.index

    def add_comment(self, comment_id, comment, user, date, visible=True,
                    psentiment=0, nsentiment=0) -> None:

        comment_data = [comment_id,
                        comment,
                        user,
                        date,
                        visible,
                        psentiment,
                        nsentiment]

        self.dataframe.loc[len(self.dataframe.index)] = comment_data

def read_comments_sql(sql, db_conn) -> CommentDataFrame:
    df = pd.read_sql(sql, db_conn)
    return CommentDataFrame(dataframe=df)
