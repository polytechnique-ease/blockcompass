from flask import Flask, request, jsonify, g, abort
import json
import logging
import dbmongo

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True

@app.route("/sensor/add", methods=['POST'])
def add_sensor_record():
    data = json.loads(request.get_data())
    status = dbmongo.insert_record_mongo(data)
    if status == 1:
        return jsonify({"status": status})
    abort(400)


@app.route("/sensor/query/<int:page>")
def query_sensor_record(page):
    return jsonify(dbmongo.query_record_mongo(page))


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=False, port=80)
