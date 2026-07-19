# -*- coding: utf-8 -*-
"""
   Create tabulate markdown from a pandas dataframe
"""

from typing import TYPE_CHECKING
from tabulate import tabulate

if TYPE_CHECKING:
    from pandas import DataFrame


def tabulate_dataframe(df: 'DataFrame', colalign: tuple = None, showindex: bool = False) -> str:
    return tabulate(df, headers='keys', tablefmt='psql', colalign=colalign, showindex=showindex)

if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    print(tabulate_dataframe(df))