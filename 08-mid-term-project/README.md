# AdTracking Fraud Detection

## Problem
Fraud risk is everywhere, but for companies that advertise online, click fraud can happen at an overwhelming volume, resulting in misleading click data and wasted money. Ad channels can drive up costs by simply clicking on the ad at a large scale. With over 1 billion smart mobile devices in active use every month, China is the largest
mobile market in the world and therefore suffers from huge volumes of fradulent traffic.

[TalkingData](https://www.talkingdata.com/), China’s largest independent big data service platform, covers over 70% of active mobile devices nationwide. They handle 3 billion clicks per day, of which 90% are potentially fraudulent. Their current approach to prevent click fraud for app developers is to measure the journey of a user’s click across their portfolio, and flag IP addresses who produce lots of clicks, but never end up installing apps. With this information, they've built an IP blacklist and device blacklist.

In this project we were going to build an algorithm that predicts whether a user will download an app after clicking a mobile app ad.

## Dataset
The Dataset is a sample from the TalkingData AdTracking competition. the author kept all the positive examples (where is_attributed == 1), while discarding 99% of the negative samples. The sample has roughly 20% positive examples.

You can download the dataset [here](https://www.kaggle.com/datasets/matleonard/feature-engineering-data). I used `baseline_data.pqt` for this project.

Data fields:

Each row of the training data contains a click record, with the following features.

* `ip`: ip address of click.
* `app`: app id for marketing.
* `device: device type id of user mobile phone (e.g., iphone 6 plus, iphone 7, huawei mate 7, etc.)
* `os`: os version id of user mobile phone
* `channel`: channel id of mobile ad publisher
* `click_time`: timestamp of click (UTC)
* `attributed_time`: if user download the app for after clicking an ad, this is the time of the app download
* `is_attributed`: the target that is to be predicted, indicating the app was downloaded

**Note that ip, app, device, os, and channel are encoded.**

## Files
* `README.md`: Description and explanation of the project
* `AdTracking_Fraud_Detection.ipynb`: Notebook file contains EDA and Modeling
* `model_xgb.bin`: saved model for prediction
* `service.py`: python script for serving ML models using FastAPI
* `test_service.py`: python script to send a request to the API
* `requirements.txt`: library requirement for this project
* `Dockerfile`: to run service on container
* `.dockerignore`: ignore/exclude files and directories when building container
* `.gcloudignore`: ignore/exclude files and directories to prevent uploading it to google cloud

## Prerequisites
1. Docker - Install instruction: https://docs.docker.com/install
2. Google cloud CLI tool - Install instruction: https://cloud.google.com/sdk/docs/install

## Steps
1. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
2. Run the Fraud Detection service
    ```bash
    python service.py
    ```
    Open your web browser at http://localhost:9696 to view the Swagger UI for sending test requests.
    Or you can just run `test_service.py` to send request to the API.
    ```bash
    python test_service.py
    ```
3. Containerize the service using Docker

    Create `Dockerfile`
    ```docker
    FROM python:3.9-slim

    WORKDIR /app

    COPY ["requirements.txt", "./"]

    RUN pip install -r requirements.txt

    COPY ["model_xgb.bin", "service.py", "./"]

    EXPOSE 9696

    ENTRYPOINT [ "python", "service.py" ]
    ```

    Build Docker Image
    ```bash
    docker build -t fraud-service .
    ```
    
    Run Docker Image
    ```bash
    docker run -it -p 9696:9696 fraud-service:latest
    ```
    Now the service is running inside the container. you can send request by running `test_service.py`
4. Deploy the service to google cloud run
    
    We need to build container on google cloud in order to deploy it to the cloud run

    Create `Dockerfile`
    ```docker
    FROM python:3.9-slim

    WORKDIR /app

    RUN pip install pipenv

    COPY ["requirements.txt", "./"]

    RUN pip install -r requirements.txt

    COPY ["model_xgb.bin", "service.py", "./"]

    RUN pip install gunicorn

    CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --worker-class uvicorn.workers.UvicornWorker --timeout 0 service:app
    ```
    Also create `.gcloudignore` to prevent uploading unnecessary file to the cloud.

    Before building container in cloud and deploy it, we need to activate Cloud Build API, Artifact Registry API, and Cloud Run API.
    
    Deploy from source code directory using the following command:
    ```bash
    gcloud run deploy
    ```
    Automatically builds a container image from source code and deploys it.
    
    * When you are prompted for the source code location, press Enter to deploy the current folder.
    * When you are prompted for the service name, press Enter to accept the default name, `helloworld`.
    * When you are prompted for region: select the region of your choice.
    * You will be prompted to allow unauthenticated invocations: respond `y`.

    Then wait few moments until the deployment is complete.
    
    For more information: [link](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
    ```
    $ gcloud run deploy
    Building using Dockerfile and deploying container to Cloud Run service [fraud-service] in project [project] region [us-west1]
    OK Building and deploying new service... Done.
    OK Uploading sources...
    OK Building Container... 
    OK Creating Revision... Deploying Revision.
    OK Routing traffic...
    OK Setting IAM Policy...
    Done.
    Service [fraud-service] revision [fraud-service-00001-bek] has been deployed and is serving 100 percent of traffic.
    Service URL: https://fraud-service-i2gw4npszq-uw.a.run.app
    ```
    
    This command is equivalent to running `gcloud builds submit --tag [IMAGE] D:\Rahmatsyah Firdaus\Data Project\mid-term-project` and `gcloud run deploy fraud-service --image [IMAGE]`

    you can visit Service URL to open Swagger UI or send a request.
    ```
    $ python test_service.py
    {'download_probability': 0.9966546297073364, 'download': True}
    ```

