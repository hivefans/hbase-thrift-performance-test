

import json, traceback, sys, datetime, time, logging, threading, random
import logging.handlers

import thrift
sys.path.append('gen-py')


from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase



gWritenItems = 0
gStartT = 0
gEndT = 0

recordsPerBatch = 300 #reports per client per day
columns = 3

#config
concurrent = 10
records = 60000#6000000 #6 million
bytesPerRecord = 1024



mylock = threading.RLock()
class writeThread(threading.Thread):
    def __init__(self, threadname, RecordsThreadwillwrite):
        threading.Thread.__init__(self, name = threadname)
        bytesPerColumn = int(bytesPerRecord/columns) - 11 #suppose 3 columns

        self.columnvalue = "value_" + "x"*bytesPerColumn + "_endv"
        self.tbwBatch = int (RecordsThreadwillwrite / recordsPerBatch)
        
        self.transport = TBufferedTransport(TSocket('10.1.2.230', 9090), 40960)
        self.transport.open()
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        self.client = Hbase.Client(protocol)
                        
    def run(self):
        print "+%s start" % (self.getName())
        global gEndT
        global gWritenItems           
        
        threadWritenItem = 0
        for loopidx in xrange(0, self.tbwBatch):            
            self.write_hbase() #write                                           
            threadWritenItem += recordsPerBatch   
            
        mylock.acquire()
        gEndT = time.time()  
        gWritenItems += threadWritenItem
        print "%s done, %s seconds past, %d reocrds saved" % (self.getName(), gEndT-gStartT, gWritenItems)
        mylock.release()
        self.transport.close()
             
        
        
        
    def write_hbase(self): #write 50 rowkyes, and  3 column families in each rowkey
        print self.getName(), "Start write"
        batchmutations = []
        for i in xrange(0, recordsPerBatch): # write to db, 300 items together
            mutations = []
            rowkey = "RK_%s_%s" % (random.random(), time.time())       
            for ii in xrange(0, columns):
                mutations.append(Hbase.Mutation(column="f1:%s"%ii, value=self.columnvalue))
            batchmutations.append(Hbase.BatchMutation(rowkey, mutations))
        self.client.mutateRows("testdb1", batchmutations)        



itemsPerThread = int(records / concurrent)
for threadid in xrange(0, concurrent):    
    gStartT = time.time()
    t = writeThread("Thread_%s" % threadid, itemsPerThread)
    t.start();
print "%d thread created, each thread will write %d records" % (concurrent, itemsPerThread)



