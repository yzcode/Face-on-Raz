#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tornado.web
import time
import hashlib
import json
from sqlalchemy import desc

from facelib import apitest as fapi, oface
from database.models import Record, Face

rough_rec = True

trust_table = [
    "",
    "Mingyu Liang",
    "Guangli Peng"
]


class RecordUploadHandler(tornado.web.RequestHandler):
    @property
    def trust_set(self):
        return self.application.trust_set

    @property
    def db(self):
        return self.application.db


    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = hashlib.md5(file1['body']).hexdigest()
        final_filename= fname + extension

        output_file = open("static/uploads/" + final_filename, 'w')
        output_file.write(file1['body'])
        output_file.flush()

        print final_filename, "captured"

        if not rough_rec:
            fapi.search_face("static/uploads/" + final_filename)
        else:
            try:
                record = Record(time=time.strftime('%Y-%m-%d %H:%M:%S'), file_hash=fname, face_id=0, cof='1')
                ret = oface.search_face("static/uploads/" + final_filename, self.trust_set)
                for conf, pre_lable, id in ret:
                    if conf <= 0.5:
                        print "{} is detected with conf {:0.3f}".format(pre_lable, conf)
                        record.face_id = id
                        record.cof = conf

                if record.face_id == 0:
                    print "There might be a stranger"

                self.db.add(record)
                self.db.commit()
                self.db.close()
            except:
                self.write("No face detected!\n")
        self.finish("file" + final_filename + " is uploaded")


class RecordGetHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        start = int(self.get_argument("start"))
        end = int(self.get_argument("end"))
        byname = self.get_argument("name")
        ignore_strange = self.get_argument("ignore_strange", None, 'off')

        face_dic = {0l: 'stranger'}
        for face in self.db.query(Face).all():
            face_dic[face.id] = face.name


        sql_object = self.db.query(Record)
        if ignore_strange == "on":
            sql_object = sql_object.filter(Record.face_id != 0)

        if len(byname) > 0:
            id = self.db.query(Face).filter(Face.name == byname).first().id
            sql_object = sql_object.filter(Record.face_id == id)

        records = sql_object.order_by(desc(Record.id)).limit(end-start).offset(start).all()

        self.finish(json.dumps([{
            'id': record.id,
            'time': record.time.strftime('%Y-%m-%d %H:%M:%S'),
            'name': face_dic[record.face_id],
            'url': '/static/uploads/{}.jpg'.format(record.file_hash)
        } for record in records]))
