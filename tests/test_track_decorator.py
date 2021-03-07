import pandas as pd
import pytest

from pipediff import DiffTracker


def test_basic_tracking_decorator(tracker: DiffTracker, df_num: pd.DataFrame) -> None:
    def _func(df: pd.DataFrame) -> pd.DataFrame:
        return df

    _func_decorated = tracker.track()(_func)
    res_1 = df_num.pipe(_func)
    res_2 = df_num.pipe(_func_decorated)

    pd.testing.assert_frame_equal(res_1, res_2)

    assert len(tracker.frame_logs) == 2


def test_decorator_exceptions(tracker: DiffTracker, df_num: pd.DataFrame) -> None:
    @tracker.track()
    def _func_1(df: pd.DataFrame) -> pd.DataFrame:
        return df, 5

    df_num.pipe(_func_1)

    @tracker.track()
    def _func_2(df: pd.DataFrame) -> pd.DataFrame:
        return 5, df

    with pytest.raises(TypeError):
        df_num.pipe(_func_2)

    @tracker.track()
    def _func_3(arg_1: int, df: pd.DataFrame) -> pd.DataFrame:
        return df, 5

    with pytest.raises(TypeError):
        _func_3(5, df_num)
    with pytest.raises(TypeError):
        _func_3(arg_1=5, df=df_num)