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
  - `kube-compose top SERVICE` => `kubectl exec pod -- cat /proc/*/stats`
  - `kube-compose stats SERVICE` => `kubectl top pod`
  - `kube-compose events SERVICE` => `kubectl events`
  - `kube-compose start SERVICE` => `kubectl scale --replicas={compose_defined}`
  - `kube-compose scale SERVICE` => `kubectl scale --replicas={user_specified}`
  - `kube-compose stop SERVICE` => `kubectl scale --replicas=0`
- helm-like features
  - `kube-compose ls` => `helm list`
  - `kube-compose template` => `helm template`
  - `kube-compose history` => `helm history`
  - `kube-compose status` => `helm status`
  - `kube-compose get WHAT` => `helm get WHAT`
  - `kube-compose rollback REVISION` => `helm rollback REVISION`
- additional features
  - `kube-compose volume ...` => manage docker-compose defined volumes as persistent volume claims
    - `kube-compose volume create [VOLUME]` => create the claim(s)
    - `kube-compose volume rm [VOLUME]` => delete the claim(s)
  - `kube-compose diff` => `diff -Naur <(helm get values) <(docker-compose config)`
  - `kube-compose version SERVICE [<newversion> | major | minor | patch]` => like npm version but for services in the docker-compose.yaml
  - `kube-compose port-forward SERVICE local:remote`

## Pre-requisites
- kubernetes cluster
- kubectl
- helm
- docker-compose

## Installation
```bash
# install off of pypi
pip install kube-compose

# verify install was successful
kube-compose --help
```

## CLI Usage with Docker
```bash
# Assuming your kubeconfig is at the default location ~/.kube/config
alias kube-compose="docker run -v .:/work -v ~/.kube/config:/work/.kube/config -it u8sand/kube-compose"

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

# 
# start the docker-compose service(s) on the kubernetes cluster
kube-compose -f tests/units/simple/docker-compose.yaml up

# verify it's running at http://localhost
```
