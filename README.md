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