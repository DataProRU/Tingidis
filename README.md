## 1. build docker image
```
docker build -t web-app .  
```
## 2) run docker image
```
docker run -d -p 8000:8000 web-app 
```
## 3) run docker image with reload

```
docker run -v $(pwd):/app -p 8000:8000 web-app uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Note:
all routers
http://127.0.0.1:8000/docs