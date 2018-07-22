# surveys

A minimal implementation of a survey API in Python. 

## Surveys API

The code for the project is in the `surveys` module. It uses `Flask` for handling requests to the API, `mongodb` for the database, and `mongoengine` to provide an ODM to `mongodb`.

The endpoints and associated logic for the API are found in `suveys/app.py`. This creates a minimal Flask app with routes for surveys and survey responses. The `GET` and `POST` methods for the surveys endpoint is split into two functions. These functions could be combined into a single function, however keeping them separated makes them easier to read and minimises the complexity of the functions.   

The `surveys/db/models.py` contains the data models for surveys and survey responses. I used `mongoengine` as an ODM that maps the Python classes to fields in the `mongodb` documents. This was used instead of `pymongo` as `mongoengine` provides features like validation and makes the definition of the documents clearer and more consistent. 

The `SurveyResponse` model is an `EmbeddedDocument` that is embedded in the `Survey` model. Most of the time that a survey is queried the person requesting it is also interested with the survey responses. By embedding the `SurveyResponses` document inside of `Survey` this reduces the time it takes for the DB to return the data as no additional joins are required between the documents.

The last two main parts of the application are the `survey.py` and  `survey_response.py` files. These files provide functions for creating and querying surveys and survey responses. The code in these files could have been combined with the `SurveyResponses` and `Survey` classes. I chose to keep them separate as it decouples the api code from the db code. By decoupling in this way I can change out the DB engine or library without needing to change code in the `app.py`. I could also replace the library that manages requests without needing to change the code in the db layer.

I included validation survey responses to check that the maximum number of survey responses for a single was not exceeded and to stop the same user competing the same survey twice. I did not include data type validation for surveys. For a production API it's helpful to wrap Python exceptions caused by validation or incorrect data types with more human friendly error messages. This helps people using the API understand why their requests are incorrect.

For the application, I wrote tests for the `survey.py` and `survey_response.py` files. These tests can be found in the `tests` directory. I used the `mongomock` library to mock out the interactions with the database. This ensure that the tests do not accidentally interact with production data. It also keeps them isolated from other data that exists in the database so that they are deterministic.

Usually I would write automated API tests for `app.py`, however I did not due to time. I tested the API manually, which is fine given the complexity of the system. However, if the complexity of the system increased, automated API tests would save time by removing the need to do manual regression tests against the API.

I did not include a user document. In a production system this would be essential to validate that the user exists when they create a survey or complete a survey response. Users could also be managed by a separate service. 

The hostname of the `mongodb` database is hardcoded in the `surveys/db/mongo_connection.py` file. This is OK when working with a single environment, however when working with multiple environments it should be replaced with an environment variable or a `settings.py` file.

## Kubernetes

The Kubernetes configuration creates a pod and service for both the database and the API. The pods contain the running components of the application. The services allow other pods to interact with the pod by providing a constant host name. The service for the API enables it to be accessed from outside the cluster. 

The pod for `mongodb` uses the official image. I did not set up persistent storage for the pod, which means if the pod is restarted all data in the database will be lost. For a production application this is a bad idea. I would setup a Kubernetes `StatefulSet`.

Kubernetes also provides liveness and status checks for containers. Kubernetes can restart containers that fail liveness checks and manage updates with zero perceived down-time with status checks. I did not implement either of these features in the application due to time.  

The Docker image for the Python application is uploaded to Docker hub. Ideally for local development and testing this should not be required and a local artifact repository should be used instead. However, I could not get this to work within the time limit.

## Running with Minikube

This section explains how to run the application with Minikube. The steps to 

To begin the Python code needs to be containerised as a Docker image. The image can be created with the following command:

```commandline
docker build -t craigargh/surveys .
```

When this command is run the application's code is copied into the image and the Python requirements are installed.

Next the docker image needs to pushed to an artifact repository so that Kubernetes can use it. To push it to the Docker Hub artifact repository you can use this command (this will probably not work as you won't have the correct permissions for this repository, a local repository can be used instead, however I did not have time to work out how to do this):

```commandline
docker push craigargh/surveys
```

After the Docker image is built and uploaded to the artifact repository, you can start the application on Minikube. 


The first step to deploying the application on Minikube is to start the `mongodb` pod and service:

```commandline
kubectl create -f kubernetes/mongo-pod.yml
kubectl create -f kubernetes/mongo-svc.yml
```

Next you need to start the surveys API pod and its service: 

```commandline
kubectl create -f kubernetes/surveys-pod.yml
kubectl create -f kubernetes/surveys-svc.yml
```

After these pods and services are deployed the application is running. You can now call the API.

To find the IP address and port of the API you need to do two things.

First you need to find the IP address of the Minikube cluster:

```commandline
minikube ip
```

The output should look something like this:

```commandline
192.168.100.112
```

Next you need to find out the port of the API service:

```commandline
kubectl get svc
```

The output should look something like this:

```commandline
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP        3d
mongo             ClusterIP   10.103.194.120   <none>        27017/TCP      2h
surveys-service   NodePort    10.103.66.61     <none>        80:31474/TCP   2h
```

The important part is the port of the `surveys-service`. In this case it is `31474`. 

With the IP address and port you can now call the API:

```commandline
curl 192.168.100.112:31474/surveys
```
