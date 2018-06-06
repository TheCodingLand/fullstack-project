#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import redis
import threading
import sys
import logging

if os.getenv('LOGFILE'):
    logfile = '%s' % os.environ['LOGFILE']


if 'Telephony' in logfile:
    from project.log_parser.telephony_log import TelephonyLog as Log
else:
    from project.log_parser.presence_log import PresenceLog as Log

conn = redis.StrictRedis(host="redis", port=6379, db=2)


class parseLog(threading.Thread):

    def __init__(self, logfile):
        threading.Thread.__init__(self)
        self.kill_received = False
        self.LogFile = logfile
        self.line = ""
        self.num_lines = 0
        self.filesize = 0
        self.oldfilesize = 0
        self.f = ""
        self.percent = 0

    def parseline(self):
        e = Log(self.line)
        e.parse()

    def run(self):
        self.f = open(self.LogFile)
        logging.warning("opened file %s" % (self.LogFile))

        self.num_lines = sum(1 for line in self.f)
        self.f.close()
        self.f = open(self.LogFile)
        self.filesize = os.stat(self.LogFile).st_size
        self.oldfilesize = self.filesize
        logging.warning("Starting Parsing of log...")
        i=0
        while not self.kill_received:
            if i>100:
                logging.warning(f"log still running {self.LogFile}")
                i=0
            
            self.filesize = os.stat(self.LogFile).st_size
            if self.filesize < self.oldfilesize:  # check if file has been rotated
                self.f.close()
                self.f = open(self.LogFile)
            self.oldfilesize = self.filesize
            self.line = self.f.readline()
            if self.line != '':
                self.parseline()
                k = conn.keys('*')
                while len(k) > 2:
                    time.sleep(0.1)
                    k = conn.keys('*')

        self.f.close()


thread = parseLog(logfile)
thread.start()
