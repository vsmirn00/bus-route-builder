echo "Starting Minikube..."
minikube start 

echo "Building Docker image..."
docker build -t vsmirn/fastapi-app:01 .

echo "Pushing Docker image to Docker Hub..."
docker push vsmirn/fastapi-app:01

echo "Applying Kubernetes Deployment..."
kubectl apply -f kubernetes/deployment.yaml

echo "Applying Kubernetes Service..."
kubectl apply -f kubernetes/service.yaml

echo "Waiting 10 minutes for the service to be ready..."
sleep 600

echo "Accessing the Minikube Service..."
minikube service fast-api-service
