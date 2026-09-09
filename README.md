# docker

## 1.runing flask_server

```bash
docker built -t 'image name' 'dockerfile path'
docker built -t flask_server .

docker run -it -d -p host_port:docker_port 'image name'
docker run -it -d -p 8000:8000 flask_server
```
## 2.volumes
## docker volumes store in /var/lib/docker/volume
```bash
docker volume create <volume name>
docker run -it -d --name <container name> -v <volume name>:<where this volume will mount in container> <img name>
``` 

