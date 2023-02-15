## Deploy Deep learning model with TensorFlow Serving on Kubernetes(GKE)

The model will be deployed using Flask, TensorFlow Serving and Kubernetes(GKE). Flask was used to create a web service, while TensorFlow Serving was used to serve the model as a API.

## Files
* `Pipfile` and `Pipfile.lock` : library requirement for deployment
* `tf-serving-connect.ipynb` : Notebook file to test TF Serving connection
* `save_model.py` : Python script to download and convert the model
* `gateway.py` : python script for serving ML models using Flask
* `proto.py` : python script for convert np tp protobuf
* `test.py` : python script to send a request to the API
* `image-gateway.dockerfile` : Docker file build service container
* `image-model.dockerfile` : Docker file to build model server container
* `kube-config` : Contain yaml file that define deployment and service for this project

## Prerequisites
Before deploying our model, wee need to install these tools:
* Docker, Docker desktop instalation instruction [here](https://docs.docker.com/desktop/install/windows-install/)
* kubectl: the Kubernetes command-line tool, Docker desktop comes with kubectl already.
* GCP account
* Google Cloud CLI: set of tools to create and manage Google Cloud resources. [link](https://cloud.google.com/sdk/docs/install-sdk)

## How to Run

1. Download and save model
    Run `save_model.py` to save model so it can be serve using tensorflow serving.

2. Build docker image for service and model server

    Docker image model server
    ```bash
    docker build -t zoomcamp-10-model:xception-v4-001 \
        -f image-model.dockerfile .
    ```
    Docker image service
    ```bash
    docker build -t zoomcamp-10-gateway:001 \
        -f image-gateway.dockerfile .
    ```

3. Setup gcloud cli
    Authorize gcloud to access the Cloud Platform using your GCP account
    ```bash
    gcloud auth login
    ```
    Set your project
    ```bash
    export PROJECT_ID=de-zoomcamp-376104
    gcloud config set project $PROJECT_ID
    ```

4. Create Artifact registry repository to store docker image
    
    ```bash
    gcloud artifacts repositories create ml-zoomcamp \
        --repository-format=docker \
        --location=us-west1 \
        --description="ML Zoomcamp Docker repository"
    ```
    If can't create using cli, create on console.

5. Push docker image to Artifact registry
    Before push image, Tag the local image with the repository name, following this format.

    ```bash
    docker tag SOURCE-IMAGE LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG
    ```
    example:
    ```bash
    docker tag zoomcamp-10-model:xception-v4-001 us-west1-docker.pkg.dev/${PROJECT_ID}/ml-zoomcamp/zoomcamp-10-model:xception-v4-001
    ```

    Setup the credential helper configuration for authentication
    ```bash
    gcloud auth configure-docker \
        us-west1-docker.pkg.dev
    ```

    Push the image to Artifact registry
    ```bash
    docker push us-west1-docker.pkg.dev/${PROJECT_ID}/ml-zoomcamp/zoomcamp-10-model:xception-v4-001
    ```

6. Create GKE cluster
    Set compute engine region
    ```bash
    gcloud config set compute/region us-west1
    ```

    Create a cluster named `ml-zoom-cluster`
    ```bash
    gcloud container clusters create-auto ml-zoom-cluster
    ```
    Note: Existing versions of kubectl and custom Kubernetes clients contain provider-specific code to manage authentication between the client and Google Kubernetes Engine. Starting with v1.26, this code will no longer be included as part of the OSS kubectl. GKE users will need to download and use a separate authentication plugin to generate GKE-specific tokens. More information [link](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke)

    `gke-gcloud-auth-plugin` is needed for continued use of kubectl. follow the instruction [link](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke)
    
    Connect to your GKE cluster
    `gcloud container clusters get-credentials CLUSTER_NAME --region REGION`
    ```bash
    gcloud container clusters get-credentials ml-zoom-cluster --region us-west1
    ```
7. Create deployment and service of model and gateway.
    ```bash
    kubectl apply -f ./kube-config/model-deployment.yaml
    kubectl apply -f ./kube-config/model-service.yaml
    kubectl apply -f ./kube-config/gateway-deployment.yaml
    kubectl apply -f ./kube-config/gateway-service.yaml
    ```
    check the services.
    ```bash
    $ kubectl get svc
    W0215 18:49:03.702745    2636 gcp.go:120] WARNING: the gcp auth plugin is deprecated in v1.22+, unavailable in v1.25+; use gcloud instead.
    To learn more, consult https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
    NAME                        TYPE           CLUSTER-IP   EXTERNAL-IP      PORT(S)        AGE
    gateway                     LoadBalancer   10.6.2.33    104.199.121.64   80:31228/TCP   2m18s
    kubernetes                  ClusterIP      10.6.0.1     <none>           443/TCP        21m
    tf-serving-clothing-model   ClusterIP      10.6.3.181   <none>           8500/TCP       10m
    ```

8. Test the API
    Use the API by sending a POST request to the EXTERNAL-IP of gateway with the input image in the request body. you can simply run `test.py` file.





