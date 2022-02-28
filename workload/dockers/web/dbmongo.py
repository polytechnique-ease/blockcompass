from flask import Flask, request, jsonify, g, abort
from sys import getsizeof
from pymongo import MongoClient
import os
import hashlib
import requests
import json

def get_db_mongo():
    if 'db' not in g:
        user = os.environ.get("ME_CONFIG_MONGODB_ADMINUSERNAME")
        passwd = os.environ.get("ME_CONFIG_MONGODB_ADMINPASSWORD")
        g.mg_client = MongoClient(
            "mongodb://%s:%s@%s:27017/" % (user, passwd, "db"))
        g.db = g.mg_client.iot
        print(user, passwd, g.mg_client, g.db)
    return g.db


def insert_record_mongo(r):
    m = hashlib.md5()
    m.update(r["sensor_data"].encode('utf-8'))
    dhash = m.hexdigest()[:30]

    url = "http://service.localhost:3000/invoke"
    args = [str(r["dev_id"]), str(r["sensor_data"][0:10000])]

    payload = {"function": "Write", "args": args}
    # print("send data: ")
    # print(str(r["sensor_data"][0:128]))
    print("bytes:")
    print(str(r["sensor_data"][0:10000]))
    print(getsizeof(args))
    headers = {'content-type': "application/json"}
    # payload = { "record_id":uuid.uuid4().hex, "device": str(r["dev_id"]), "ts": str(r["ts"]), "seq": str(r["seq_no"]), "ddata": str(r["sensor_data"][0:128]), "dsize": str(r["data_size"]), "dhash": str(dhash) }
    response = requests.request(
        "POST", url, data=json.dumps(payload), headers=headers)
    # reply = json.loads(response.status_code)
    if response.status_code == 200:
        return 1
    return 0


def query_record_mongo(page):
    db = get_db_mongo()
    records = []
    for r in db.sensors.find().limit(10).skip(page * 10):
        records.append(r)
    return records