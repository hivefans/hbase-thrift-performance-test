hbase-thrift-performance-test
=============================
10 concurrent threads write 60MB data to HBase

**Detail:**   
http://blog.thisisfeifan.com/2012/06/hbase-thrift-performance-test.html

connectioninthread.py, each thread own its private thrift connection   
sharedconnection.py, one shared thrift connection only.   

**My test result:**   
connectioninthread.py,   6.9139 seconds -> 60 000 records (60MB)   
sharedconnection.py, 16.345 seconds -> 60 000 records(60MB)   