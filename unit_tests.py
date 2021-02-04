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

# local imports
import create_tables

# global variables
BASEURL = "http://192.168.1.100:5001"
IPADDRESS = "192.168.1.100"
HEADERS = {"Content-Type": "application/json","Accept": "application/json"}

def test_drop_and_create_tables():
    # WARNING: this will delete the existing data in the database by dropping all the tables
    create_tables.recreate_tables()

def test_main_page():
    r = requests.get(url=BASEURL)
    assert(r.status_code == 200)

def test_post_bin_info():
    postRequest = {"data":[{"ip_address":IPADDRESS,"bin_height":50,"location":"your_place","bin_type":"R","waste_metrics":"FP"}]}
    r = requests.post(BASEURL + "/post/bin-info", data=json.dumps(postRequest),headers=HEADERS)
    print(r.content)
    assert(r.status_code == 201)

def test_get_bin_info_all():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/bin-info/all`
    """
    r = requests.get(url=BASEURL+"/bin-info/all")
    print(r.json())
    assert(r.status_code == 200)

def test_post_bin_usage():
    postRequest = {"data":[{"bin_id":1,"datetime":"2020-11-04 15:06:25"}]}
    r = requests.post(BASEURL + "/post/usage", data=json.dumps(postRequest),headers=HEADERS)
    assert(r.status_code == 201)

def test_get_usage_all():
   r = requests.get(url=BASEURL + "/usage/all")
   print(r.json)
   assert(r.status_code == 200)


def test_post_fullness():
    postRequest = {"data":[{"datetime":"2015-11-04 15:06:25","fullness":50,"bin_id":1}]}
    r = requests.post(BASEURL+"/post/fullness", data=json.dumps(postRequest),headers=HEADERS)
    print(r.content)
    assert(r.status_code == 201)

def test_get_fullness_all():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/bin-fullness/all`
    """
    r = requests.get(url=BASEURL + "/bin-fullness/all")
    print(r.json)
    assert(r.status_code == 200)

def test_get_fullness_w_id():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/bin-fullness?start_timestamp="2019-11-04 15:06:25"&end_timestamp="2016-11-04 15:06:25"&bin_id=1`
    """
    params = {"start_timestamp":"2019-11-04 15:06:25","end_timestamp":"2021-01-29 15:06:25","bin_id":1}
    r = requests.get(BASEURL+"/bin-fullness", params=params,headers=HEADERS)
    print(r.json)
    assert(r.status_code == 200)

def test_post_weight():
    postRequest = {"data":[{"datetime": "2015-11-04 15:06:25","weight": 25,"bin_id": 1}]}
    r = requests.post(BASEURL+"/post/weight",data=json.dumps(postRequest),headers=HEADERS)
    print(r.json)
    assert(r.status_code == 201)

def test_get_weight_all():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/weight/all`
    """
    r = requests.get(url=BASEURL+"/weight/all")
    print(r.json)
    assert(r.status_code == 200)

def test_get_weight_w_id():
    """
    **Equivalent Request**
    `http://BASEURL:YOURPORT/weight?start_timestamp="bin_id=1&2014-11-04 15:06:25"&end_timestamp="2016-11-04 15:06:25"`
    """
    params = {"bin_id":1,"start_timestamp":"2014-11-04 15:06:25","end_timestamp":"2021-01-29 15:06:25"}
    r = requests.get(BASEURL+"/weight",params=params,headers=HEADERS)
    print(r.json)
    assert(r.status_code==200)

def test_post_image():
    with open("404.jpg", 'rb') as f:
        r = requests.post(BASEURL+"/post/image", files={"file": f})
        assert(r.status_code == 200)

if __name__ == "__main__":
    test_drop_and_create_tables()
    test_post_bin_info()
    test_post_fullness()
