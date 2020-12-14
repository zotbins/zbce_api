"""
1. Change the BASEURL variable to match your BASEURL
2. Make sure your Flask server is running
3. Run the following test using pytest:
        pytest -q unit_tests.py

(WARNING: this will delete the exists data in the database by dropping all the tables)
"""
# library imports
import datetime, time
import json
import requests

# local imports
import create_tables

# global variables
BASEURL = "YOUR_URL_HERE"
HEADERS = {"Content-Type": "application/json","Accept": "application/json"}

def test_drop_and_create_tables():
    create_tables.recreate_tables()

def test_main_page():
    r = requests.get(url=BASEURL)
    assert(r.status_code==200)

def test_post_bin_info():
    postRequest = {"data":[{"ip_address":"dummy","bin_height":100,"location":"your_place","bin_type":"R","waste_metrics":"FP"}]}
    r = requests.post(BASEURL + "/post/bin-info", data=json.dumps(postRequest),headers=HEADERS)
    assert(r.status_code == 200)

def test_get_bin_info():
    r = requests.get(url=BASEURL+"/bin-info/all")
    data = r.json()
    print(data)
    assert(r.status_code == 200)

def test_post_fullness():
    postRequest = {"data":[{"datetime":"2015-11-04 15:06:25","fullness":50,"bin_id":1}]}
    r = requests.post(BASEURL+"/post/fullness", data=json.dumps(postRequest),headers=HEADERS)
    assert(r.status_code == 200)

def test_get_fullness():
    r = requests.get(url=BASEURL + "/bin-fullness/all")
    data = r.json()
    print(data)
    assert(r.status_code == 200)

def test_post_image():
    with open("404.jpg", 'rb') as f:
        r = requests.post(BASEURL+"/post/image", files={"file": f})
        assert(r.status_code == 200)

def test_get_image():
    r = requests.get(url=BASEURL + "/uploads/404.jpg")
    assert(r.status_code == 200)
