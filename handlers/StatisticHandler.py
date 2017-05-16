#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tornado.web
import datetime
import json
from sqlalchemy import func
from sqlalchemy import desc

from database.models import Record, Face


class DayPieHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        current_time = datetime.datetime.now()
        one_day_ago = current_time - datetime.timedelta(hours=24)

        ret = {
            'trust': self.db.query(func.count(Record.id)).filter(Record.time > one_day_ago).filter(Record.face_id!=0).first()[0],
            'stranger': self.db.query(func.count(Record.id)).filter(Record.time > one_day_ago).filter(Record.face_id==0).first()[0],
        }
        self.finish(json.dumps(ret))


class DaybarHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        current_time = datetime.datetime.now()
        one_day_ago = current_time - datetime.timedelta(hours=24)

        ret = [0 for _ in range(24)]
        for record in self.db.query(Record).filter(Record.time > one_day_ago).all():
            ret[record.time.hour] += 1

        self.finish(json.dumps(ret))


class TopVisHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        current_time = datetime.datetime.now()
        one_day_ago = current_time - datetime.timedelta(hours=24)

        ret = []
        ans = self.db.query(Record.face_id, func.count(Record.face_id))\
            .filter(Record.time > one_day_ago).filter(Record.face_id != 0)\
            .group_by(Record.face_id).order_by(desc(func.count(Record.face_id))).all()

        for fid, cnt in ans:
            face = self.db.query(Face).filter(Face.id == fid).first()
            ret.append(
                {
                    'name': face.name,
                    'count': cnt,
                    'url': '/static/trustlib/{}.jpg'.format(face.file_hash)
                }
            )

        self.finish(json.dumps(ret))



