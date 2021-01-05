kubectl apply -f redis-deployment.yaml -n crawler
kubectl apply -f redis-service.yaml -n crawler
kubectl apply -f web-crawler-config.yaml -n crawler
kubectl apply -f web-crawler-deployment.yaml -n crawler
kubectl apply -f web-crawler-service.yaml -n crawler