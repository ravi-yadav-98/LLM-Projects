# Docker Commands for TokViz

## Build the Docker image
```bash
docker build -t tokviz .
```

## Run the container
```bash
docker run -p 5000:5000 tokviz
```

## Run with volume mount for persistent models
```bash
docker run -p 5000:5000 -v $(pwd)/models:/app/models tokviz
```

## Run in detached mode
```bash
docker run -d -p 5000:5000 --name tokviz-app tokviz
```

## View logs
```bash
docker logs tokviz-app
```

## Stop the container
```bash
docker stop tokviz-app
```

## Remove the container
```bash
docker rm tokviz-app
```

## Access the application
Open your browser and go to: http://localhost:5000
