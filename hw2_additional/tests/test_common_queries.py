import pandas as pd
import pytest

from ..src.olympics_utils.common_queries import (get_athlete_medals,
                                                 get_medal_count)


@pytest.fixture(scope='module')
def test_df():
    test_df = pd.DataFrame([
        [1896, "FLACK, Edwin", "AUS", "Gold"],
        [1896, "SCHUMANN, Carl", "GER", "Gold"],
        [1896, "TSITAS, Georgios", "GRE", "Silver"],
        [1900, "HALMAY, Zoltan", "HUN", "Bronze"],
        [1900, "LANE, Frederick C.V.", "AUS", "Gold"],
        [1904, "HALMAY, Zoltan", "HUN", "Gold"],
        [1904, "HALMAY, Zoltan", "HUN", "Gold"],
        [1908, "HALMAY, Zoltan", "HUN", "Silver"],
        [1908, "HALMAY, Zoltan", "HUN", "Silver"]
    ], columns=["Edition", "Athlete", "NOC", "Medal"])
    return test_df


# get_athlete_medals tests
def test_get_athlete_medals_halmay(test_df):
    expected = test_df.iloc[[3, 5, 6, 7, 8]]
    actual = get_athlete_medals(test_df, 'HALMAY, Zoltan')

    pd.testing.assert_frame_equal(expected, actual)


def test_get_athlete_medals_halmay_gold(test_df):
    expected = test_df.iloc[[5, 6]]
    actual = get_athlete_medals(test_df, 'HALMAY, Zoltan', ['Gold'])

    pd.testing.assert_frame_equal(expected, actual)


def test_get_athlete_medals_halmay_gold_silver(test_df):
    expected = test_df.iloc[[5, 6, 7, 8]]
    actual = get_athlete_medals(test_df, 'HALMAY, Zoltan', ['Gold', 'Silver'])

    pd.testing.assert_frame_equal(expected, actual)


def test_get_athlete_medals_halmay_1904(test_df):
    expected = test_df.iloc[[5, 6]]
    actual = get_athlete_medals(test_df, 'HALMAY, Zoltan', editions=[1904])

    pd.testing.assert_frame_equal(expected, actual)


def test_get_athlete_medals_halmay_1904_silver(test_df):
    expected = test_df.iloc[[]]
    actual = get_athlete_medals(test_df, 'HALMAY, Zoltan', ['Silver'], [1904])

    pd.testing.assert_frame_equal(expected, actual)


def test_get_athlete_medals_unsupported_args(test_df):
    with pytest.raises(TypeError):
        get_athlete_medals(test_df, 'HALMAY, Zoltan', 'Silver')


# get_medal_count tests
def test_get_medal_count_1904(test_df):
    expected = pd.DataFrame(
        [[2, 2, 0, 0]],
        columns=['Total_medals', 'Gold_medals',
                 'Silver_medals', 'Bronze_medals'],
        index=['HUN'], dtype=int)
    expected.index.name = 'NOC'
    actual = get_medal_count(test_df, 1904)

    pd.testing.assert_frame_equal(expected, actual)


def test_get_medal_count_1896(test_df):
    expected = pd.DataFrame(
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 1, 0]
        ],
        columns=['Total_medals', 'Gold_medals',
                 'Silver_medals', 'Bronze_medals'],
        index=['AUS', 'GER', 'GRE'], dtype=int)
    expected.index.name = 'NOC'
    actual = get_medal_count(test_df, 1896)

    pd.testing.assert_frame_equal(expected.sort_index(), actual.sort_index())
