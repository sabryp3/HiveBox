# HiveBox
HiveBox
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/sabryp3/HiveBox/badge)](https://scorecard.dev/viewer/?uri=github.com/sabryp3/HiveBox)
Overview
HiveBox is a FastAPI-based application designed to monitor and aggregate the temperature readings from three specified sensors. It provides API endpoints to retrieve sensor temperatures, calculate the average, store the result in a Minio bucket, check sensor readiness, and report the application version. The app uses Redis for caching and is built for deployment on AWS EKS, leveraging Kubernetes manifests and a Dockerized workflow. CI/CD automation and security are integrated through GitHub Actions.

