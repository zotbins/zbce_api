# ZotBins Community Edition API's

| #   | Method   | Endpoint     |
| :-- | :---     | :---         |
| 1   | POST/GET | /bininfo      |
| 2   | GET      | /bininfo-all  |
| 3   | POST/GET | /weight       |
| 4   | GET      | /weight-all   |
| 5   | POST/GET | /fullness     |
| 6   | GET      | /fullness-all |
| 7   | POST/GET | /usage        |
| 8   | GET      | /usage-all    |
| 9   | POST/GET | /image        |


## /bininfo

#### POST:
> **Body Example:**
>
> ```json
> {
>    "data": [
>        {
>            "ip_address": "127.0.0.1",
>            "bin_height": 50,
>            "location": "kitchen1",
>            "bin_type": "R",
>            "waste_metrics": "FP"
>        }
>    ]
>}
> ```
>
> **Request Example (Python):**
> ```python
>import requests
>postRequest = {"data":[{"ip_address":127.0.0.1,"bin_height":50,"location":"kitchen1","bin_type":"R","waste_metrics":"FP"}]}
>r = requests.post("http:127.0.0.1/bininfo", data=json.dumps(postRequest),headers={"Content-Type": "application/json","Accept": "application/json"})
>print(r.content)
>assert(r.status_code == 201)
>```

#### GET [In-Progress]:
> **Body Example:**
>
> ```json
> {"bin-id":1}
> ```



## /bininfo-all

#### GET:

> **Request Example (Python)**:
>
> ```python
> import requests
> r = requests.get(url="http://127.0.0.1/bininfo-all")
>print(r.json())
>assert(r.status_code == 200)
> ```
> **Request Example (curl)**:
> ```bash
>curl http://127.0.0.1/bininfo-all
> ```
> **Response Example**
>```json
>{
>  "data": [
>    {
>      "bin_height": 50,
>      "bin_type": "R",
>      "id": 1,
>      "ip_address": "127.0.0.1",
>      "location": "kitchen1",
>      "waste_metrics": "FP"
>    }
>  ]
>}
> ```
## /weight

#### POST:

> **Body Example:**
>
> ```json
>{
>  "data": [
>    {
>      "datetime": "2020-11-04 15:06:25",
>      "weight": 25,
>      "bin_id": 1
>    }
>  ]
>}
> ```
>
> **Request Example (Python):**
>
> ```python
>import requests
>postRequest = {"data":[{"datetime": "2020-11-04 15:06:25","weight": 25,"bin_id": 1}]}
>r = requests.post(BASEURL+"/post/weight",data=json.dumps(postRequest),headers={"Content-Type": "application/json","Accept": "application/json"})
>print(r.json)
>assert(r.status_code == 201)
> ```

#### GET:

> **Body Example:**
>
> ```json
>{"bin_id":1,"start_timestamp":"2014-11-04 15:06:25","end_timestamp":"2021-01-29 15:06:25"}
> ```
>
> **Request Example (Python):**
>
> ```python
>import requests
>params = {"bin_id":1,"start_timestamp":"2014-11-04 15:06:25","end_timestamp":"2021-01-29 15:06:25"}
>r = requests.get("http://127.0.0.1/weight",params=params,headers={"Content-Type": >"application/json","Accept": "application/json"})
>print(r.json)
>assert(r.status_code==200)
> ```
> **Request Example (curl):**
> ```bash
>curl 'http://127.0.0.1/weight?bin_id=1&start_timestamp=2014-11-04%2015:06:25&end_timestamp=2016-11-04%2015:06:25'
>```
> **Response Example**:
> ```json
>{
>  "data": [
>    {
>      "bin_id": 1,
>      "bin_weight": 25.0,
>     "timestamp": "2015-11-04 15:06:25"
>    }
>  ]
>}
> ```

## /weight-all

#### GET:

> **Request Example (Python)**:
>
> ```python
>import requests
>r = requests.get(url="http://127.0.0.1/weight-all")
>print(r.json)
>assert(r.status_code == 200)
> ```
> **Request Example (curl)**:
> ```bash
>curl http:127.0.0.1/weight-all
>```
> **Response Example**:
> ```json
>{
>  "data": [
>    {
>      "bin_id": 1,
>      "bin_weight": 25.0,
>      "timestamp": "2015-11-04 15:06:25"
>    }
>  ]
>}
> ```

## /fullness

#### POST:
> **Body Example:**
>
> ```json
>{
>  "data": [
>    {
>      "datetime": "2015-11-04 15:06:25",
>      "fullness": 50,
>      "bin_id": 1
>    }
>  ]
>}
> ```
>
> **Request Example (Python):**
>
> ```python
>import requests
>postRequest = {"data":[{"datetime":"2015-11-04 15:06:25","fullness":50,"bin_id":1}]}
>r = requests.post("http://127.0.0.1/fullness", data=json.dumps(postRequest),headers={"Content-Type": "application/json","Accept": "application/json"})
>print(r.content)
>assert(r.status_code == 201)
> ```


#### GET:

> **Body Example:**
>
> ```json
>{
>    "start_timestamp": "2014-11-04 15:06:25",
>    "end_timestamp": "2021-01-29 15:06:25",
>    "bin_id": 1
>}
> ```
>
> **Request Example (Python):**
>
> ```python
>import requests
>params = {"start_timestamp":"2019-11-04 15:06:25","end_timestamp":"2021-01-29 15:06:25","bin_id":1}
>r = requests.get(BASEURL+"/fullness", params=params,headers={"Content-Type": "application/json","Accept": "application/json"})
>print(r.json)
>assert(r.status_code == 200)
> ```
> **Request Example (curl):**
> ```bash
>curl 'http://127.0.0.1/fullness?start_timestamp=2019-11-04%2015:06:25&end_timestamp=2021-01-29%2015:06:25&bin_id=1'
>```
> **Response Example**
>```json
>{
>  "data": [
>    {
>      "bin_id": 1,
>      "bin_fullness": 25.0,
>      "timestamp": "2015-11-04 15:06:25"
>    }
>  ]
>}
>```
## fullness-all

**GET:**
> **Request Example (Python)**
> ```python
>import requests
>r = requests.get(url="http://127.0.0.1/fullness-all")
>print(r.json)
>assert(r.status_code == 200)
>```
> **Response Example**
>```json
>{
>  "data": [
>    {
>      "bin_id": 1,
>     "bin_fullness": 25.0,
>      "timestamp": "2015-11-04 15:06:25"
>    }
>  ]
>}
>```

## /usage

**POST:**

> **Body Example:**
> ```json
>{
>    "data": [
>        {
>            "bin_id": 1,
>            "datetime": "2020-11-04 15:06:25"
>        }
>    ]
>}
> ```
>
> **Request Example (Python):**
>
> ```python
>import requests
>postRequest = {"data":[{"bin_id":1,"datetime":"2020-11-04 15:06:25"}]}
>r = requests.post(BASEURL + "/usage", data=json.dumps(postRequest),headers={"Content-Type": "application/json","Accept": "application/json"})
>assert(r.status_code == 201)
> ```

#### GET:

> **Body Example:**
>
> ```json
>{
>   "start_timestamp": "2014-11-04 15:06:25",
>   "end_timestamp": "2021-01-29 15:06:25",
>    "bin_id": 1
>}
> ```
>
> **Request Example (Python):**
>
> ```python
>import requests
>params = {"start_timestamp":"2019-11-04 15:06:25","end_timestamp":"2021-01-29 15:06:25","bin_id":1}
>r = requests.get("http://127.0.0.1/usage", params=params, headers={"Content-Type": >"application/json","Accept": "application/json"})
>print(r.json)
>assert(r.status_code == 200)
> ```
> **Request Example (curl):**
>```bash
>curl 'http://127.0.0.1/usage?bin_id=1&start_timestamp=2014-11-04%2015:06:25&end_timestamp=2016-11-04%2015:06:25'
>```
>
> **Response Example**
> ```json
>{
>  "data": [
>    {
>      "bin_id": 1,
>      "timestamp": "2015-11-04 15:06:25"
>    }
>  ]
>}
> ```
## usage-all

#### GET:

> **Request Example (Python):**
>
> ```python
>import requests
>r = requests.get(url="http://127.0.0.1/usage-all")
>print(r.json)
>assert(r.status_code == 200)
> ```
> **Request Example (curl):**
>
> ```bash
>curl 'http://127.0.0.1/usage-all'
>```
> **Response Example**
> ```json
>{
>  "data": [
>    {
>      "bin_id": 1,
>      "timestamp": "2015-11-04 15:06:25"
>    }
>  ]
>}
> ```
