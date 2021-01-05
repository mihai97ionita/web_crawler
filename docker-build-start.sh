docker stop web_crawler
docker rm web_crawler
docker build --no-cache -t web_crawler .
docker run -p 80:1007 --name web_crawler web_crawler