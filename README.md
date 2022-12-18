# K8sPy

A simple test how to get a py flask app run on kubernetes.


---


## 1. For Docker

### Instructions

1. docker build -t flaskapp .

2. docker images -a

3. docker run -d -p 80:8000 flaskapp

-> Open Browser: http://localhost

Endpoints:
  - /start-thread/<ID>
  - /start-thread
  - /stop-thread/<ID>
  - /stop-thread 
  - /content/<ID>
  - /content


