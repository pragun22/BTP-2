from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file
import hydrology
import json
import os
from flask_cors import CORS
import rain_pred
app = Flask(__name__)

# allow cross origin access
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = "userdata"

# Takes custom data for catchment and performs hydrology mapping
@app.route('/custom_data', methods=['GET', 'POST'])
def file_upload():
    target = "userdata"
    if not os.path.isdir(target):
        os.mkdir(target)
    # check if infiltration data is uploaded
    try:
        infil = request.files['infil']
        forma = infil.filename.split('.')[1]
        infil.save("/".join([target, "infil." + forma]))
        infil = "/".join([target, "infil." + forma])
    except:
        infil = None
    # checks if soil data is uploaded
    try:
        soil = request.files['soil']
        forma = soil.filename.split('.')[1]
        soil.save("/".join([target, "soil." + forma]))
        soil = "/".join([target, "soil." + forma])
    except:
        soil = None
    dem = request.files['dem']
    forma = dem.filename.split('.')[1]
    dem.save("/".join([target, "dem." + forma]))
    dem = "/".join([target, "dem." + forma])
    try:
        rain = int(request.form['rain'])
    except:
        rain = request.files['rain']

    # calls hydrology mapping function which returns a plot
    filename = hydrology.custom_hydrology(rain, dem, infil, soil)
    if isinstance(filename, list):
        return jsonify({"url": "http://localhost:8081/static/error.png"}), 200
    return jsonify({"url": "http://localhost:8081/" + filename}), 200

# Performs hydrology mapping for city and returns a plot
@app.route('/get_map', methods=['GET', 'POST'])
def runner():
    # get city and date from request
    city = request.form['city']
    date = request.form['date']
    centre, bbox, filename, rainfall = hydrology.map_hydrology(city, date)
    if isinstance(filename, list):
        return jsonify({"err": "An unexpected error occured"}), 500
    else:
        return jsonify({"centre": centre, "bbox": bbox, "url": "http://localhost:8081/" + filename, "rainfall":rainfall}), 200

# Takes time series as input and predicts rainfall.
@app.route('/rain_pred', methods=['GET', 'POST'])
def rainfall_prediction():
	return jsonify({"url": "http://localhost:8081/" + rain_pred.pred()}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
