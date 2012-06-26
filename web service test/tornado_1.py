# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web

import json, traceback, sys, datetime, time, logging, random


import thrift
sys.path.append('gen-py')


from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase



transport = TBufferedTransport(TSocket('10.1.2.230', 9090), 40960)
transport.open()
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Hbase.Client(protocol)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<br>".join(client.getTableNames()))
        
class Save2HBase(tornado.web.RequestHandler):
    def post(self):
        try:
            jsonmsg = json.loads(self.request.body);                         
            batchmutations = []            
            for ts,reports in jsonmsg.items():
                mutations = [] #multi-op together        
                rowKey = "RK__%s__%s" % (random.random(), ts)
                for k,v in reports.items():
                    mutations.append(Hbase.Mutation(column="f1:%s"%k, value=v))               
                
                if len(mutations) != 0:
                    batchmutations.append(Hbase.BatchMutation(rowKey, mutations))
            
            if len(batchmutations) != 0:
                client.mutateRows("testdb2", batchmutations)            
                pass
        except Exception as e:
            traceback.print_exc()
            self.write("error %s" % str(e))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/savemsg/", Save2HBase),
])

if __name__ == "__main__":
    application.listen(sys.argv[1])
    tornado.ioloop.IOLoop.instance().start()
