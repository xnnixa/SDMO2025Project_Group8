import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import pandas as pd
from SDMO2025Project.project2and3data import prepare_inter_service_calls


def test_prepare_inter_service_calls_creates_caller_callee():
    df = pd.DataFrame(
        [
            {
                "SpanID": "1",
                "ParentID": "",
                "PodName": "frontend",
                "OperationName": "get",
                "StartTimeUnixNano": 1,
                "EndTimeUnixNano": 2,
            },
            {
                "SpanID": "2",
                "ParentID": "1",
                "PodName": "backend",
                "OperationName": "query",
                "StartTimeUnixNano": 3,
                "EndTimeUnixNano": 4,
            },
        ]
    )
    result = prepare_inter_service_calls(df)
    assert "caller_service" in result.columns
    assert "callee_service" in result.columns
    assert not result.empty
    assert result.iloc[0]["caller_service"] == "frontend"
    assert result.iloc[0]["callee_service"] == "backend"


def test_prepare_inter_service_calls_filters_self_calls():
    df = pd.DataFrame(
        [
            {
                "SpanID": "1",
                "ParentID": "",
                "PodName": "A",
                "OperationName": "op",
                "StartTimeUnixNano": 1,
                "EndTimeUnixNano": 2,
            },
            {
                "SpanID": "2",
                "ParentID": "1",
                "PodName": "A",
                "OperationName": "op",
                "StartTimeUnixNano": 3,
                "EndTimeUnixNano": 4,
            },
        ]
    )
    result = prepare_inter_service_calls(df)
    assert result.empty


def test_prepare_inter_service_calls_missing_parents():
    df = pd.DataFrame(
        [
            {
                "SpanID": "10",
                "ParentID": "999",
                "PodName": "C",
                "OperationName": "ping",
                "StartTimeUnixNano": 1,
                "EndTimeUnixNano": 2,
            }
        ]
    )
    result = prepare_inter_service_calls(df)
    assert result.empty
