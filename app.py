# built-in library imports
import json
import datetime
import os
import glob

# flask related imports
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, make_response, request, abort, flash, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import between, and_
import pandas

# local custom imports
from error import Error
from config import db, app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import models
import zbce_queries

# TODO: Condense code and create functions/decorators for repeptitive code
# TODO: set the hardlimit somewhere else
limit_request = 1000

@app.route('/')
def main_page():
    return "<h1>ZotBins Community Edition</h1>"

@app.route('/bin-info',methods=['POST', 'GET'])
def bin_info():
    try:
        if request.method == 'POST':
            # Check if JSON request
            if not request.json: raise Error("JSON_FORMAT")

            # Process request data
            post_data = request.json["data"]
            for row in post_data:
                # bin_id, bin_height, location, bin_type, and waste_metrics must be present in body
                if ("ip_address" not in row) or ("bin_height" not in row) or ("location" not in row) or ("bin_type" not in row) or ("waste_metrics" not in row):
                    raise Error("MISSING_KEY")

                # bin_id, bin_height, location, bin_type, and waste_metrics cannot be null
                if (row["ip_address"] is None) or (row["bin_height"] is None) or (row["location"] is None) or (row["bin_type"] is None) or (row["waste_metrics"] is None):
                    raise Error("NULL_VALUE")

                addToDatabase(models.BinInfo(ip_address=row["ip_address"],bin_height=row["bin_height"],\
                                   location=row["location"],bin_type=row["bin_type"],\
                                   waste_metrics=row["waste_metrics"]))

            return "Posted: " + str(request.json), 201
        elif request.method == 'GET':
            bin_id = request.args.get("bin_id") # make sure you have the bin id

            if bin_id is None: # checking is bin exists
                raise Error("NULL_VALUE")
            else:
                # Get entries with same bin_id and between start_timestamp and end_timestamp
                bin_data = models.BinInfo.query.filter(models.BinInfo.id == bin_id).all() # returns the bin data with matching bin id
                if len(bin_data) > 0: # check if the bin id surpasses the amount of bins in database
                    b = bin_data[0]
                    keys = ["id","ip_address","bin_height","location","bin_type","waste_metrics"] # keys
                    vals = [b.id,b.ip_address,b.bin_height,b.location,b.bin_type,b.waste_metrics] # values
                    return jsonify(dict(zip(keys,vals))), 200 # return the json of the keys and values :)
                else:
                    return jsonify({"message": "No Bin Found"}), 404 # return error message is there's an error
    except Error as e:
        return Error.em[str(e)]
    except Exception as e:
        return str(e), 400

@app.route('/bin-info-all',methods=['GET'])
def get_bin_info_all():
    try:
        if request.method == 'GET':
            bins = models.BinInfo.query.all()
            ret = {"data":[]}
            for the_bin in bins:
                keys = ["id","ip_address","bin_height","location","bin_type","waste_metrics"]
                vals = [the_bin.id,the_bin.ip_address,the_bin.bin_height,the_bin.location,the_bin.bin_type,the_bin.waste_metrics]
                ret["data"].append(dict(zip(keys,vals)))
            return jsonify(ret),200
    except Exception as e:
        return str(e), 400

@app.route('/usage',methods=['POST','GET'])
def usage():
    try:
        if request.method == 'POST':
            # Check if JSON request
            if not request.json: raise Error("JSON_FORMAT")
            # Process request data
            post_data = request.json["data"]
            for row in post_data:
                # bin_id and datetime must be present in body
                if ("bin_id" not in row) or ("datetime" not in row):
                    raise Error("MISSING_KEY")

                # bin_id and datetime cannot be null
                if (row["bin_id"] is None) or (row["datetime"] is None):
                   raise Error("NULL_VALUE")

                # Check bin_id and return 400 if invalid bin_id
                thebin = models.BinInfo.query.get(row["bin_id"])
                if thebin is None: raise Error("INVALID_BIN_ID")

                # Add datetimestamp to db
                addToDatabase(models.BinUsage(datetimestamp=row["datetime"], bin=thebin))

            return "Posted: " + str(request.json), 201
        elif request.method == 'GET':
            # Get query parameters
            bin_id = request.args.get("bin_id")
            start_timestamp = request.args.get("start_timestamp")
            end_timestamp = request.args.get("end_timestamp")

            # None of the parameters can be null
            if bin_id is None or start_timestamp is None or end_timestamp is None:
                raise Error("INVALID_PARAM")
            else:
                # Get entries with same bin_id and between start_timestamp and end_timestamp
                usage_data = models.BinUsage.query.filter(and_(models.BinUsage.bin_id == bin_id, between(models.BinUsage.datetimestamp, start_timestamp, end_timestamp))).all()
                ret = {"data":[]}
                for row in usage_data:
                    keys = ["bin_id","timestamp"]
                    vals = [row.bin_id,str(row.datetimestamp)]
                    ret["data"].append(dict(zip(keys,vals)))
                return jsonify(ret), 200

    except Error as e:
        return Error.em[str(e)]
    except Exception as e:
        return str(e), 400

@app.route('/usage-today',methods=['GET'])
def get_usage_today():
    try:
        usage_data = models.BinUsage.query.filter(models.BinUsage.datetimestamp>datetime.datetime.now().strftime("%Y-%m-%d")).all()
        ret = {"data":[]}
        for row in usage_data:
            keys = ["id","datetimestamp", "bin_id"] #["id","datetime","bin_id"]
            vals = [row.id, str(row.datetimestamp), row.bin_id]
            ret["data"].append(dict(zip(keys,vals)))
        return jsonify(ret),200
    except Exception as e:
        return str(e), 400


@app.route('/weight', methods=['POST','GET'])
def weight():
    try:
        if request.method == 'POST':
            # Check if JSON request
            if not request.json: raise Error("JSON_FORMAT")

            post_data = request.json["data"]
            for row in post_data:

                # bin_id, datetime, and weight must be present in body
                if ("bin_id" not in row) or ("datetime" not in row) or ("weight" not in row):
                    raise Error("MISSING_KEY")

                # bin_id, datetime, or weight cannot be null
                if (row["bin_id"] is None) or (row["datetime"] is None) or (row["weight"] is None):
                    raise Error("NULL_VALUE")

                # Check if bin_id and return 400 if invalid bin_id
                thebin = models.BinInfo.query.get(row["bin_id"])
                if thebin is None:
                    raise Error("INVALID_BIN_ID")

                # Add weight data to db
                addToDatabase(models.BinWeight(datetimestamp=row["datetime"], bin_weight=row["weight"], bin=thebin))

            return "Posted: " + str(request.json), 201
        elif request.method == 'GET':
            # Get query parameters
            bin_id = request.args.get("bin_id")
            start_timestamp = request.args.get("start_timestamp")
            end_timestamp = request.args.get("end_timestamp")

            # None of the parameters can be null
            if bin_id is None or start_timestamp is None or end_timestamp is None:
                raise Error("NULL_VALUE")
            else:
                # Get entries with same bin_id and between start_timestamp and end_timestamp
                weight_data = models.BinWeight.query.filter(and_(models.BinWeight.bin_id == bin_id, between(models.BinWeight.datetimestamp, start_timestamp, end_timestamp))).all()
                ret = {"data":[]}
                for row in weight_data:
                    keys = ["timestamp","bin_weight","bin_id"]
                    vals = [str(row.datetimestamp), row.bin_weight, row.bin_id]
                    ret["data"].append(dict(zip(keys,vals)))
                return jsonify(ret), 200

    except Error as e:
        return Error.em[str(e)]
    except Exception as e:
        return str(e), 400

@app.route('/weight-today', methods=['GET'])
def get_weight_today():
    try:
        weight_data = models.BinWeight.query.filter(models.BinWeight.datetimestamp>datetime.datetime.now().strftime("%Y-%m-%d")).all()
        ret = {"data":[]}
        for row in weight_data:
            keys = ["id", "timestamp", "bin_weight", "bin_id"]
            vals = [row.id, str(row.datetimestamp), row.bin_weight, row.bin_id]
            ret["data"].append(dict(zip(keys,vals)))
        return jsonify(ret), 200

    except Exception as e:
        return str(e), 400

@app.route('/fullness',methods=['GET', 'POST'])
def fullness_info():
    try:
        if request.method == 'GET':
            bin_id = request.args.get("bin_id")
            start_timestamp = request.args.get("start_timestamp")
            end_timestamp = request.args.get("end_timestamp")
            #throw error if any required parameters are None
            if bin_id == None or start_timestamp == None or end_timestamp == None:
                raise Error("NULL_VALUE")

            #throw error if start_timestamp > end_timestamp
            if start_timestamp > end_timestamp:
                raise Error("TIMESTAMP_ISSUE")

            bins = models.BinFullness.query.filter(and_(models.BinFullness.bin_id == bin_id, start_timestamp <= models.BinFullness.datetimestamp, end_timestamp >= models.BinFullness.datetimestamp)).all()
            ret = {"data":[]}
            for the_bin in bins:
                keys = ["id","fullness", "bin_id", "datetimestamp"]
                vals = [the_bin.id,the_bin.fullness, the_bin.bin_id, str(the_bin.datetimestamp)]
                ret["data"].append(dict(zip(keys,vals)))

            return jsonify(ret),200

        elif request.method == 'POST':
            # Process request data
            if not request.json: raise Error("JSON_FORMAT")

            post_data = request.json["data"]

            for row in post_data:
                # bin_id, datetime, and fullness must be present in body
                if ("bin_id" not in row) or ("datetime" not in row) or ("fullness" not in row):
                    raise Error("MISSING_KEY")

                # bin_id, datetime, or weight cannot be null
                if (row["bin_id"] is None) or (row["datetime"] is None) or (row["fullness"] is None):
                    raise Error("NULL_VALUE")

                # Check bin_id and return 400 if invalid bin_id
                thebin = models.BinInfo.query.get(row["bin_id"])
                if thebin is None: raise Error("INVALID_BIN_ID")

                # Add fullness to db
                addToDatabase(models.BinFullness(datetimestamp=row["datetime"],fullness=row["fullness"], bin=thebin))

            return "Posted: " + str(request.json), 201

    except Error as e:
        return Error.em[str(e)]

    except Exception as e:
        return str(e), 400

@app.route('/fullness-today',methods=['GET'])
def get_fullness():
    try:
        if request.method == 'GET':
            fullness_data = models.BinFullness.query.filter(models.BinFullness.datetimestamp>datetime.datetime.now().strftime("%Y-%m-%d")).all()
            ret = {"data":[]}
            for the_f in fullness_data:
                keys = ["id","datetimestamp","fullness","bin_id"]
                vals = [the_f.id,str(the_f.datetimestamp),the_f.fullness,the_f.bin_id]
                ret["data"].append(dict(zip(keys,vals)))
            return jsonify(ret),200
    except Exception as e:
        return str(e), 400

@app.route('/image',methods=['POST','GET'])
def post_image():
    """
    Post Request Example:
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part in request')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # gather the datetime stamp for the filename
            curr_datetime = datetime.datetime.utcnow()

            # create filename
            filename = secure_filename(curr_datetime.strftime("%Y-%m-%d_%H-%M-%S") + "_" + file.filename)

            # check if file already exists
            img_path = UPLOAD_FOLDER + '/' + filename
            if os.path.isfile(img_path):
                raise Error("IMAGE_EXISTS")

            # save the file to the upload folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Success", 200 #redirect(url_for('uploaded_file',filename=filename))
    else:
        # return a list of images
        img_names = [os.path.basename(x) for x in glob.glob(UPLOAD_FOLDER + '/*.jpg')]# glob.glob(UPLOAD_FOLDER + '/*.jpg')
        img_names.reverse()
        return jsonify({"image_names": img_names[1:limit_request]}),200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    This function is for viewing the uploaded files we have
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/metric-csv', methods=['GET'])
def get_metrics_as_csv():
    """
    **GET Request Parameters**
    > `metric`
    > `start_timestamp`
    > `end_timestamp`
    """
    try:
        # get request parameters
        metric = request.args.get("metric")
        start_timestamp = request.args.get("start_timestamp")
        end_timestamp = request.args.get("end_timestamp")

        #throw error if any required parameters are None
        if None in [metric, start_timestamp, end_timestamp]:
            raise Error("NULL_VALUE")

        # generate all function queries
        fullness_query = models.BinFullness.query.filter(and_(start_timestamp <= models.BinFullness.datetimestamp, end_timestamp >= models.BinFullness.datetimestamp)).all
        weight_query = models.BinWeight.query.filter(and_(start_timestamp <= models.BinWeight.datetimestamp, end_timestamp >= models.BinWeight.datetimestamp)).all
        usage_query = models.BinUsage.query.filter(and_(start_timestamp <= models.BinUsage.datetimestamp, end_timestamp >= models.BinUsage.datetimestamp)).all

        # generate dict of functions for querying specific data metric
        data_query_func = {"fullness":fullness_query, "weight":weight_query, "usage":usage_query}

        # check if parameters are valid
        if metric not in data_query_func.keys():
            raise Error("INVALID_PARAM")

        #throw error if start_timestamp > end_timestamp
        if start_timestamp > end_timestamp:
            raise Error("TIMESTAMP_ISSUE")

        # call query function
        query_data = data_query_func[metric]()

        # iterate through each row of data
        obj_dict = None
        for row in query_data:
            # convert fullness data into dictionary form such as {key1:str1, key2:str2}
            row_dict_form = dict(row)

            # assign obj_dict to appropriate keys based on model schema
            if not obj_dict:
                headers = row_dict_form.keys()
                # create a dictionary of empty lists such as {key1:[], key2:[]}
                obj_dict = dict(zip(headers, [[] for i in range(len(headers))]))

            # append data to the obj_dict based on keys
            for k in obj_dict.keys():
                obj_dict[k].append(row_dict_form[k])

        # create the pandas dataframe
        df = pandas.DataFrame(obj_dict)
        resp = make_response(df.to_csv(index=False))
        file_name = "{}_{}_{}.csv".format(metric,start_timestamp,end_timestamp)
        resp.headers["Content-Disposition"] = "attachment; filename=" + file_name
        resp.headers["Content-Type"] = "text/csv"

        # return as CSV file
        return resp

    except Error as e:
        return Error.em[str(e)]

    except Exception as e:
        return str(e), 400

def allowed_file(filename):
    """
    Checks whether or not the extension name is allowed.
    """
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

def paramMissing(required_params:tuple,row:iter)->bool:
    for p in required_params:
        if p not in row:
            return True
    return False

#adding to database function
def addToDatabase(data):
    db.session.add(data)
    db.session.commit()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001')
