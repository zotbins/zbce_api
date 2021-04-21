# built-in library imports
import json
import datetime
import os
import glob

# flask related imports
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, make_response, request, abort, flash, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import between, and_

# local custom imports
from error import Error
from config import db, app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import models
import zbce_queries

# TODO: Condense code and create functions/decorators for repeptitive code

@app.route('/')
def main_page():
    return "<h1>ZotBins Community Edition</h1>"

@app.route('/bin-info',methods=['POST'])
def post_bin_info():
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

                bin_data = models.BinInfo(ip_address=row["ip_address"],bin_height=row["bin_height"],\
                                   location=row["location"],bin_type=row["bin_type"],\
                                   waste_metrics=row["waste_metrics"])
                db.session.add(bin_data)
                db.session.commit()
            return "Posted: " + str(request.json), 201
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
def post_usage():
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
                usage_data = models.BinUsage(datetimestamp=row["datetime"], bin=thebin)
                db.session.add(usage_data)
                db.session.commit()
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

@app.route('/usage-all',methods=['GET'])
def get_usage_all():
    try:
        if request.method == 'GET':
            usages = models.BinUsage.query.order_by(models.BinUsage.datetimestamp.desc()).limit(50).all()
            ret = {"data":[]}
            for u in usages:
                keys = ["id","datetime","bin_id"]
                vals = [u.id,str(u.datetimestamp),u.bin_id]
                ret["data"].append(dict(zip(keys,vals)))
            return jsonify(ret),200
    except Exception as e:
        return str(e), 400

@app.route('/weight', methods=['POST','GET'])
def post_weight():
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
                weight_data = models.BinWeight(datetimestamp=row["datetime"], bin_weight=row["weight"], bin=thebin)
                db.session.add(weight_data)
                db.session.commit()
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

@app.route('/weight-all', methods=['GET'])
def get_weight_all():
    try:
        weight_data = models.BinWeight.query.order_by(models.BinWeight.datetimestamp.desc()).limit(50).all()
        ret = {"data":[]}
        for row in weight_data:
            keys = ["timestamp","bin_weight","bin_id"]
            vals = [str(row.datetimestamp), row.bin_weight, row.bin_id]
            ret["data"].append(dict(zip(keys,vals)))
        return jsonify(ret), 200

    except Exception as e:
        return str(e), 400

@app.route('/fullness',methods=['GET', 'POST'])
def get_fullness_info():
    try:
        if request.method == 'GET':
            bin_id = request.args.get("id")
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
                fullness_data = models.BinFullness(datetimestamp=row["datetime"],fullness=row["fullness"], bin=thebin)
                db.session.add(fullness_data)
                db.session.commit()
            return "Posted: " + str(request.json), 201

    except Error as e:
        return Error.em[str(e)]

    except Exception as e:
        return str(e), 400

@app.route('/fullness-all',methods=['GET'])
def get_fullness():
    try:
        if request.method == 'GET':
            fullness_data = models.BinFullness.query.order_by(models.BinFullness.datetimestamp.desc()).limit(50).all()
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
            filename = secure_filename(curr_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f") + "_" + file.filename)

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
         # TODO: include a hard limit on the number of files returned (current set at 1000)
        return jsonify({"image_names": img_names[1:1000]}),200

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
    app.run(host='0.0.0.0', port='5001')
