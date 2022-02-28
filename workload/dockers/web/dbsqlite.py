from flask import Flask, request, jsonify, g, abort
import sqlite3
import hashlib

def init_db_sqlite3():
    db = get_db_sqlite3()
    sql = """
CREATE TABLE IF NOT EXISTS `sensor` (
`id` bigint PRIMARY KEY,
`device` varchar(128) NOT NULL,
`ts` double NOT NULL,
`seq` bigint NOT NULL,
`dsize` int NOT NULL,
`dhash` varchar(128) NOT NULL
)
"""
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()

def get_db_sqlite3():
    if 'db' not in g:
        g.db = sqlite3.connect("iot.db")
        init_db_sqlite3()

    return g.db

def insert_record_sqlite3(r):
    m = hashlib.md5()
    m.update(r["sensor_data"].encode('utf-8'))
    dhash = m.hexdigest()[:30]

    db = get_db_sqlite3()
    sql = """
INSERT INTO `sensor` (device, ts, seq, dsize, dhash) 
VALUES (?,?,?,?,?)
"""
    cursor = db.cursor()
    cursor.execute(sql, (r["dev_id"], r["ts"],
                   r["seq_no"], r["data_size"], dhash))
    db.commit()
    cursor.close()

def query_record_sqlite3(page):
    sql = """
SELECT * FROM `sensor` LIMIT 10 OFFSET %d
""" % (page * 10,)
    db = get_db_sqlite3()
    cursor = db.cursor()
    rows = cursor.execute(sql)
    records = []
    for row in rows:
        records.append({'id': row[0], 'device': row[1], 'ts': row[2],
                       'seq': row[3], 'size': row[4], 'hash': row[5]})
    db.commit()
    cursor.close()
    return records