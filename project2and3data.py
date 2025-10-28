import pandas as pd
import os


def prepare_inter_service_calls(df=None):
    # If no DataFrame is provided, load the default CSV
    if df is None:
        df = pd.read_csv(
            os.path.join(
                os.path.dirname(__file__), "project2&3traces", "train-ticket-traces.csv"
            )
        )

    # Rename columns for clarity
    df.rename(
        columns={
            "SpanID": "span_id",
            "ParentID": "parent_id",
            "PodName": "service",
            "OperationName": "operation",
            "StartTimeUnixNano": "start_time",
            "EndTimeUnixNano": "end_time",
        },
        inplace=True,
    )

    # Create lookup of spans by SpanID
    span_lookup = df.set_index("span_id")

    # Identify the caller service by the parent_id of a callee service
    df["caller_service"] = df["parent_id"].map(span_lookup["service"])

    # Filter: only inter-service calls (callee != caller)
    inter_service_calls = df[df["service"] != df["caller_service"]].copy()

    # Filter: remove rows with missing caller_service
    inter_service_calls = inter_service_calls[
        inter_service_calls["caller_service"].notna()
    ]

    # Rename to callee service
    inter_service_calls.rename(columns={"service": "callee_service"}, inplace=True)

    # Sort by time
    inter_service_calls = inter_service_calls.sort_values(by="start_time")

    return inter_service_calls


if __name__ == "__main__":
    df = prepare_inter_service_calls()
    df.to_csv(
        os.path.join(
            os.path.dirname(__file__), "project2&3traces", "project2edgeflow.csv"
        ),
        index=False,
        header=True,
    )
