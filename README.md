# kube-compose

An opinionated way of deploying docker-compose to kubernetes clusters by managing them with a helm chart.

The CLI is intended to be easy to use for those familiar with docker-compose and includes some additional features. Basically all features expect you to have a `docker-compose.yaml` file in the working directory.

- `kube-compose init` => specify the helm release name/namespace in your `docker-compose.yaml` file
- docker-compose-like features
  - `kube-compose up` => `helm install/upgrade` + volume create (pvc)
  - `kube-compose down` => `helm uninstall`
  - `kube-compose ps` => `helm status`
  - `kube-compose logs SERVICE` => `kubectl logs`
  - `kube-compose exec SERVICE` => `kubectl exec`
  - `kube-compose restart SERVICE` => `kubectl rollout restart`
- additional features
  - `kube-compose volume ...` => manage docker-compose defined volumes as persistent volume claims
    - `kube-compose volume create [VOLUME]` => create the claim(s)
    - `kube-compose volume rm [VOLUME]` => delete the claim(s)
  - `kube-compose diff` => `diff -Naur <(helm get values) <(docker-compose config)`
  - `kube-compose version SERVICE [<newversion> | major | minor | patch]` => like npm version but for services in the docker-compose.yaml

## Pre-requisites
- kubernetes cluster
- kubectl
- helm

## Installation
```bash
# install off of pypi
pip install kube-compose

# verify install was successful
kube-compose --help
```

## End-to-end Example with K3D
```bash
# launch a test kubernetes cluster
k3d cluster create -a1 -p "80:80@loadbalancer" -p "443:443@loadbalancer"

# one option for auto-creating Ingress resources from annotations on the deployment
helm repo add maayanlab https://maayanlab.github.io/helm-charts
helm install kubernetes-auto-ingress maayanlab/kubernetes-auto-ingress --set ingressClassName=traefik

# create the docker-compose.yaml
cat > docker-compose.yaml << EOF
version: '3'
x-kubernetes:
  # this is the helm chart release name and namespace
  name: test
  namespace: default
services:
  # a deployment is created with this name
  test-web:
    image: nginx:latest
    ports:
      # a service is created exposing this port
      - 80
    x-kubernetes:
      # these are the kubernetes annotations added to the deployment
      annotations:
        # this annotation causes a ingress to be created for the deployment
        maayanlab.cloud/ingress: http://localhost
EOF

# start the docker-compose service(s) on the kubernetes cluster
kube-compose up

# verify it's running at http://localhost
```
