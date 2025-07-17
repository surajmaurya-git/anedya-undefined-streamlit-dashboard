import os
import json
import requests
import csv
import io
import streamlit as st

INFLUX_DB_TOKEN = st.secrets["INFLUX_DB_TOKEN"]


def get_alerts():
    # Endpoint and auth
    url = "https://us-east-1-1.aws.cloud2.influxdata.com/api/v2/query"
    headers = {
        "Authorization": f"Token {INFLUX_DB_TOKEN}",
        "Content-Type": "application/vnd.flux",
        "Accept": "text/csv",
    }
    params = {"org": "anedya"}
    # Your Flux query
    query = """
        from(bucket: "undefined_doorStatus")
        |> range(start: -30d)
        |> filter(fn: (r) => r._measurement == "ColdRoom1" and r._field == "doorState")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 100)
    """

    # Send query
    response = requests.post(url, params=params, headers=headers, data=query)

    # Parse response into a list
    if response.status_code == 200:
        csv_data = response.text
        csv_reader = csv.DictReader(io.StringIO(csv_data))
        parsed_data = []
        for row in csv_reader:
            if "_time" in row and "_value" in row:
                parsed_data.append({"time": row["_time"], "value": row["_value"]})
        # print(csv_data)
        return parsed_data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
        return []
