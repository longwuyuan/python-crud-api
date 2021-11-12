# PYTHON CRUD API

## INTRODUCTION

* This is a tiny app.

* This app implements CRUD (create, update, delete)

* The CRUD functions are availale as a api.

* Language used is Python

* Python modules are flask, flask_uuid and psycopg2.

* The WSGI server used is gunicorn.

* Nginx is running in reverseproxy mode for the api microservice.

* The app works on kubernetes or in docker-compose.

* The api microservice is exposed to clients outside the k8s cluster via a "NodePort" type K8s service.

* API connects to a postgresql database.

* There is a deployment script included, for installing the app to with minikube.

* There are 2 docker images. One for the postgres microservice and another for the api microservice.

* There are microservice specific readme files, in the respective src sub-folder.

* The app is a single file of python code, instead of multiple files as per MVC.

* Nginx in reverseproxy mode, and the WSGI server "gunicorn" (in python crud api microservice), are started by Supervisord.

A project can get microserviced, containerised, orchestrated and automated in the engineering workflow. Gitlab-Autodevops (with all its pros & cons) is one of the shortest path to integrating, SCM, Code-Coverage, CI/CD, Monitoring and Logging. Albeit the use of heroku buildpacks potentially, introduces surprises that may be difficult to control easily.

## REQUIREMENTS

- A functional healthy kubernetes cluster is required to run the app. I tested it on a minikube cluster and a kind cluster.

## INSTALLATION

There are multiple ways to install the app

  1. kubectl apply -f https://github.com/longwuyuan/python-crud-api/blob/524e85b528ec0c74e6d12955226a4b6b6e16b6c1/install/python-crud-api.yaml

  2. If the code is downloaded locally, then just `kubectl apply -f <path_to_approot>/install/python-crud-api.yaml

  3. Use the docker-compose file at __(path_to_your_git_clone_root_folder_of_this_project)__/src/docker-compose.yml

        ```
        cd <gitroot>/src/
        docker-compose build
        docker-compose up
        ```

## API ENDPOINTS Exposed

Endpoint                    |       Request Header              |       Request Body
----------------------------|-----------------------------------|-------------------
/hello                      | Content-Type: application/json    |
/passengerlist              | Content-Type: application/json    |
/getpassenger/\<uuid\>      | Content-Type: application/json    |
/postpassenger              | Content-Type: application/json              | {"survived":true,"passengerClass":2,"name":"Post-Test-Name","sex":"male","age":27.0,"siblingsOrSpousesAboard":0,"parentsOrChildrenAboard":0,"fare":13.0}       |
/putpassenger/\<uuid\>      | Content-Type: application/json    | {"survived":false,"passengerClass":2,"name":"Put-Test-Name","sex":"male","age":27.0,"siblingsOrSpousesAboard":0,"parentsOrChildrenAboard":0,"fare":13.0}
/deletepassenger/\<uuid\>    | Content-Type: application/json    |

## Networking

- Install a ingress-controller on your cluster like https://kubernetes.github.io/ingress-nginx/ and create a ingress object like this ;
  ```
  kind: Ingress
  metadata:
    name: pycrudapi
    namespace: python-crud-api
  spec:
    ingressClassName: nginx
    rules:
    - host: pycrudapi.dev.devopsdragon.com
      http:
        paths:
        - path: /
          pathType: Exact
          backend:
            service:
              name: pycrudapi
              port:
                number: 80
  ```

- Use port-forwarding https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/ 

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
