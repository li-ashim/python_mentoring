'''
This module contains some useful patterns for working with
1896 - 2008 Olimpics dataset.
'''
from typing import Literal, Sequence, Union

import pandas as pd

Medal = Literal['Gold', 'Silver', 'Bronze']


def get_athlete_medals(df: pd.DataFrame, athlete: str,
                       medals: Union[Sequence[Medal], None] = None,
                       editions: Union[Sequence[int], None] = None
                       ) -> pd.DataFrame:
    '''Returns athlete's certain medals if specified, otherwise all medals'''
    if not medals:
        if not editions:
            return df[(df['Athlete'] == athlete)]
        else:
            return df[(df['Athlete'] == athlete)
                      & (df['Edition'].isin(editions))]
    else:
        if not editions:
            return df[(df['Athlete'] == athlete)
                      & (df['Medal'].isin(medals))]
        return df[(df['Athlete'] == athlete)
                  & (df['Medal'].isin(medals))
                  & (df['Edition'].isin(editions))]


def get_medal_count(df: pd.DataFrame, edition: int) -> pd.DataFrame:
    '''Returns medal count of certain Olimpics sorted in descending order.'''
    d = df[df['Edition'] == edition].groupby('NOC')['Medal'].count()
    d = d.to_frame(name=f'{edition} Olimpics')
    d.columns = ['Total_medals']
    for medal in ['Gold', 'Silver', 'Bronze']:
        d[f'{medal}_medals'] = df[(df['Edition'] == edition)
                                  & (df['Medal'] == medal)
                                  ].groupby('NOC')['Medal'].count()

    d = d.fillna(0)  # NaN marks absence of medals of given type
    d = d.astype(int)
    return d.sort_values('Total_medals', ascending=0)
