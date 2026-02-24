# Docker Project

## Files

-   `index.html` - Custom Nginx webpage
-   `task2/server.py` - Python TCP server
-   `task2/client.py` - Python TCP client
-   `task2/docker-compose.yml` - Multi-container configuration

## Task 1: Deploy a Web Server

``` sh
docker run -d -p 8080:80 --name my-nginx nginx:latest
```

Open:

``` sh
http://localhost:8080
```

Run:

``` sh
docker stop my-nginx
docker rm my-nginx

docker run -d -p 8080:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html --name my-nginx nginx:latest
```

## Task 2: Multi-Container Setup (Server + Clients)

``` sh
cd task2
docker compose up --build --scale client=3
```

Stop:

``` sh
docker compose down
```
