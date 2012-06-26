# -*- coding:utf-8 -*-
import json, urllib2, httplib, sys, random, time, threading


recordsPerBatch = 300 #reports per client per day
columns = 3

concurrent = 10
records = 6000000 #6000000 #6 million
bytesPerRecord = 1024

gWritenItems = 0
gStartT = 0
gEndT = 0


url = "http://10.1.2.78:8880/savemsg/"

mylock = threading.RLock()
class writeThread(threading.Thread):
    def __init__(self, threadname, RecordsThreadwillwrite):
        threading.Thread.__init__(self, name = threadname)
        self.tbwBatch = int (RecordsThreadwillwrite / recordsPerBatch)
        
    def run(self):
        global gEndT
        global gWritenItems
        
        threadWritenItem = 0
        for loopidx in xrange(self.tbwBatch):
            self.emu_post()
            threadWritenItem += recordsPerBatch
            
        mylock.acquire()
        gEndT = time.time()
        gWritenItems += threadWritenItem
        print "%s done, %s seconds past, %d reocrds saved" % (self.getName(), gEndT-gStartT, gWritenItems)
        mylock.release()
            
    def emu_post(self):
        jsonreq = {}
        for ii in xrange(recordsPerBatch):
            datapiece = {}
            bytesPerColumn = int(bytesPerRecord/columns) - 11 #suppose 3 columns    

            for i in xrange(columns):
                datapiece[i] = "value_" + "x"*bytesPerColumn + "_endv"
            jsonreq[time.time() + random.random()] = datapiece

        #print jsonreq        
        req = urllib2.Request(url, json.dumps(jsonreq))
        resp = urllib2.urlopen(req)
        #print resp.read()       
    

    
itemsPerThread = int(records / concurrent)
for threadid in xrange(0, concurrent):    
    gStartT = time.time()
    t = writeThread("Thread_%s" % threadid, itemsPerThread)
    t.start();
print "%d thread created, each thread will write %d records" % (concurrent, itemsPerThread)

