# docker
first docker project

```bash
docker built -t 'image name' 'dockerfile path'
docker built -t flask_server .

docker run -it -d -p host_port:docker_port 'image name'
docker run -it -d -p 8000:8000 flask_server

