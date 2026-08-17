#!/bin/bash

kubectl apply -f k8s/service.yaml 
source .env && sed "s|__PRODUCTION_APP_URL__|${PRODUCTION_APP_URL}|" k8s/deployment.yaml | kubectl apply -f -
