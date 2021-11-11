#  Check if required commands (minikube, docker & kubectl) are available
if ! [ -x "$(command -v minikube)" ]; then
  echo 'Error: minikube is not installed or not in PATH.' >&2
  exit 1                                                   
fi  

# Check if docker is working
if ! [ -x "$(command -v kubectl)" ]; then
  echo 'Error: docker-client is not installed or not in PATH.' >&2
  exit 1                                                   
fi  

# Check if kubectl is working
if ! [ -x "$(command -v kubectl)" ]; then
  echo 'Error: kubectl is not installed or not in PATH.' >&2
  exit 1                                                   
fi  

# Re-Configure docker-cli client, to connect to the docker-daemon on the minikube vm. This makes docker build save the docker images on the minikube VM. So our deployment does not need to pull the docker image from the internet as the localy built images are used to create the pods.

eval $(minikube docker-env)

# Get data from minikube instance 
os=`docker info | grep "Operating System" | awk '{print $3}'`
name=`docker info | grep "Name" | awk '{print $2}'`

# Verify minikube data and deploy if verification passes
if [[ "$os" == "Buildroot" ]]; then
    if [[ "$name" == "minikube" ]]; then
	    echo "Minikube found"

        # Delete if exists namespace
        echo "Deleting ns python-crud-api"
        kubectl delete ns python-crud-api --ignore-not-found=true

        # Build the docker images
        echo "Building docker images"
	    docker build -t postgres0 ../src/postgres0/.
	    docker build -t pycrudapi ../src/pycrudapi/.

	    # Deploy the workloads
        echo "Deploying microservices"
        kubectl create ns python-crud-api
	    kubectl apply -f manifests/

        # Checking the install
        echo "Checking deployments"
        sleep 10
        echo "Sending a request using curl"
	    echo ""
        curl `minikube ip`:`kubectl -n python-crud-api get service pycrudapi --output='jsonpath={.spec.ports[0].nodePort}'`
	    echo ""
        echo "Getting the details of the NodePort Service for the API"
	    echo ""
        kubectl -n python-crud-api get svc/pycrudapi
	echo ""
    else
    	echo "Minikube not found ..."
	exit
    fi
else
    echo "Minikube not found ..."
fi
