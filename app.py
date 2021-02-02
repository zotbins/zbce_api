# library imports
import json
import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, make_response, request, abort, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from sqlalchemy import between, and_

# local imports
from config import db, app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import models
import zbce_queries

# TODO: Condense code and create functions/decorators for repeptitive code

@app.route('/')
def main_page():
    return "<h1>ZotBins Community Edition</h1>"

@app.route('/post/bin-info',methods=['POST'])
def post_bin_info():
    """
    Body Example:
    {
      "data": [
        {
          "ip_address": "dummy",
          "bin_height": 100,
          "location": "your_place",
          "bin_type": "R",
          "waste_metrics": "FP"
        }
      ]
    }
    """
    try:
        if request.method == 'POST':
            # Check if JSON request
            if not request.json: return "Request body is not in JSON format", 400

            # Process request data
            post_data = request.json["data"]
            for row in post_data:
                # bin_id, bin_height, location, bin_type, and waste_metrics must be present in body
                if ("ip_address" not in row) or ("bin_height" not in row) or ("location" not in row) or ("bin_type" not in row) or ("waste_metrics" not in row):
                    return "Missing key in body", 400

                # bin_id, bin_height, location, bin_type, and waste_metrics cannot be null
                if (row["ip_address"] is None) or (row["bin_height"] is None) or (row["location"] is None) or (row["bin_type"] is None) or (row["waste_metrics"] is None):
                    return "Values cannot be null", 400


                bin_data = models.BinInfo(ip_address=row["ip_address"],bin_height=row["bin_height"],\
                                   location=row["location"],bin_type=row["bin_type"],\
                                   waste_metrics=row["waste_metrics"])
                db.session.add(bin_data)
                db.session.commit()
            return "Posted: " + str(request.json), 201
    except Exception as e:
        return str(e), 400


@app.route('/bin-info/all',methods=['GET'])
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

@app.route('/post/usage',methods=['POST'])
def post_usage():
    """
    Body Example:
    {
      "data": [
        {
          "bin_id": 1,
          "datetime": "2020-11-04 15:06:25"
        }
      ]
    }
    """
    try:
        if request.method == 'POST':
            # Check if JSON request
            if not request.json: return "Request body is not in JSON format", 400
            # Process request data
            post_data = request.json["data"]
            for row in post_data:
                # bin_id and datetime must be present in body
                if ("bin_id" not in row) or ("datetime" not in row):
                    return "Missing key in body",

                # bin_id and datetime cannot be null
                if (row["bin_id"] is None) or (row["datetime"] is None):
                    return "Values cannot be null", 400

                # Check bin_id and return 400 if invalid bin_id
                thebin = models.BinInfo.query.get(row["bin_id"])
                if thebin is None: return "Invalid bin_id", 400

                # Add datetimestamp to db
                usage_data = models.BinUsage(datetimestamp=row["datetime"], bin=thebin)
                db.session.add(usage_data)
                db.session.commit()
            return "Posted: " + str(request.json), 201
    except Exception as e:
        return str(e), 400

@app.route('/usage/all',methods=['GET'])
def get_usage_all():
    try:
        if request.method == 'GET':
            usages = models.BinUsage.query.all()
            ret = {"data":[]}
            for u in usages:
                keys = ["id","datetime","bin_id"]
                vals = [u.id,str(u.datetimestamp),u.bin_id]
                ret["data"].append(dict(zip(keys,vals)))
            return jsonify(ret),200
    except Exception as e:
        return str(e), 400



@app.route('/post/fullness',methods=['POST'])
def post_fullness():
    """
    Body Example:
    {
      "data": [
        {
          "datetime": "2015-11-04 15:06:25",
          "fullness": 50,
          "bin_id": 1
        }
      ]
    }
    """
    try:
        if request.method == 'POST':
            # Check if JSON request
            if not request.json: return "Request body is not in JSON format", 400

            # Process request data
            post_data = request.json["data"]
            for row in post_data:
                # bin_id, datetime, and fullness must be present in body
                if ("bin_id" not in row) or ("datetime" not in row) or ("fullness" not in row):
                    return "Missing key in body", 400

                # bin_id, datetime, or weight cannot be null
                if (row["bin_id"] is None) or (row["datetime"] is None) or (row["fullness"] is None):
                    return "Values cannot be null", 400

                # Check bin_id and return 400 if invalid bin_id
                thebin = models.BinInfo.query.get(row["bin_id"])
                if thebin is None: return "Invalid bin_id", 400

                # Add fullness to db
                fullness_data = models.BinFullness(datetimestamp=row["datetime"],fullness=row["fullness"], bin=thebin)
                db.session.add(fullness_data)
                db.session.commit()
            return "Posted: " + str(request.json), 201
    except Exception as e:
        return str(e), 400

@app.route('/bin-fullness/all',methods=['GET'])
def get_fullness_all():
    try:
        if request.method == 'GET':
            fullness_data = models.BinFullness.query.all()
            ret = {"data":[]}
            for the_f in fullness_data:
                keys = ["id","datetimestamp","fullness","bin_id"]
                vals = [the_f.id,str(the_f.datetimestamp),the_f.fullness,the_f.bin_id]
                ret["data"].append(dict(zip(keys,vals)))
            return jsonify(ret),200
    except Exception as e:
        return str(e), 400

@app.route('/post/weight', methods=['POST'])
def post_weight():
    """
    Body Example:
    {
        "data": [
            {
                "datetime": "2015-11-04 15:06:25",
                "weight": 25,
                "bin_id": 1
            }
        ]
    }
    """
    try:
        if request.method == 'POST':
            # Check if JSON request
            if not request.json: return "Request body is not in JSON format", 400

            post_data = request.json["data"]
            for row in post_data:

                # bin_id, datetime, and weight must be present in body
                if ("bin_id" not in row) or ("datetime" not in row) or ("weight" not in row):
                    return "Missing key in body", 400

                # bin_id, datetime, or weight cannot be null
                if (row["bin_id"] is None) or (row["datetime"] is None) or (row["weight"] is None):
                    return "Values cannot be null", 400

                # Check if bin_id and return 400 if invalid bin_id
                thebin = models.BinInfo.query.get(row["bin_id"])
                if thebin is None:
                    return "Invalid bin_id", 400

                # Add weight data to db
                weight_data = models.BinWeight(datetimestamp=row["datetime"], bin_weight=row["weight"], bin=thebin)
                db.session.add(weight_data)
                db.session.commit()
            return "Posted: " + str(request.json), 201
    except Exception as e:
        return str(e), 400


@app.route('/weight/all', methods=['GET'])
def get_weight_all():
    try:
        weight_data = models.BinWeight.query.all()
        ret = {"data":[]}
        for row in weight_data:
            keys = ["timestamp","bin_weight","bin_id"]
            vals = [str(row.datetimestamp), row.bin_weight, row.bin_id]
            ret["data"].append(dict(zip(keys,vals)))
        return jsonify(ret), 200

    except Exception as e:
        return str(e), 400


@app.route('/weight', methods=['GET'])
def get_weight():
    """
    Example Parameters:
    bin_id = 1
    start_timestamp = 2015-11-04 15:06:25
    end_timestamp = 2015-11-05 15:06:25
    """
    try:
        # Get query parameters
        bin_id = request.args.get("bin_id")
        start_timestamp = request.args.get("start_timestamp")
        end_timestamp = request.args.get("end_timestamp")

        # None of the parameters can be null
        if bin_id is None or start_timestamp is None or end_timestamp is None:
            return "Invalid parameter(s)", 400
        else:
            # Get entries with same bin_id and between start_timestamp and end_timestamp
            weight_data = models.BinWeight.query.filter(and_(models.BinWeight.bin_id == bin_id, between(models.BinWeight.datetimestamp, start_timestamp, end_timestamp))).all()
            ret = {"data":[]}
            for row in weight_data:
                keys = ["timestamp","bin_weight","bin_id"]
                vals = [str(row.datetimestamp), row.bin_weight, row.bin_id]
                ret["data"].append(dict(zip(keys,vals)))
            return jsonify(ret), 200

    except Exception as e:
        return str(e), 400

@app.route('/post/image',methods=['POST','GET'])
def post_image():
    """
    Post Request Example:
    """
    ip_addr = request.remote_addr
    if request.method == 'POST':
        if zbce_queries.ip_bin_id(ip_addr) == None:
            return "Invalid Ip Address", 400
        if 'file' not in request.files:
            flash('no file part in request')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        img_path = UPLOAD_FOLDER + '/' + file.filename
        if os.path.isfile(img_path):
            return "Image already exists", 400

        if file and allowed_file(file.filename):
            # extract the extension of the file
            ext = file.filename.split('.')[-1]

            # gather the datetime stamp for the filename
            curr_datetime = datetime.datetime.utcnow()
            filename = secure_filename(curr_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f") + "_" + ip_addr.replace(".","-") +  "." +  ext)

            # save the file to the upload folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Success", 200 #redirect(url_for('uploaded_file',filename=filename))

    return '''
        <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    This function is for viewing the uploaded files we have
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

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

# @app.route('/observation/get/image-list', methods=['GET'])
# def image_names():
#     onlyfiles = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
#     return jsonify({"imageNames":onlyfiles})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)
