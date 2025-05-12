def test_aggregate_counts(spark):
    data = [
        {"state_province": "California"},
        {"state_province": "California"},
        {"state_province": "Texas"},
    ]
    df = spark.createDataFrame(data)

    result = df.groupBy("state_province").count().collect()
    counts = {row["state_province"]: row["count"] for row in result}
    
    assert counts["California"] == 2
    assert counts["Texas"] == 1