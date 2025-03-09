echo "Starting Minikube..."
minikube start 

echo "Building Docker image..."
docker build -t vsmirn/fastapi-app:01 .

echo "Pushing Docker image to Docker Hub..."
docker push vsmirn/fastapi-app:01

echo "Applying Kubernetes Deployment..."
kubectl apply -f deployment/deployment.yaml

echo "Applying Kubernetes Service..."
kubectl apply -f deployment/service.yaml

echo "Waiting 5 minutes for the service to be ready..."
sleep 300

echo "Accessing the Minikube Service..."
minikube service fast-api-service
