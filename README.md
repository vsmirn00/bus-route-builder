# 🚍 Bus Route Optimization Service

## 📌 Introduction

This project **automates the creation of optimized bus routes** for any city. It serves as a **heuristic-based solution** that finds the **best possible K routes for a given number of N stations**, using a **Hierarchical Clustering Algorithm**.

The application includes the following key features:
- **Automated Route Generation** – Finds the best K routes based on city infrastructure.
- **Central Bus Station Integration** – Optionally generates a **central hub** for bus routes.
- **Balanced Route Optimization** – Ensures an **even distribution of bus stops per route**.
- **Flexible Input Handling** – Users can specify parameters **or let the app optimize automatically**.
- **Multiple Deployment Options** – Supports **FastAPI**, **Docker**, and **Kubernetes** deployment.
- **Interactive Route Visualization** – Generates an **interactive map** with **route visualizations**.

For demonstration purposes, the input data is **preprocessed and stored** in a CSV file (`equipaments_model_2.csv`). Future iterations will include an endpoint for **direct file uploads**.

The **app execution takes approximately 8 minutes** and saves a **screenshot of the generated routes** while returning a **JSON response** detailing route characteristics.

Deployment options include:
- **FastAPI** – Quickest and easiest way to test the app locally.
- **Docker** – Containerized deployment for a **stable and reproducible environment**.
- **Kubernetes (K8s)** – For **scalable and production-ready service deployment**.

For automation, we provide a **`script.sh`** file that **builds and launches the service** with a single command.

---

## 📂 Repository Structure

```
bus-route-builder/
│── app/
│   ├── main.py           # FastAPI app entry point
│   ├── routes            # API endpoints
│   ├── factory           # Handles application execution
│   ├── context_manager   # Handles application's lifespan
│   ├── utils             # Helper functions
│   ├── models            # Has the Adapter model to handle the app logic
│   ├── http_model        # Stores the json schemas
│   ├── output_folder     # Stores the output maps
│   ├── src               # Handles the optimization logic
│   └── data/
│       ├── equipaments_model_2.csv  # Input dataset
│
│── deployment/
│   ├── deployment.yaml      # Kubernetes Deployment config
│   ├── service.yaml         # Kubernetes Service config
│
│── scripts/
│   ├── script.sh            # Automates deployment process
│
│── Dockerfile               # Docker container setup
│── docker-compose.yml        # Docker Compose configuration
│── requirements.txt          # Python dependencies
│── README.md                # Documentation
```

---

## 🛠 Dependencies & Installation

This project uses **Poetry** for dependency management. It is recommended to:
1. **Install Poetry** → [Installation Guide](https://python-poetry.org/docs/)
2. **Create a Virtual Environment**
3. **Ensure Docker & Kubernetes are installed** for containerized deployment.

**Clone the repository and navigate to the project directory:**
```sh
git clone https://github.com/vsmirn00/bus-route-builder.git
cd bus-route-builder
```

**Install dependencies using Poetry:**
```sh
poetry install
```

---

## 🚀 How to Run the Application

### 1️⃣ Running with FastAPI (Local Development)
The easiest way to test the app locally:
```sh
fastapi dev
```
Then open **http://127.0.0.1:8000/docs** to test the API.

---

### 2️⃣ Running with Docker
To run the app inside a Docker container:
```sh
docker-compose build
docker-compose up --build
```
This ensures a **stable and portable environment**.

---

### 3️⃣ Running on Kubernetes
To deploy the service on **Minikube**, update the **Docker username** and run:
```sh
minikube start

docker build -t username/fastapi-app:01 .
docker push username/fastapi-app:01

kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service.yaml

minikube service fast-api-service
```
This simulates **real-world cloud deployment**.

---

### 4️⃣ Automating Deployment with the Bash Script
For full automation, use the provided **`script.sh`**:
```sh
chmod +x scripts/script.sh
bash scripts/script.sh
```
This script **builds, deploys, and launches the service** in a single step.

---

## 📡 API Usage

### 📥 JSON Request Format
#### 🔹 FastAPI Request
```json
{
  "name": "viladecans",
  "input_path": "data/equipaments_model_2.csv",
  "output_path": "output_folder/",
  "num_stations": 0,
  "num_routes": 0,
  "central_station": true,
  "balance_stations": true
}
```
#### 🔹 Request for Docker/Kubernetes Deployment
```json
{
  "name": "viladecans",
  "input_path": "app/data/equipaments_model_2.csv",
  "output_path": "output_folder/",
  "num_stations": 0,
  "num_routes": 0,
  "central_station": true,
  "balance_stations": true
}
```

---

### 📤 Expected API Response
```json
{
  "name": "viladecans",
  "input_path": "data/equipaments_model.csv",
  "output_path": "output_folder/image.jpg",
  "num_stations": 30,
  "num_routes": 3,
  "central_station": true,
  "balanced_num_stops": true,
  "results": [
    {
      "route_id": 2,
      "route_num_stations": 3,
      "distance": 10.23
    }
  ]
}
```
✔ The API **returns a JSON response** summarizing the computed routes.  
✔ A **map screenshot** is saved in the output folder.  

---

## 📍 Interactive Map
The `/map` endpoint generates an **interactive folium map** showing all bus routes.

After starting the app, visit:
```
http://127.0.0.1:8000/map
```
This helps visualize **the optimized routes in real-time**.

---

## 🌍 Future Improvements
- **Automated File Uploads** – Replace CSV input with dynamic file uploads.
- **Real-Time Route Optimization** – Improve algorithm efficiency for large cities.
- **Cloud Deployment (AWS/GCP)** – Scale the service for production use.
- **Parallelize application logic** – Parallelize every possible step.

---

## 📜 License
This project is licensed under the **MIT License** – feel free to use and modify it.

---

## 🙌 Contributors
🚀 **Developed by:**
- **Vladimir Smirnov** – AI Engineer & Data Scientist

