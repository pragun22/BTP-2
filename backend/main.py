from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file
import hydrology
import json
import os
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = "userdata"


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/custom_data', methods=['GET', 'POST'])
def file_upload():
    target = "userdata"
    if not os.path.isdir(target):
        os.mkdir(target)
    try:
        infil = request.files['infil']
        forma = infil.filename.split('.')[1]
        infil.save("/".join([target, "infil." + forma]))
        infil = "/".join([target, "infil." + forma])
    except:
        infil = None
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
    filename = hydrology.custom_hydrology(rain, dem, infil, soil)
    print(filename)
    if isinstance(filename, list):
        return jsonify({"url": "http://localhost:8081/static/error.png"}), 200
    return jsonify({"url": "http://localhost:8081/" + filename}), 200


@app.route('/get_map', methods=['GET', 'POST'])
def runner():
    # replace with this later
    # print(request.form['city'], request.form['date'])
    centre, bbox, filename = hydrology.map_hydrology("hyderabad", "07-11-2020")
    print(filename)
    if isinstance(filename, list):
        return jsonify({"err": "An unexpected error occured"}), 500
    else:
        return jsonify({"centre": centre, "bbox": bbox, "url": "http://localhost:8081/" + filename}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
