TARGET_REGISTRY="mihai97ionita/web-crawler"

## build docker image for web_crawler_image
docker build -t ${TARGET_REGISTRY}:python_crawler_base ./python_base/

## build docker image for web_crawler_image
docker build --no-cache -t ${TARGET_REGISTRY}:web_crawler_image ..

## build docker image for redis_crawler_cache
docker build --no-cache -t ${TARGET_REGISTRY}:redis_crawler_cache ./redis/

## push image to registry web_crawler_image
docker push ${TARGET_REGISTRY}:web_crawler_image

## push image to registry redis_crawler_cache
docker push ${TARGET_REGISTRY}:redis_crawler_cache