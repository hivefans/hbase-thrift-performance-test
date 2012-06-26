hbase-thrift-performance-test
=============================
**Write to thrift directly**    
----------------------------
10 concurrent threads write 60MB data to HBase by thrift

**Detail:**   
http://blog.thisisfeifan.com/2012/06/hbase-thrift-performance-test.html

connectioninthread.py, each thread own its private thrift connection   
sharedconnection.py, one shared thrift connection only.   

**My test result:**   
connectioninthread.py,  60 000 records (60MB) -> 6.9139 seconds    
sharedconnection.py, 60 000 records(60MB) -> 16.345 seconds   


**Web service write to thrift**   
-------------------------------
under folder "web service test"   
including nginx setting, supervisord setting and both web side tornado application code and test-driven code   

**Detail:**   
http://blog.thisisfeifan.com/2012/06/hbase-thrift-performance-test-2.html   

emu_massdata.py, test-driven code, 10 concurrent threads send 300K-length data to web server continually   
tornado_1.py, web side application, writen in tornado   

**My test result:**   
60 000 records (60MB) -> 6.22 seconds   
6 000 000 records (6GB) -> 768.79 seconds