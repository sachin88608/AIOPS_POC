To run the Docker --

1. To build the docker --> docker build -t my-api .
2. To run the docker on 5000 port --> docker run -d -p 5000:5000 my-api
3. Curl need to hit on postman -->

    curl --location 'http://localhost:5000/predict' \
--header 'Content-Type: application/json' \
--data '{
  "features": [
    [
      14.1, 20.3, 90.2, 600.0, 0.111, 0.12, 0.3, 0.1, 0.21, 0.062,
      0.3, 1.2, 2.3, 25.0, 0.02, 0.06, 0.07, 0.02, 0.03, 0.021,
      16.0, 25.0, 100.0, 800.0, 0.12, 0.31, 0.4, 0.15, 0.215, 0.07
    ]
  ]
}'



If any changes made in the code - then need to stop the container and then again need to run the container to make the changes available.

To get the docker container runnnig --> docker ps
To stop the container --> docker stop <container-id>
To start the container if you have container id --> docker start <container-id>
To Run the container **without OpenTelemeter** --> docker run -d -p 5000:5000 my-api

To capture the **logs in realtime** in different terminal--> 
docker logs -f <container-id> >> my_api.log

To run the **app using OpenTelemetry** -->
docker run -d -p 5000:5000 -e OTEL_SERVICE_NAME=breast-cancer-api -e OTEL_RESOURCE_ATTRIBUTES="deployment.environment=dev,service.version=1.0.0" -e OTEL_TRACES_EXPORTER=console -e OTEL_METRICS_EXPORTER=none -e OTEL_LOGS_EXPORTER=none my-api

# Rebuild the Flask app image by running: 
docker compose build

# Start or restart the services with:- This will start all containers (Flask, Prometheus, Loki) using the latest images.
docker compose up

# During Loki installed on GCP then this command needs to run 
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

# To Stop all the containers - 
docker compose down

# To Build the container 
docker compose up --build

# Added cadvisor to Scrap the CPU, Memory Usage etc from the Promethesus

# Add Grafana for the Dashboard
To visualize *Prometheus* and *Loki* together



# <!-- Prometheus metrics -->
Open: http://localhost:9090​

Go to the “Graph” or “Expression” tab and type a metric name, for example:

flask_http_request_total

flask_http_request_duration_seconds_count

sum(rate(container_cpu_usage_seconds_total[1m]))

Hit Execute to see the current values or switch to the Graph view to see time‑series charts.


# Open GRAFANA
http://localhost:3000/login

# Open Promethesus
http://prometheus:9090

# Open Loki - Won't open from this 
http://loki:3100


Run **Docker stats** to get the CPU, Memory etc.. on CMD


4) Query in Prometheus
In http://localhost:9090 you will now see:

api_requests_total – per‑endpoint/method/status request counts.

api_request_latency_seconds_bucket / _count / _sum – histogram for latency.

prediction_errors_total – total failures.​

Example PromQL:

<!-- Requests per second: -->
rate(api_requests_total[1m])

<!-- p95 latency: -->
histogram_quantile(0.95, sum(rate(api_request_latency_seconds_bucket[5m])) by (le))

<!-- Error rate: -->
rate(prediction_errors_total[5m]).


<!-- Memory usage of each container (bytes): -->

text
container_memory_usage_bytes


<!-- cpu_usage_seconds_total -->
rate(container_cpu_usage_seconds_total[10m])

<!-- memory_usage_bytes -->

container_memory_usage_bytes


## Check the Promethesus Logs on UI - Promethesus Level Logs only
http://localhost:9090/metrics


## For Flask api logs - Application level logs (Used in promothesus UI) - Important for us
Open GIT BASH and run -->

curl http://localhost:5000/metrics


-- HOLD This POC for now..--

1. To run the docker and up the terminal - **docker compose up --build**
2. To stop the docker -- **docker compose down**
3. To check the flask api logs -- Open GIT BASH and run --> **curl http://localhost:5000/metrics**
4. To check Promethesus logs -- **http://localhost:9090/metrics**
5. Learn more about the PROMQL and the Loki Queries 
6. To open Grafana -- **http://localhost:3000/login**
7. To open Promethesus -- **http://prometheus:9090**
8. Use postman to hit the my-api-flask-app-1 (**Curl** is already present at the top)
9. To check the what all containers are running -- **docker ps**