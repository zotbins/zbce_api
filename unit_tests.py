"""
1. Change the BASEURL variable to match your BASEURL
2. Make sure your Flask server is running
3. Run the following test using pytest:
        pytest -q unit_tests.py

(WARNING: this will delete the existing data in the database by dropping all the tables)
"""
# library imports
import datetime, time
import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# local imports
import create_tables

# load environment variables
dirname = os.path.dirname(__file__)
dotenv_path = Path(os.path.join(dirname, ".env"))
load_dotenv(dotenv_path=dotenv_path)

# global variables
BASEURL = os.getenv("BASE_URL")  # replace with your own base URL
IPADDRESS = "127.0.0.1"  # replace with your own IP Address you are testing with
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def test_drop_and_create_tables():
    # WARNING: this will delete the existing data in the database by dropping all the tables
    create_tables.recreate_tables()


def test_main_page():
    r = requests.get(url=BASEURL)
    assert r.status_code == 200


def test_post_bin_info():
    postRequest = {
        "data": [
            {
                "ip_address": IPADDRESS,
                "bin_height": 50,
                "location": "your_place",
                "bin_type": "R",
                "waste_metrics": "FP",
            }
        ]
    }
    r = requests.post(
        BASEURL + "/bin-info", data=json.dumps(postRequest), headers=HEADERS
    )
    print(r.content)
    assert r.status_code == 201


def test_get_bin_info_all():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/bin-info/all`
    """
    r = requests.get(url=BASEURL + "/bin-info-all")
    print(r.json())
    assert r.status_code == 200


def test_post_bin_usage():
    postRequest = {"data": [{"bin_id": 1, "datetime": "2020-11-04 15:06:25"}]}
    r = requests.post(BASEURL + "/usage", data=json.dumps(postRequest), headers=HEADERS)
    assert r.status_code == 201


def test_get_bin_usage():
    params = {
        "start_timestamp": "2019-11-04 15:06:25",
        "end_timestamp": "2021-01-29 15:06:25",
        "bin_id": 1,
    }
    r = requests.get(url=BASEURL + "/usage", params=params, headers=HEADERS)
    print(r.json())
    assert r.status_code == 200


def test_get_usage_all():
    r = requests.get(url=BASEURL + "/usage-today")
    print(r.json())
    assert r.status_code == 200


def test_post_fullness():
    postRequest = {
        "data": [{"datetime": "2015-11-04 15:06:25", "fullness": 50, "bin_id": 1}]
    }
    r = requests.post(
        BASEURL + "/fullness", data=json.dumps(postRequest), headers=HEADERS
    )
    print(r.content)
    assert r.status_code == 201


def test_get_fullness_all():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/bin-fullness/all`
    """
    r = requests.get(url=BASEURL + "/fullness-today")
    print(r.json())
    assert r.status_code == 200


def test_get_fullness_w_id():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/bin-fullness?start_timestamp="2019-11-04 15:06:25"&end_timestamp="2016-11-04 15:06:25"&bin_id=1`
    """
    params = {
        "start_timestamp": "2014-11-04 15:06:25",
        "end_timestamp": "2021-01-29 15:06:25",
        "bin_id": 1,
    }
    r = requests.get(BASEURL + "/fullness", params=params, headers=HEADERS)
    print(r.json())
    assert r.status_code == 200


def test_post_weight():
    postRequest = {
        "data": [{"datetime": "2015-11-04 15:06:25", "weight": 25, "bin_id": 1}]
    }
    r = requests.post(
        BASEURL + "/weight", data=json.dumps(postRequest), headers=HEADERS
    )
    print(r.content)
    assert r.status_code == 201


def test_get_weight_all():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/weight/all`
    """
    r = requests.get(url=BASEURL + "/weight-today")
    print(r.json())
    assert r.status_code == 200


def test_get_weight_w_id():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/weight?start_timestamp="bin_id=1&2014-11-04 15:06:25"&end_timestamp="2016-11-04 15:06:25"`
    """
    params = {
        "bin_id": 1,
        "start_timestamp": "2014-11-04 15:06:25",
        "end_timestamp": "2021-01-29 15:06:25",
    }
    r = requests.get(BASEURL + "/weight", params=params, headers=HEADERS)
    print(r.json())
    assert r.status_code == 200


def test_post_image():
    with open("404.jpg", "rb") as f:
        r = requests.post(BASEURL + "/image", files={"file": f})
        print(r.content)
        assert r.status_code == 200


if __name__ == "__main__":
    test_drop_and_create_tables()
    test_post_bin_info()
    test_get_bin_info_all()
    test_post_bin_usage()
    test_get_bin_usage()
    test_get_usage_all()
    test_post_fullness()
    test_get_fullness_all()
    test_get_fullness_w_id()
    test_post_weight()
    test_get_weight_all()
    test_get_weight_w_id()
    test_post_image()
