#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

import tornado.web
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
import numpy as np

from database.db import engine
from database.db import Base
from database.models import Face, Record
from handlers.FaceDetectHandler import RecordUploadHandler, RecordGetHandler
from handlers.TrustlibHandler import TrustAddFaceHandler, TrustDelFaceHandler, TrustGetFaceHandler
from handlers.StatisticHandler import DayPieHandler, DaybarHandler, TopVisHandler

def logging(msg, lv):
    ISOTIMEFORMAT = "%Y-%m-%d %X"
    logtime = time.strftime(ISOTIMEFORMAT, time.localtime())
    lvstr = ["MASSAGE", "WARNING", "ERROR  "]
    print lvstr[lv], logtime, ":", msg


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        faces = self.application.db.query(Face).all()
        records = self.application.db.query(Record).order_by(desc(Record.time)).limit(10).all()
        self.render("index.html", faces=faces, records=records)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/upload", RecordUploadHandler),
            (r"/trustaddface", TrustAddFaceHandler),
            (r"/trustdelface", TrustDelFaceHandler),
            (r"/api/daypie", DayPieHandler),
            (r"/api/daybar", DaybarHandler),
            (r"/api/topvis", TopVisHandler),
            (r"/api/getfaces", TrustGetFaceHandler),
            (r"/api/getrecords", RecordGetHandler),
        ]
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates")
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))
        self.trust_set = []
        for face in self.db.query(Face).all():
            rep = np.load('static/trustlib/{}.npy'.format(face.file_hash))
            self.trust_set.append((face.name, rep, face.id))

    def init_trust_lib(self):
        del self.trust_set[:]
        for face in self.db.query(Face).all():
            rep = np.load('static/trustlib/{}.npy'.format(face.file_hash))
            self.trust_set.append((face.name, rep, face.id))



if __name__ == "__main__":
    print "Loaded!"
    Application().listen(8888)
    Base.metadata.create_all(engine)
    # pc = PeriodicCallback(fetch, 1000 * 60 * 60)
    # pc.start()
    tornado.ioloop.IOLoop.instance().start()