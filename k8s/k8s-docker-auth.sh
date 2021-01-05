docker login
cat ~/.docker/config.json >> docker-config.json
kubectl create secret generic regcred --from-file=.dockerconfigjson="docker-config.json" --type=kubernetes.io/dockerconfigjson
rm docker-config.json

## the proper alternative is to create a Secret manifest with data: .dockerconfigjson: ${DOCKER_AUTH_BASE64_ENCODED}