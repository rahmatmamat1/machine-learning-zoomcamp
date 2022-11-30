## Deploy Deep Learning Model on Cloud Functions
Google Cloud Functions is a serverless cloud computing solution for creating, managing, and deploying applications. Designed to run your code in the cloud without having to manage containers or servers.

## Files
* `main.py`: python script for cloud functions.
* `requirements.txt`: library requirements for this service.
* `tensorflow_model_convert.ipynb`: notebook file to convert keras model to TF Lite.
* `test.py`: python script for testing cloud functions.

## Steps
1. Prepare Machine Learning/Deep Learning Model.
I used pre-trained Deep Learning model for this project. run `tensorflow_model_convert.ipynb` to download and convert pre-trained model into TF Lile format.

2. Upload Model to Cloud Storage
Open Google cloud storage and upload your model. for example I created bucket to store my deep learning models.

    ![](img/01_create%20bucket.PNG)
    ![](img/02_upload%20model.PNG)

3. Create Cloud Function
You can search and go to Cloud Functions. click on create and give a name for the function, make sure it's in the same region as the model storage bucket. Select the function trigger type to be HTTP.

    ![](img/03_create%20cloud%20functions.PNG)

    set authentication to allow unauthenticated invocations and click save and next.

4. Script for Cloud Function
Once you click next, define runtime environtment for this script, in this case I use python 3.9.

    ![](img/04_script%20for%20cloud%20function.PNG)

    as you can see there is 2 file that we must provide.

        * `main.py`: main file which contains the function to be executed when there is a trigger event.
        * `requirements.txt`: library requirements we need on order to run the script.

    you can copy and paste content in `main.py` and `requirements.txt` in this repo into cloud function editor. Inside `main.py` file we download tf lite model from cloud storage bucket that we created earlier and predict function is the main entry point function which responds to the HTTP request.

5. Deploy Cloud Fuctions
Once source code updated, Click deploy. cloud function will automatically build container aand install libraries from requirements file. this can take some time, Once the setup is complete and the function is deployed successfully, a green tick mark will appear next to the function name.

    ![](img/05_cloud%20function%20setup%20completed.PNG)

6. Testing serverless prediction service
you can now test you service by clicking the function name and open testing tab. you can send JSON request like

    ![](img/06_testing%20service.PNG)

    then click test the function to see the results.

    ![](img/07_request%20results.PNG)

    or you can just run `test.py` to send request to your function.