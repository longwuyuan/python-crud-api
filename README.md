# CI/CD - High Level Architecture

![ci-cd-high-lvel-architecture](https://user-images.githubusercontent.com/5085914/142748681-65e2ff9c-85f1-4489-9385-5b0de8e8da35.png)

# Microservices - 12factor Visualized (taken from 12factor.net)

![12factor](https://user-images.githubusercontent.com/5085914/142748772-3ee07fab-0396-4c4f-84a8-9c5551d39081.png)


# PYTHON CRUD API

A CI/CD pipeline, for 4 api endpoints, written in flask, that generates yaml files (kubectl Kustomize), for installation on Kubernetes


## INTRODUCTION

* This is a tiny app. Its basically about names & details of passengers on a flight

* This app implements CRUD (create, update, delete)

* The CRUD functions are availale as 4 api(s)

* Language used is Python and framework is flask

* Other Python modules used are flask_uuid and psycopg2

* The WSGI server used is gunicorn

* A Nginx instance is running in reverseproxy mode for the api microservice

* The app works on kubernetes or in docker-compose

* The api microservice needs to be exposed to clients outside the k8s cluster

* API uses a postgresql instance

* There is a K8s manifest in the /install directory that can be used as `kubectl apply -f`, for deploying the app to K8s

* There are 2 docker images. One for the postgres microservice and another for the api microservice

* There are microservice specific readme files, in the respective src sub-folder

* The app is a single file of python code, instead of multiple files as per MVC

* Nginx in reverseproxy mode, and the WSGI server "gunicorn" (in python crud api microservice), are started by Supervisord


## REQUIREMENTS

- A functional healthy kubernetes cluster is required to run the app. Tested on minikube, kind, GKE & EKS clusters
- For the CI pipeline, a Github Token called GCHR_PAT, with repo & package read/write permissions is needed. Creating a token is documented here https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry .

## INSTALLATION

There are multiple ways to install the app

  1. kubectl apply -f https://github.com/longwuyuan/python-crud-api/blob/524e85b528ec0c74e6d12955226a4b6b6e16b6c1/install/pycrudapi.yaml

  2. If the code is downloaded locally, then just `kubectl apply -f <path_to_approot>/install/pycrudapi.yaml`

  3. If you want to use docker-compose (not recommended) then use the docker-compose file at __(path_to_your_git_clone_root_folder_of_this_project)__/src/docker-compose.yml

        ```
        cd <gitroot>/src/
        docker-compose build
        docker-compose up
        ```

## API ENDPOINTS Exposed

Endpoint                    |       Request Header              |       Request Body
----------------------------|-----------------------------------|-------------------
/hello                      | Content-Type: application/json    |
/zero                       | Content-Type: application/json    |
/passengerlist              | Content-Type: application/json    |
/getpassenger/\<uuid\>      | Content-Type: application/json    |
/postpassenger              | Content-Type: application/json              | {"survived":true,"passengerClass":2,"name":"Post-Test-Name","sex":"male","age":27.0,"siblingsOrSpousesAboard":0,"parentsOrChildrenAboard":0,"fare":13.0}       |
/putpassenger/\<uuid\>      | Content-Type: application/json    | {"survived":false,"passengerClass":2,"name":"Put-Test-Name","sex":"male","age":27.0,"siblingsOrSpousesAboard":0,"parentsOrChildrenAboard":0,"fare":13.0}
/deletepassenger/\<uuid\>    | Content-Type: application/json    |

## Networking

- Make sure your Kubernetes cluster can provision a LoadBalancer from your cloud-provider. If your cluster is created using minikube, K3s, Kind or Kubeadm (on-premises or cloud) and does not have a provisioner for creating a LoadBalancer, then install Metallb https://metallb.org/installation/ .

- Install a ingress-controller on your cluster like https://kubernetes.github.io/ingress-nginx/ . You can then create a ingress object to expose the app. A sample of the ingress object's yaml, looks like this. Change the host value to suit your needs. I had a cert for my domain so I used it. You can use with/without TLS. Some people may choose to not even use a LoadBalancer service for the ingress-controller and they may just use a service of type NodePort for the ingress-controller. That discussion is out of scope here but his is just a hint/note on networking ;
  ```
  kind: Ingress
  metadata:
    name: pycrudapi
    namespace: python-crud-api
  spec:
    ingressClassName: nginx
    rules:
    - host: pycrudapi.dev.yourdomain.com
      http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: pycrudapi
              port:
                number: 80
  ```

- Use port-forwarding https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/ 

## CI/CD Pipeline

- For the pycrudapi microservice

```
        git commit
            |
if /src/pycrudapi changed then build image
            |
     push image to gcr.io
            |
run kubectl kustomize to change tag
            |
  publish new yaml at /install
```

- For the postgres0 microservice, the change will be rare and hardly ever needed. But if required, make the change and pipeline will build new image for postgres0 microservice and push to gcr. Then we manually change the /src/kubernetes/base/deploy.postgres0.yaml to reflect the new tag. TODO - automate this but low priority. 



## TROUBLESHOOTING TIPS

* Create an issue.

* You can check the portnumber of your minikube/k8s NodePort, on which the api service can be reached

        ```
        kubectl -n python-crud-api get svc | grep api
        ```

* If you have packet-filtering or other kind of firewall, then make sure that the port reported by above command is open.

* Healthcheck curl command ;

        ```
        curl `minikube ip`:`kubectl -n python-crud-api get service pycrudapi --output='jsonpath={.spec.ports[0].nodePort}'`
        ```

## TODO - Fix db connection pool code (pool not closed now)

## TODO : Write Test cases for CI

* Good to have but not minimalist so need to balance it. In any case the test stage is part of the pipeline so will work on creating tests.

## TODO : Several changes to make it simpler & more efficient

## REFERENCES

* <http://www.postgresqltutorial.com/postgresql-uuid/>
* <https://stackoverflow.com/questions/46433459/postgres-select-where-the-where-is-uuid-or-string>
* <http://initd.org/psycopg/docs/sql.html#module-psycopg2.sql>
* <http://initd.org/psycopg/docs/extras.html>
* many more
