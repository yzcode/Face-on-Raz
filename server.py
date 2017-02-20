#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import time
import random
import os
import string
from tornado.ioloop import PeriodicCallback



def logging(msg, lv):
    ISOTIMEFORMAT = "%Y-%m-%d %X"
    logtime = time.strftime(ISOTIMEFORMAT, time.localtime())
    lvstr = ["MASSAGE", "WARNING", "ERROR  "]
    print lvstr[lv], logtime, ":", msg


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        pass



class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename= fname+'.jpg'
        output_file = open("uploads/" + final_filename, 'w')
        output_file.write(file1['body'])
        self.finish("file" + final_filename + " is uploaded")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", UploadHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    # pc = PeriodicCallback(fetch, 1000 * 60 * 60)
    # pc.start()
    tornado.ioloop.IOLoop.instance().start()