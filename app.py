# library imports
import json
import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, make_response, request, abort, flash, send_from_directory
from werkzeug.utils import secure_filename
import os

# local imports
from config import db, app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import models

@app.route('/')
def main_page():
    return "<h1>ZotBins Community Edition</h1>"

@app.route('/post/bin-info',methods=['POST'])
def post_bin_info():
    """
    Post Request Example:
    {"data":[{"mac_address":"dummy","bin_height":100,"location":"your_place","bin_type":"R","waste_metrics":"FP"}]
    """
    if request.method == 'POST':
        if not request.json:
            abort(400)
        post_data = request.json["data"]
        for row in post_data:
            # TODO: check for duplicate ip_addresses and return an error
            bin_data = models.BinInfo(ip_address=row["ip_address"],bin_height=row["bin_height"],\
                               location=row["location"],bin_type=row["bin_type"],\
                               waste_metrics=row["waste_metrics"])
            db.session.add(bin_data)
            db.session.commit()
        return "Created: " + str(request.json), 200

@app.route('/bin-info/all',methods=['GET'])
def get_bin_info():
    """
    """
    if request.method == 'GET':
        bins = models.BinInfo.query.all()
        ret = {"data":[]}
        for the_bin in bins:
            keys = ["id","ip_address","bin_height","location","bin_type","waste_metrics"]
            vals = [the_bin.id,the_bin.ip_address,the_bin.bin_height,the_bin.location,the_bin.bin_type,the_bin.waste_metrics]
            ret["data"].append(dict(zip(keys,vals)))
    return jsonify(ret),200

@app.route('/post/fullness',methods=['POST'])
def post_fullness():
    """
    Post Request Example:
    {"data":[{"datetime":"2015-11-04 15:06:25","fullness":50,"bin_id":1 }]
    }
    """
    if request.method == 'POST':
        if not request.json:
            abort(400)
        post_data = request.json["data"]
        for row in post_data:
            # TODO: handle invalid or non-existent bin_id input
            thebin = models.BinInfo.query.get(row["bin_id"]) # filter_by(id=row["bin_id"]).first()
            fullness_data = models.BinFullness(datetimestamp=row["datetime"],fullness=row["fullness"], bin=thebin)
            db.session.add(fullness_data)
            db.session.commit()
    return "Created: " + str(request.json), 200

@app.route('/bin-fullness/all',methods=['GET'])
def get_fullness():
    """
    """
    if request.method == 'GET':
        fullness_data = models.BinFullness.query.all()
        ret = {"data":[]}
        for the_f in fullness_data:
            keys = ["id","datetimestamp","fullness","bin_id"]
            vals = [the_f.id,str(the_f.datetimestamp),the_f.fullness,the_f.bin_id]
            ret["data"].append(dict(zip(keys,vals)))
    return jsonify(ret),200


@app.route('/post/image',methods=['POST','GET'])
def post_image():
    """
    Post Request Example:
    """
    if request.method == 'POST':
        print(request)
        print(request.files)
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
            filename = secure_filename(curr_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f") + "." +  ext)

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

# @app.route('/observation/get/image-list', methods=['GET'])
# def image_names():
#     onlyfiles = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
#     return jsonify({"imageNames":onlyfiles})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)
