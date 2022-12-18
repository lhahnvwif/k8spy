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


---


## 2. For Kubernetes
Here this is just testing with minikube!!!!
(Adjust the imagePullPolicy to Never when using Minikube)

This will create a cluster with 5 nodes and 10 replica pods;
On average(!) 2 pods per node, but does not have to be!

0. $ minikube start --nodes=5

1. $ minikube nodes list

2. $ minikube image load flaskapp

3. $ minikube kubectl -- apply -f deployment.yaml -f service.yaml

4. $ minikube kubectl -- get pods

5. $ minikube kubectl -- get pods -o json

6. $ minikube service list -> open URL in Browser and have fun! :)

7. $ minikube delete