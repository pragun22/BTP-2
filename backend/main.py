from flask import Flask
from flask import request
from flask import jsonify
import hydrology
import json
app = Flask(__name__)


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/get_map', methods=['GET'])
def runner():
    # needs city and date as param
    centre, bbox, matrix = hydrology.map_hydrology("Mumbai", "10/1/11")
    if len(matrix) == 0:
        return jsonify({"err": "An unexpected error occured"}), 500
    else:
        return jsonify({"centre": centre, "bbox": bbox, "mat": matrix.tolist()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
