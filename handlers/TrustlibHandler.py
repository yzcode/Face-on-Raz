#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tornado.web
import hashlib
import numpy as np
import json

from database.models import Face, FaceBind
from facelib.oface import getRep

class TrustAddFaceHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def post(self):
        file1 = self.request.files['file1'][0]

        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = hashlib.md5(file1['body']).hexdigest()
        final_filename = fname + extension

        if len(self.db.query(Face).filter(Face.file_hash == fname).all()) != 0:
            self.finish("Face has already beed uploaded!")
            return

        output_file = open("static/trustlib/" + final_filename, 'w')
        output_file.write(file1['body'])
        output_file.flush()

        try:
            face_rep = getRep("static/trustlib/" + final_filename)
            np.save('static/trustlib/{}'.format(fname), face_rep)

            face_name = self.get_argument('facename')
            new_face = Face(name=face_name, file_hash=fname, face_hash='NULL')
            self.db.add(new_face)

            face_id = self.db.query(Face).filter(Face.file_hash == fname).first().id
            new_face_bind = FaceBind(trust_id=1, face_id=face_id)
            self.db.add(new_face_bind)

            self.db.commit()
            self.db.close()

            self.application.init_trust_lib()

            print final_filename, "captured"
            self.finish("Upload!")
        except:
            print "No face detected!"
            self.finish("No face detected!")


class TrustDelFaceHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        f_hash = self.get_argument("file_hash")
        face = self.db.query(Face).filter(Face.file_hash == f_hash).first()

        if face == None:
            self.finish("No face to delete!")
            return

        self.db.delete(face)
        self.db.commit()
        self.db.close()

        self.application.init_trust_lib()

        self.finish("face deleted!")


class TrustGetFaceHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        faces = self.db.query(Face).all()
        ret = []

        for face in faces:
            ret.append({
                'name': face.name,
                'file_hash': face.file_hash,
                'url': '/static/trustlib/{}.jpg'.format(face.file_hash)
            })

        self.db.close()

        self.finish(json.dumps(ret))
