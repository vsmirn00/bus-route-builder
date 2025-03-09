# Run locally on reload

uvicorn app.main:app --reload

---




# Request

{
  "name": "viladecans",
  "input_path": "data/equipaments_model_2.csv",
  "output_path": "output_folder/",
  "num_stations": 0,
  "num_routes": 0,
  "central_station": true,
  "balance_stations": true
}






























# Request in fastapi

{
  "name": "Viladecans",
  "num_stops": 13,
  "path": "data/russia_cities.geojson"
}


---

# Docker commands

docker-compose build
docker-compose up --build

---


### Kubernetes (CLI workflow)

minikube start

docker build -t vsmirn/fastapi-app:01 .

docker push vsmirn/fastapi-app:01

kubectl apply -f kubernetes/deployment.yaml

kubectl apply -f kubernetes/service.yaml

minikube service fast-api-service


### sh file

chmod +x scripts/script.sh
bash scripts/script.sh



### Kubernetes (No longer relevant)

minikube start --extra-config=apiserver.authorization-mode=RBA

# minikube start --memory=4096 --cpus=2 --addons=default-storageclass --addons=storage-provisioner 
# docker build -t vsmirn/fastapi-app:01 .
# minikube image load logistics/fastapi-app:01

kubectl create secret docker-registry regcred \
    --docker-server=https://index.docker.io/v1/ \
    --docker-username=<your-docker-username> \
    --docker-password=<your-docker-password> \
    --docker-email=<your-email>


