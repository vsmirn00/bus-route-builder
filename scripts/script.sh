#!/bin/bash

# Start Minikube 
echo "Starting Minikube..."
minikube start 

# Build the Docker image
echo "Building Docker image..."
docker build -t vsmirn/fastapi-app:01 .

# Push the Docker image to Docker Hub
echo "Pushing Docker image to Docker Hub..."
docker push vsmirn/fastapi-app:01

# Apply the Kubernetes Deployment
echo "Applying Kubernetes Deployment..."
kubectl apply -f kubernetes/deployment.yaml

# Apply the Kubernetes Service
echo "Applying Kubernetes Service..."
kubectl apply -f kubernetes/service.yaml

# Wait for 10 minutes
echo "Waiting 10 minutes for the service to be ready..."
sleep 600

# Access the Minikube Service
echo "Accessing the Minikube Service..."
minikube service fast-api-service
