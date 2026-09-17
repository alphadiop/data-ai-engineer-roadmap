def test(**context):
    print(context)

test(
    params={
        "periode": 202501,
        "taxi_type": "yellow",
        "env": "docker"
    }
)