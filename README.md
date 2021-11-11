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

Minikube <https://github.com/kubernetes/minikube> is required to use this app.

You can also find alternate ways to use the app but use of the docker daemon, inside the minikube vm, to build images is the quickest way. The images are already available for the workloads and there is no need to pull them from some registry on the internet or the network and hence avoid authentication. This helps the app get deployed in seconds anywhere anytime.

## INSTALLATION - minikube

* Minikube provides the docker-environment config details if you type "minikube docker-env".

        * Pass mninikube's docker-environment config, to your laptop's docker-client ;

        ```
        eval $(minikube docker-env)
        ```

        * If successful, then the docker commands, executed in that specific shell (where you typed "eval $(minikube docker-env), will run inside the minikube VM, instead of docker-daemon as configured on your Host OS. This is one easy method to build the images locally (on the minikube vm) . Once the docker images needed to run the microservices, are already built and ready for use in the mnikube VM, we have avoided authentication to registries. But internet connection is required to pull the required bits, specified in the Dockerfile.


        * This local build is automated by the shell script "install_on_minikube.sh". But please use your awareness as not all use-cases are accounted for. If there are problems or issues, please report them and will be fixed.

1. Make sure you have the docker command working on your laptop.

2. Make sure you have __kubectl__ working on your laptop.

3. Go to the minikube folder.

4. Run the script.

        ```
        chmod +x ./install_on_minikube.sh && ./install_on_minikube.sh
        ```

The best way, however, is to use helm and package this app.

## INSTALLATION - docker-compose

* Use the docker-compose file at __(path_to_your_git_clone_root_folder_of_this_project)__/src/docker-compose.yml

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

## TROUBLESHOOTING

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

## TODO : Generate helm chart in CI (using draft maybe)

* The specs provided do not clarify if helm is installed or not. If helm is known to be installed, initialized and working then it would be a simple task to use draft or plain old helm to generate helm package in CI and installation could be done using the official recommended K8s packaging 'helm install'. Will wait for feedback.

## TODO : Write Test cases for CI

* Good to have but not minimalist so need to balance it. In any case the test stage is part of the pipeline so will work on creating tests that run in gitlab-ci. just need to launch both microservices in docker-compose and run curl on the api's .

## TODO : Several changes to make it simple & efficient

## REFERENCES

* <http://www.postgresqltutorial.com/postgresql-uuid/>
* <https://stackoverflow.com/questions/46433459/postgres-select-where-the-where-is-uuid-or-string>
* <http://initd.org/psycopg/docs/sql.html#module-psycopg2.sql>
* <http://initd.org/psycopg/docs/extras.html>
* many more
