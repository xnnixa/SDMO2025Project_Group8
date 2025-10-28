import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import pandas as pd
from unittest.mock import MagicMock


def test_interval_grouping_correctness():
    df = pd.DataFrame(
        {
            "caller_service": ["A", "B"],
            "callee_service": ["B", "C"],
            "start_time": [1000, 2000],
        }
    )
    interval_duration_ns = 1000
    min_time_ns = df["start_time"].min()
    df["interval"] = ((df["start_time"] - min_time_ns) // interval_duration_ns).astype(
        int
    )
    assert list(df["interval"]) == [0, 1]


def test_masuda_holme_mock(monkeypatch):
    from SDMO2025Project.project3anomaly import MasudaHolme

    mock_func = MagicMock(return_value=(2, [[0, 1, 2]], [0.7, 0.8], None, None))
    monkeypatch.setattr("SDMO2025Project.project3anomaly.MasudaHolme", mock_func)
    mock_network = MagicMock()
    best_C, labels, dunn_scores, *_ = MasudaHolme(mock_network)
    assert best_C == 2
    assert isinstance(dunn_scores, list)
    assert len(dunn_scores) == 2
