
# Requirements

- Docker 

# How to start with Docker
- First start:
    - build `docker build --no-cache -t web_crawler .`
    - first start `docker run -p 80:1007 --name web_crawler web_crawler`
    - stop `docker stop web_crawler`

- Rebuild and start again:
    - stop container `docker stop web_crawler` 
    - remove container `docker rm web_crawler`
    - rebuild image `docker build --no-cache -t web_crawler .`
    - start container `docker run -p 80:1007 --name web_crawler web_crawler`
    
- Start again using the script:
    - run `./docker-build-start`