# DockerHub Prometheus Exporter

This Python application is a Prometheus exporter that collects metrics from a specified DockerHub organization and exposes them for Prometheus to scrape. It uses the DockerHub API to retrieve the number of pulls for each public Docker image in the organization.

## Features

- Fetches the number of pulls for Docker images in a specified DockerHub organization.
- Exposes the metrics in Prometheus format.
- Runs a simple HTTP server to serve the metrics.

## Requirements

- Python 3.12 or newer
- Docker 25.0.0
- Kubernetes (kubectl 1.29, kind 0.21.0)

## Installation

### Clone the repository and access application directory
```sh
git clone <repository-url>
cd <repository-directory>/app-python/
```

### Local Development

1. **Set up a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set environment variables**:
    ```sh
    export DOCKERHUB_ORGANIZATION=<your-dockerhub-organization>
    export APP_PORT=2113
    ```

4. **Run the application**:
    ```sh
    python src/main.py
    ```




5. **Access the metrics**:
    Open your browser or use `curl` to access [http://localhost:2113/metrics](http://localhost:2113/metrics).
    ```sh
    curl http://localhost:2113/metrics
    ```

### Docker

1. **Build the Docker image**:
    ```sh
    docker build -t local.registry/test-app:1.0.0 .
    ```

2. **Run the Docker container**:
    ```sh
    docker run -d -p 2113:2113 -e DOCKERHUB_ORGANIZATION=<your-dockerhub-organization> local.registry/test-app:1.0.0
    ```

3. **Access the metrics**:
    Open your browser or use `curl` to access [http://localhost:2113/metrics](http://localhost:2113/metrics).
    ```sh
    curl http://localhost:2113/metrics
    ```

### Kubernetes

1. **Create a kind cluster**:
    ```sh
    kind create cluster --name exporter-cluster
    ```

2. **Build and push the Docker image to a kind cluster**:
    ```sh
    docker build -t local.registry/test-app:1.0.0 .
    kind load docker-image "local.registry/test-app:1.0.0" --name exporter-cluster
    ```

3. **Apply the Kubernetes manifests**:
    ```sh
    kubectl apply -f ../k8s-resources/app.yml
    ```

4. **Port forward to access the service**:
    ```sh
    kubectl port-forward svc/test-app 2113:2113
    ```

7. **Access the metrics**:
    Open your browser or use `curl` to access [http://localhost:2113/metrics](http://localhost:2113/metrics).
    ```sh
    curl http://localhost:2113/metrics
    ```

## Configuration

### Environment Variables

- `DOCKERHUB_ORGANIZATION`: The name of the DockerHub organization. Example: `test`
- `APP_PORT`: The port on which the HTTP server will run. Default is `2113`.

