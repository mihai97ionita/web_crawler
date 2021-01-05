
# Requirements

- Docker
- Docker Account
- Image Registry ( Docker Hub repository )
- Minikube 
- Kubectl
- Bash

#First of all

- In `docker-build-push.sh` file there is a path for each image, change it for your registry
- For each `*-deployment.yaml` there will be that image used

# Configure your microservice: 
Your microservice needs to use this enviorment variables:
- `REDIS_CACHE_HOST` <- k8s config will point your microservice to the right host
- `REDIS_CACHE_PORT` 
- `REDIS_CACHE_PASS`


# How to start

- start minikube cluster: `minikube start`
- run `./k8s-docker-auth.sh`, login in docker if promoted <- this is required only once
- create Namespace `kubectl create -f ./namespace.yaml` <- only once
- run `./docker-build-push.sh`, it will build your microservice and push it in your docker registry <- every time you make a change
- run `./k8s-apply-all.sh` < will apply all changes 
- run `minikube service web-crawler -n crawler` to get your application ip :D
